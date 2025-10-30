"""
Módulo de notificaciones al WebSocket
Envía eventos HTTP POST a ws://localhost:8080/notify/{room}
cuando hay cambios en el REST API
"""
import httpx
import os
from typing import Optional

WS_BASE_URL = os.getenv("WS_BASE_URL", "http://localhost:8080")
WS_ENABLED = os.getenv("WS_NOTIFICATIONS_ENABLED", "1") == "1"


async def notify_websocket(
    room: str,
    event: str,
    message: str,
    data: Optional[dict] = None
):
    """
    Envía notificación al WebSocket para que replique a clientes conectados
    
    Args:
        room: Sala del WebSocket (reports, comments, general, etc.)
        event: Tipo de evento (new_report, update_report, comment_added, etc.)
        message: Mensaje descriptivo del evento
        data: Datos adicionales opcionales
    """
    if not WS_ENABLED:
        return  # WebSocket notifications deshabilitadas
    
    try:
        payload = {
            "event": event,
            "message": message,
        }
        if data:
            payload["data"] = data
        
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.post(
                f"{WS_BASE_URL}/notify/{room}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ WebSocket notificado: {event} en sala '{room}'")
            else:
                print(f"⚠️ WebSocket respondió con status {response.status_code}")
                
    except httpx.TimeoutException:
        print(f"⏱️ Timeout al notificar WebSocket (sala: {room}, evento: {event})")
    except httpx.ConnectError:
        print(f"❌ No se pudo conectar al WebSocket en {WS_BASE_URL}")
    except Exception as e:
        print(f"❌ Error notificando WebSocket: {e}")


# Funciones helper específicas por evento
async def notify_new_report(report_id: int, title: str):
    """Notifica creación de nuevo reporte"""
    await notify_websocket(
        room="reports",
        event="new_report",
        message=f"Nuevo reporte creado: {title}",
        data={"report_id": report_id, "title": title}
    )


async def notify_update_report(report_id: int, title: str):
    """Notifica actualización de reporte"""
    await notify_websocket(
        room="reports",
        event="update_report",
        message=f"Reporte actualizado: {title}",
        data={"report_id": report_id, "title": title}
    )


async def notify_comment_added(report_id: int, comment_id: int, content: str):
    """Notifica nuevo comentario en reporte"""
    await notify_websocket(
        room="comments",
        event="comment_added",
        message=f"Nuevo comentario en reporte #{report_id}",
        data={"report_id": report_id, "comment_id": comment_id, "preview": content[:100]}
    )


async def notify_rating_added(report_id: int, rating_value: int):
    """Notifica nueva puntuación"""
    await notify_websocket(
        room="reports",
        event="rating_added",
        message=f"Nueva puntuación en reporte #{report_id}: {rating_value}/5",
        data={"report_id": report_id, "rating": rating_value}
    )
