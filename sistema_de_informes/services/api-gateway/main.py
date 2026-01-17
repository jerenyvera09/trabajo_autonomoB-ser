from __future__ import annotations

import os
from typing import Dict, Optional

import httpx
from dotenv import load_dotenv
import asyncio

from fastapi import FastAPI, Header, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="API Gateway (Segundo Parcial)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REST_API_URL = (os.getenv("REST_API_URL") or "http://rest-api:8000").rstrip("/")
AUTH_SERVICE_URL = (os.getenv("AUTH_SERVICE_URL") or "http://auth-service:8001").rstrip("/")
PAYMENT_SERVICE_URL = (os.getenv("PAYMENT_SERVICE_URL") or "http://payment-service:8002").rstrip("/")
AI_ORCHESTRATOR_URL = (os.getenv("AI_ORCHESTRATOR_URL") or "http://ai-orchestrator:8003").rstrip("/")
GRAPHQL_URL = (os.getenv("GRAPHQL_URL") or "http://graphql:4000").rstrip("/")
WS_URL = (os.getenv("WS_URL") or "ws://ws:8080/ws").rstrip("/")


def _pick_backend(path: str) -> str:
    p = "/" + (path or "").lstrip("/")

    if p.startswith("/auth"):
        return AUTH_SERVICE_URL
    if p.startswith("/payments") or p.startswith("/partners") or p.startswith("/webhooks"):
        return PAYMENT_SERVICE_URL
    if p.startswith("/ai"):
        return AI_ORCHESTRATOR_URL

    if p.startswith("/graphql"):
        return GRAPHQL_URL

    # Todo lo demás cae al REST API (incluye /api/v1/*, /docs, /openapi.json, etc.)
    return REST_API_URL


def _rewrite_path(path: str) -> str:
    p = "/" + (path or "").lstrip("/")
    # Para AI Orchestrator montamos bajo /ai/*, pero el servicio real expone /chat, /health, etc.
    if p.startswith("/ai/"):
        return p.replace("/ai", "", 1)
    if p == "/ai":
        return "/"

    # GraphQL se expone vía gateway en /graphql, pero el servidor Apollo suele escuchar en "/".
    if p == "/graphql":
        return "/"
    if p.startswith("/graphql/"):
        return p.replace("/graphql", "", 1)
    return p


@app.websocket("/ws")
async def ws_proxy(websocket: WebSocket):
    """Proxy WebSocket: browser -> api-gateway -> ws service.

    Permite cumplir el requisito: "comunicación a través del API Gateway".
    """

    await websocket.accept()

    # Preservar query string (room, token, etc.)
    qs = websocket.url.query
    upstream = WS_URL
    if qs:
        upstream = f"{upstream}?{qs}"

    try:
        import websockets  # type: ignore
    except Exception as e:
        await websocket.close(code=1011, reason=f"Gateway missing dependency websockets: {e}")
        return

    try:
        async with websockets.connect(upstream) as upstream_ws:

            async def client_to_upstream():
                try:
                    while True:
                        msg = await websocket.receive_text()
                        await upstream_ws.send(msg)
                except WebSocketDisconnect:
                    return
                except Exception:
                    return

            async def upstream_to_client():
                try:
                    async for msg in upstream_ws:
                        # upstream msg puede ser str/bytes
                        if isinstance(msg, bytes):
                            await websocket.send_bytes(msg)
                        else:
                            await websocket.send_text(msg)
                except Exception:
                    return

            await asyncio.gather(client_to_upstream(), upstream_to_client())
    except Exception as e:
        await websocket.close(code=1011, reason=f"Gateway upstream ws error: {e}")


@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]) 
async def proxy(path: str, request: Request, authorization: Optional[str] = Header(None)):
    backend = _pick_backend(path)
    out_path = _rewrite_path(path)

    url = f"{backend}{out_path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"

    headers: Dict[str, str] = {}
    for k, v in request.headers.items():
        lk = k.lower()
        if lk in ("host", "content-length"):
            continue
        headers[k] = v
    if authorization:
        headers["Authorization"] = authorization

    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.request(method=request.method, url=url, headers=headers, content=body)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Gateway upstream error: {e}")

    # Respuesta (preservar content-type)
    return (
        resp.content,
        resp.status_code,
        {"content-type": resp.headers.get("content-type", "application/octet-stream")},
    )
