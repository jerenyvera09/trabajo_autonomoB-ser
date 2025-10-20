# WebSocket Server (Integrante 3: Vera Mero Jereny Jhonnayker - Go/Gorilla)

Servidor WebSocket para notificaciones en tiempo real.  
**Semana 5**: Implementa emisión de notificaciones cuando se crea un nuevo reporte.

---

## Requisitos

- Go 1.20+

---

## Ejecutar

```bash
go mod tidy
go run main.go
```

Servidor disponible en: **http://localhost:8080**

---

## 🔗 Endpoints (Semana 5)

### 1. WebSocket Connection

```
ws://localhost:8080/ws
```

### 2. Health Check

```
GET http://localhost:8080/
```

Respuesta:

```json
{ "status": "ok", "service": "ws" }
```

### 3. Notificar Nuevo Reporte (POST)

```
POST http://localhost:8080/notify
Content-Type: application/json

{
  "message": "Se ha creado un nuevo reporte"
}
```

Este endpoint envía a todos los clientes conectados:

```json
{
  "event": "new_report",
  "message": "Se ha creado un nuevo reporte"
}
```

---

## 🧪 Probar

### Opción 1: Usando PieSocket o WebSocket Client

1. Conéctate a: `ws://localhost:8080/ws`
2. Envía el texto: `new_report`
3. Todos los clientes conectados recibirán la notificación

### Opción 2: Usando curl para simular el evento

```bash
curl -X POST http://localhost:8080/notify \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Nuevo reporte creado desde REST API\"}"
```

### Opción 3: Múltiples clientes (wscat)

Terminal 1:

```bash
wscat -c ws://localhost:8080/ws
```

Terminal 2:

```bash
wscat -c ws://localhost:8080/ws
```

Escribe `new_report` en una terminal y observa el broadcast en ambas.

---

## 🔒 Seguridad

`CheckOrigin` está abierto solo para demo (`return true`).  
**En producción**: Restringe dominios permitidos.

---
