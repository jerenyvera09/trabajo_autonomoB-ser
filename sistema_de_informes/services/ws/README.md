# WebSocket Server (Integrante 3: Vera Mero Jereny Jhonnayker - Go/Gorilla)

Servidor WebSocket para notificaciones en tiempo real.  
**Semana 5**: Implementa emisión de notificaciones cuando se crea un nuevo reporte.
**Semana 6**: Añade salas/canales, notificaciones por sala, keepalive (ping/pong), configuración por entorno y autenticación opcional.

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

## ⚙️ Variables de entorno

- `WS_PORT` (opcional): Puerto del servidor (por defecto `8080`).
- `ALLOWED_ORIGINS` (opcional): Lista CSV de orígenes permitidos para el handshake WS (vacío = permitir todos en dev).
- `WS_REQUIRE_AUTH` (opcional): Si vale `1`, exige token JWT para conectar.
- `WS_JWT_SECRET` (opcional): Clave HS256 para validar el JWT cuando `WS_REQUIRE_AUTH=1`.

Ejemplo (Windows CMD):

```cmd
set WS_PORT=8081
set ALLOWED_ORIGINS=http://localhost:5173
set WS_REQUIRE_AUTH=1
set WS_JWT_SECRET=supersecreto
go run main.go
```

---

## 🔗 Endpoints (Semana 5 y 6)

### 1. WebSocket Connection

```
ws://localhost:8080/ws?room=reports
```

Si `WS_REQUIRE_AUTH=1`, agrega `Authorization: Bearer <token>` o `?token=<token>`.

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

Por defecto envía a la sala `general`. Para una sala específica (Semana 6):

```
POST http://localhost:8080/notify/reports
Content-Type: application/json

{
  "event": "new_report",
  "message": "Se ha creado un nuevo reporte en la sala reports"
}
```

Respuesta enviada a los clientes conectados de la sala:

```json
{
  "event": "new_report",
  "message": "Se ha creado un nuevo reporte"
}
```

---

## 🧪 Probar

### Opción 1: Usando PieSocket o WebSocket Client

1. Conéctate a: `ws://localhost:8080/ws?room=reports`
2. Envía el texto: `new_report`
3. Todos los clientes conectados en la sala `reports` recibirán la notificación

### Opción 2: Usando curl para simular el evento

```bash
curl -X POST http://localhost:8080/notify \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Nuevo reporte creado desde REST API\"}"
```

### Opción 3: Múltiples clientes (wscat)

Terminal 1:

```bash
wscat -c ws://localhost:8080/ws?room=reports
```

Terminal 2:

```bash
wscat -c ws://localhost:8080/ws?room=reports
```

Escribe `new_report` en una terminal y observa el broadcast en ambas (solo sala `reports`).

---

## 🔒 Seguridad

**Handshake**: usa `ALLOWED_ORIGINS` para restringir orígenes (en dev, si está vacío, se permiten todos).

**Auth opcional**: Activa `WS_REQUIRE_AUTH=1` y define `WS_JWT_SECRET` (HS256). El token se pasa por `Authorization: Bearer` o `?token=` en la URL de conexión.

**Salas**: Cada conexión cae en `general` o en la sala indicada por `?room=`. Las notificaciones se emiten solo a esa sala.

---

## 📡 Tabla de eventos recomendados (Semana 6)

| Evento           | Emisor          | Descripción                             |
| ---------------- | --------------- | --------------------------------------- |
| `new_report`     | WS/REST/Cliente | Se creó un nuevo reporte                |
| `update_report`  | REST            | Un reporte fue actualizado o eliminado  |
| `update_user`    | REST            | Un usuario fue actualizado o eliminado  |
| `entity_changed` | REST (legado)   | Evento genérico (sigue siendo aceptado) |

Notas:

- El endpoint `/notify` admite un campo `event` en el JSON. Cualquier valor se reenvía a los clientes.
- A partir de Semana 6, el servicio REST envía `update_report` para cambios en reportes, y `update_user` para cambios en usuarios.

### Ejemplos con `wscat`

```bash
wscat -c ws://localhost:8080/ws?room=reports
```

Desde otra terminal:

```bash
curl -X POST http://localhost:8080/notify/reports \
  -H "Content-Type: application/json" \
  -d '{"event":"update_report","message":"Reporte #42 actualizado"}'
```

### Ejemplos con DevTools (navegador)

```js
const ws = new WebSocket("ws://localhost:8080/ws?room=reports");
ws.onmessage = (e) => console.log("WS:", e.data);
// Simular desde REST o curl el envío de eventos a la sala "reports"
```
