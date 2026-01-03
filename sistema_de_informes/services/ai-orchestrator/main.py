from __future__ import annotations

import os
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from llm.mock_llm import MockLLM
from llm.provider import LLMProvider
from schemas import ChatIn, ChatOut, ToolResult
from tools.action_tool import ActionTool
from tools.info_tool import InfoTool

load_dotenv()

app = FastAPI(title="AI Orchestrator")

allow_origins = os.getenv("ALLOW_ORIGINS") or "*"
origins = [o.strip() for o in allow_origins.split(",") if o.strip()] if allow_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_llm_provider() -> LLMProvider:
    """Selecciona el LLM vía Strategy Pattern.

    Semana 2: solo soporta 'mock'.
    """

    provider = (os.getenv("LLM_PROVIDER") or "mock").lower()
    if provider == "mock":
        return MockLLM()
    raise HTTPException(status_code=400, detail=f"LLM_PROVIDER no soportado en Semana 2: {provider}")


TOOLS = {
    "info": InfoTool(),
    "action": ActionTool(),
}


@app.get("/")
def root():
    return {"status": "ok", "service": "ai-orchestrator"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-orchestrator"}


@app.post("/chat", response_model=ChatOut)
def chat(payload: ChatIn):
    llm = get_llm_provider()

    tools_used = []
    if payload.toolName:
        tool_key = payload.toolName.strip().lower()
        tool = TOOLS.get(tool_key)
        if not tool:
            raise HTTPException(status_code=400, detail=f"Tool no soportada en Semana 2: {payload.toolName}")
        result = tool.run(payload.toolArgs)
        tools_used.append(ToolResult(tool=tool.name, result=result))

    reply = llm.generate(payload.message)

    # Si se usó tool, devolvemos una nota mínima adicional (sin IA real)
    if tools_used:
        reply = f"{reply}\n\n(mock) Tools usadas: {', '.join([t.tool for t in tools_used])}"

    return ChatOut(provider=(os.getenv("LLM_PROVIDER") or "mock"), reply=reply, toolsUsed=tools_used)
