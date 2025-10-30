# 🌐 Servicio WebSocket - Sistema de Informes

Servidor WebSocket en Go (Gorilla) para notificaciones en tiempo real con salas (rooms), keepalive ping/pong y autenticación JWT opcional.

## 📦 Características

- Salas (rooms) por querystring: `?room=reports`, `?room=general`
- Keepalive ping/pong automático cada 30s
- Eventos estándar: `new_report`, `update_report`, `comment_added`, `rating_added`
- HTTP a WS bridge: `POST /notify` y `POST /notify/{room}`
- CORS configurable y JWT opcional (HS256)

## ⚙️ Variables de entorno

- WS_PORT: Puerto del servidor (default 8080)
- ALLOWED_ORIGINS: CSV de orígenes permitidos para handshake (default `*` en dev)
- WS_REQUIRE_AUTH: 1 para exigir JWT al conectar (default 0)
- WS_JWT_SECRET: Clave para validar JWT (requerida si WS_REQUIRE_AUTH=1)

Ejemplo (Windows PowerShell):

```
$env:WS_PORT=8080; $env:ALLOWED_ORIGINS="http://localhost:5173"; $env:WS_REQUIRE_AUTH=0; go run .
```

## 🚀 Arranque

1) Instalar dependencias: `go mod tidy`
2) Ejecutar: `go run .`

Servicios:
- WS: ws://localhost:8080/ws?room=reports
- Healthcheck: GET http://localhost:8080/ → `{ "status": "ok", "service": "ws" }`

## 🔗 Endpoints HTTP

- GET `/` → Healthcheck
- GET `/ws?room=<room>&token=<jwt>` → Conexión WebSocket
- POST `/notify` → Notifica a la sala `general`
- POST `/notify/{room}` → Notifica a la sala indicada

Body JSON de notificación:

```json
{
  "event": "new_report",
  "message": "Se ha creado un nuevo reporte",
  "data": { "reporteId": 123, "titulo": "Falla" }
}
```

Respuesta:

```json
{ "status": "ok" }
```

## 🧪 Pruebas rápidas en el navegador

Abre DevTools y ejecuta:

```js
const ws = new WebSocket("ws://localhost:8080/ws?room=reports");
ws.onmessage = (e) => console.log("WS ←", e.data);

// Opcional: enviar un ping de prueba
ws.onopen = () => ws.send(JSON.stringify({ event: "ping" }));
```

Luego dispara una notificación HTTP (ejemplo con PowerShell):

```
Invoke-RestMethod -Method Post -Uri http://localhost:8080/notify/reports -ContentType 'application/json' -Body '{"event":"new_report","message":"Nuevo reporte","data":{"reporteId":1}}'
```

## 📜 Eventos de sistema (payloads sugeridos)

- new_report: `{ reporteId, titulo, creadoEn }`
- update_report: `{ reporteId, titulo, estadoAnterior, estadoNuevo, actualizadoEn }`
- comment_added: `{ reporteId, comentarioId, contenido, creadoEn }`
- rating_added: `{ reporteId, valor }`

---

Contenido histórico (obsoleto) a continuación:

**Semana 6**: Servidor WebSocket con **salas (rooms)**, **ping/pong keepalive** y **eventos en tiempo real** (new_report, update_report, comment_added).**Semana 6**: Servidor WebSocket con **salas (rooms)**, **ping/pong keepalive** y **eventos estándar** (new_report, update_report, comment_added).Servidor WebSocket para notificaciones en tiempo real.

---**Semana 5**: Implementa emisión de notificaciones cuando se crea un nuevo reporte.

## 📦 Características---**Semana 6**: Añade salas/canales, notificaciones por sala, keepalive (ping/pong), configuración por entorno y autenticación opcional.

✅ **Salas (Rooms)**: Los clientes pueden suscribirse a salas específicas (`?room=reports`, `?room=general`) ## 📦 Características---

✅ **Ping/Pong**: Keepalive automático cada 30s para mantener conexiones activas

✅ **Eventos Estándar**: Soporte para `new_report`, `update_report`, `comment_added` ✅ **Salas (Rooms)**: Los clientes pueden suscribirse a salas específicas (`?room=reports`, `?room=general`) ## Requisitos

✅ **Auth Opcional**: JWT via header `Authorization` o query `?token=`

✅ **CORS**: Configuración flexible para desarrollo y producción ✅ **Ping/Pong**: Keepalive automático cada 30s para mantener conexiones activas

✅ **Notificaciones HTTP**: Endpoint `/notify/{room}` para emitir eventos desde backend

✅ **Eventos Estándar**: Soporte para `new_report`, `update_report`, `comment_added` - Go 1.20+

---

✅ **Auth Opcional**: JWT via header `Authorization` o query `?token=`

## 🔌 Iniciar Servidor

✅ **CORS**: Configuración flexible para desarrollo y producción ---

`````bash

go mod tidy✅ **Notificaciones HTTP**: Endpoint `/notify/{room}` para emitir eventos desde backend

go run main.go

```## Ejecutar



Servidor WebSocket en: **ws://localhost:8080**  ---

Healthcheck: **http://localhost:8080** (JSON: `{"status":"ok","service":"ws"}`)

````bash

---

## 🔌 Iniciar Servidorgo mod tidy

## 🛠️ Configuración (Variables de Entorno)

go run main.go

| Variable | Descripción | Default | Ejemplo |

|----------|-------------|---------|---------|```bash```

| `WS_PORT` | Puerto del servidor | `8080` | `8080` |

| `WS_REQUIRE_AUTH` | Requiere JWT | `0` (deshabilitado) | `1` |go run main.go

| `WS_JWT_SECRET` | Secreto para validar JWT | - | `mi_secreto` |

| `ALLOWED_ORIGINS` | Orígenes permitidos (CSV) | `*` (todos) | `http://localhost:5173,https://app.com` |```Servidor disponible en: **http://localhost:8080**



### Ejemplo (Windows CMD):



```cmdServidor WebSocket en: **ws://localhost:8080**  ---

set WS_PORT=8081

set ALLOWED_ORIGINS=http://localhost:5173Healthcheck: **http://localhost:8080** (JSON: `{"status":"ok","service":"ws"}`)

set WS_REQUIRE_AUTH=1

set WS_JWT_SECRET=supersecreto## ⚙️ Variables de entorno

go run main.go

```---



---- `WS_PORT` (opcional): Puerto del servidor (por defecto `8080`).



## 📡 Eventos Soportados## 🛠️ Configuración (Variables de Entorno)- `ALLOWED_ORIGINS` (opcional): Lista CSV de orígenes permitidos para el handshake WS (vacío = permitir todos en dev).



### **Tabla de Eventos del Sistema**- `WS_REQUIRE_AUTH` (opcional): Si vale `1`, exige token JWT para conectar.



| Evento | Descripción | Formato JSON | Trigger | Ejemplo || Variable | Descripción | Default | Ejemplo |- `WS_JWT_SECRET` (opcional): Clave HS256 para validar el JWT cuando `WS_REQUIRE_AUTH=1`.

|--------|-------------|--------------|---------|---------|

| `new_report` | Nuevo reporte creado | `{"event": "new_report", "payload": {...}}` | `POST /reportes` en REST API | Ver ejemplo ⬇️ ||----------|-------------|---------|---------|

| `update_report` | Reporte actualizado | `{"event": "update_report", "payload": {...}}` | `PUT /reportes/{id}` en REST API | Ver ejemplo ⬇️ |

| `comment_added` | Nuevo comentario agregado | `{"event": "comment_added", "payload": {...}}` | `POST /comentarios` en REST API | Ver ejemplo ⬇️ || `WS_PORT` | Puerto del servidor | `8080` | `8080` |Ejemplo (Windows CMD):



---| `WS_REQUIRE_AUTH` | Requiere JWT | `0` (deshabilitado) | `1` |



### **Ejemplos de Eventos JSON**| `WS_JWT_SECRET` | Secreto para validar JWT | - | `mi_secreto` |```cmd



#### 1. **new_report** (Reporte creado)| `ALLOWED_ORIGINS` | Orígenes permitidos (CSV) | `*` (todos) | `http://localhost:5173,https://app.com` |set WS_PORT=8081



```jsonset ALLOWED_ORIGINS=http://localhost:5173

{

  "event": "new_report",---set WS_REQUIRE_AUTH=1

  "payload": {

    "reporteId": 123,set WS_JWT_SECRET=supersecreto

    "titulo": "Problema en servidor principal",

    "descripcion": "El servidor no responde",## 📡 Eventos Soportadosgo run main.go

    "estado": "Abierto",

    "prioridad": "Alta",````

    "usuario": "usuario@example.com",

    "creadoEn": "2024-01-15T10:30:00Z"### **Eventos que el Cliente Puede Enviar**

  }

}---

`````

| Evento | Descripción | Formato | Ejemplo |

**Trigger:** Cuando se ejecuta `POST /reportes` en el REST API.

|--------|-------------|---------|---------|## 🔗 Endpoints (Semana 5 y 6)

---

| `new_report` | Notifica creación de reporte | String plano | `"new_report"` |

#### 2. **update_report** (Reporte actualizado)

| `update_report` | Notifica actualización de reporte | String plano | `"update_report"` |### 1. WebSocket Connection

`````json

{| `comment_added` | Notifica nuevo comentario | String plano | `"comment_added"` |

  "event": "update_report",

  "payload": {| Mensaje personalizado | Cualquier otro mensaje | JSON o texto | `{"custom": "data"}` |```

    "reporteId": 123,

    "titulo": "Problema en servidor principal - RESUELTO",ws://localhost:8080/ws?room=reports

    "estadoAnterior": "Abierto",

    "estadoNuevo": "Cerrado",### **Respuesta del Servidor**```

    "actualizadoEn": "2024-01-15T14:45:00Z",

    "actualizadoPor": "admin@example.com"Todos los eventos estándar se envían con formato JSON:Si `WS_REQUIRE_AUTH=1`, agrega `Authorization: Bearer <token>` o `?token=<token>`.

  }

}````json### 2. Health Check

`````

{

**Trigger:** Cuando se ejecuta `PUT /reportes/{id}` en el REST API.

"event": "new_report",```

---

"message": "Se ha creado un nuevo reporte"GET http://localhost:8080/

#### 3. **comment_added** (Comentario agregado)

}```

````````json

{````

  "event": "comment_added",

  "payload": {Respuesta:

    "reporteId": 123,

    "comentarioId": 45,```````json

    "contenido": "Se reinició el servidor y ahora funciona correctamente",

    "usuario": "tecnico@example.com",{```json

    "creadoEn": "2024-01-15T11:00:00Z"

  }  "event": "update_report",{ "status": "ok", "service": "ws" }

}

```  "message": "Se ha actualizado un reporte"```



**Trigger:** Cuando se ejecuta `POST /comentarios` en el REST API.}



---```### 3. Notificar Nuevo Reporte (POST)



## 🔗 Endpoints HTTP



### 1. **WebSocket Connection**```json```



```{POST http://localhost:8080/notify

ws://localhost:8080/ws?room=reports

```  "event": "comment_added",Content-Type: application/json



**Parámetros:**  "message": "Se agregó un comentario al reporte"

- `room`: Sala a la que suscribirse (ej: `reports`, `general`)

- `token` (opcional): JWT si `WS_REQUIRE_AUTH=1`}{



**Headers opcionales:**```  "message": "Se ha creado un nuevo reporte"

- `Authorization: Bearer <token>` (si `WS_REQUIRE_AUTH=1`)

}

---

---```

### 2. **Health Check**



````````

GET http://localhost:8080/## 🧪 Probar ConexiónPor defecto envía a la sala `general`. Para una sala específica (Semana 6):

````



**Respuesta:**

### **Opción 1: DevTools del Navegador**```

```json

{POST http://localhost:8080/notify/reports

  "status": "ok",

  "service": "ws"Abre la consola de DevTools y ejecuta:Content-Type: application/json

}

````

---```javascript{

### 3. **Notificar Evento (desde REST API)**const ws = new WebSocket('ws://localhost:8080/ws?room=reports'); "event": "new_report",

```"message": "Se ha creado un nuevo reporte en la sala reports"

POST http://localhost:8080/notify/{room}

Content-Type: application/jsonws.onopen = () => {}

```

console.log('✅ Conectado a sala "reports"');```

**Parámetros:**

- `{room}`: Sala destino (ej: `reports`, `general`) ws.send('new_report'); // Enviar evento

**Body:**};Respuesta enviada a los clientes conectados de la sala:

````json

{

  "event": "new_report",ws.onmessage = (event) => {```json

  "payload": {

    "reporteId": 123,  console.log('📩 Mensaje recibido:', JSON.parse(event.data));{

    "titulo": "Nuevo reporte de prueba"

  }};  "event": "new_report",

}

```  "message": "Se ha creado un nuevo reporte"



**Respuesta:**ws.onerror = (error) => {}



```json  console.error('❌ Error:', error);```

{

  "status": "ok",};

  "message": "Evento new_report enviado a sala reports",

  "recipients": 5---

}

```ws.onclose = () => {



---  console.log('🔌 Conexión cerrada');## 🧪 Probar



## 🧪 Probar WebSocket};



### **Opción 1: Con `test.html` (Navegador)**```### Opción 1: Usando PieSocket o WebSocket Client



1. Abrir el archivo `test.html` en tu navegador

2. Conectar a `ws://localhost:8080/ws?room=reports`

3. Enviar mensajes y recibir notificaciones en tiempo real### **Opción 2: wscat (CLI)**1. Conéctate a: `ws://localhost:8080/ws?room=reports`



---2. Envía el texto: `new_report`



### **Opción 2: Con `curl` (Terminal)**Instala `wscat` globalmente:3. Todos los clientes conectados en la sala `reports` recibirán la notificación



```bash

# Notificar nuevo reporte desde terminal

curl -X POST http://localhost:8080/notify/reports \```bash### Opción 2: Usando curl para simular el evento

  -H "Content-Type: application/json" \

  -d "{\"event\":\"new_report\",\"payload\":{\"reporteId\":123,\"titulo\":\"Test\"}}"npm install -g wscat

````

````````bash

---

curl -X POST http://localhost:8080/notify \

### **Opción 3: Con JavaScript (Frontend)**

Conecta y envía eventos:  -H "Content-Type: application/json" \

```javascript

// Conectar al WebSocket  -d "{\"message\":\"Nuevo reporte creado desde REST API\"}"

const ws = new WebSocket('ws://localhost:8080/ws?room=reports');

```bash```

// Escuchar mensajes

ws.onmessage = (event) => {# Conectar a sala "reports"

  const data = JSON.parse(event.data);

  console.log('Evento recibido:', data.event);wscat -c "ws://localhost:8080/ws?room=reports"### Opción 3: Múltiples clientes (wscat)

  console.log('Payload:', data.payload);



  if (data.event === 'new_report') {

    alert(`Nuevo reporte: ${data.payload.titulo}`);# Enviar eventos (escribe en el prompt)Terminal 1:

  }

};> new_report



// Enviar ping manual> update_report```bash

ws.send('ping');

```> comment_addedwscat -c ws://localhost:8080/ws?room=reports



---```````



## 🔗 Integración con REST API### **Opción 3: test.html (Interfaz Web)**Terminal 2:



El REST API notifica automáticamente al WebSocket mediante `ws_notifier.py`:Abre `test.html` en el navegador (incluido en la carpeta `ws/`):```bash



**Archivo:** `services/rest-api/ws_notifier.py`wscat -c ws://localhost:8080/ws?room=reports



```python1. Ingresa la sala (ej: `reports`)```

import httpx

2. Clic en "Conectar"

async def notify_new_report(reporte_id: int, titulo: str):

    """Notifica al WebSocket cuando se crea un reporte"""3. Usa los botones para enviar eventos (`new_report`, `update_report`, `comment_added`)Escribe `new_report` en una terminal y observa el broadcast en ambas (solo sala `reports`).

    payload = {

        "event": "new_report",4. Observa los mensajes recibidos en el panel

        "payload": {

            "reporteId": reporte_id,---

            "titulo": titulo

        }---

    }

    async with httpx.AsyncClient() as client:## 🔒 Seguridad

        await client.post("http://localhost:8080/notify/reports", json=payload)

```## 🌐 Endpoints HTTP



**Usado en:** `routers/reporte.py` (línea 39) y `routers/comentario.py` (línea 28)**Handshake**: usa `ALLOWED_ORIGINS` para restringir orígenes (en dev, si está vacío, se permiten todos).



---### **1️⃣ WebSocket Handshake**



## 🛠️ Tecnologías**Auth opcional**: Activa `WS_REQUIRE_AUTH=1` y define `WS_JWT_SECRET` (HS256). El token se pasa por `Authorization: Bearer` o `?token=` en la URL de conexión.



- **Go** 1.20+```

- **Gorilla WebSocket** para conexiones WS

- **JWT** para autenticación opcionalws://localhost:8080/ws?room={sala}[&token={jwt}]**Salas**: Cada conexión cae en `general` o en la sala indicada por `?room=`. Las notificaciones se emiten solo a esa sala.

- **CORS** para desarrollo local

- **Ping/Pong** para keepalive automático```



------



## 📝 Notas Importantes**Parámetros:**



- ✅ **Salas independientes**: Cada sala (`reports`, `general`) recibe solo sus eventos- `room` (opcional): Nombre de la sala (default: `general`)## 📡 Tabla de eventos recomendados (Semana 6)

- ✅ **Keepalive automático**: Ping/pong cada 30s para evitar timeouts

- ✅ **REST → WS automático**: El REST API notifica al WS sin intervención manual- `token` (opcional): JWT si `WS_REQUIRE_AUTH=1`

- ✅ **JSON estándar**: Todos los eventos usan el formato `{"event": "...", "payload": {...}}`

- ✅ **Auth opcional**: Deshabilitada por default (`WS_REQUIRE_AUTH=0`)| Evento | Emisor | Descripción |



---**Ejemplo:**| ---------------- | --------------- | --------------------------------------- |



## 🧪 Pruebas de Integración```| `new_report` | WS/REST/Cliente | Se creó un nuevo reporte |



### **Test 1: Crear reporte desde REST → Recibir evento en WS**ws://localhost:8080/ws?room=reports| `update_report` | REST | Un reporte fue actualizado o eliminado |



1. Conectar cliente WebSocket a `ws://localhost:8080/ws?room=reports`ws://localhost:8080/ws?room=general&token=eyJhbGciOiJIUzI...| `update_user` | REST | Un usuario fue actualizado o eliminado |

2. Ejecutar `POST /reportes` en el REST API

3. Verificar que el cliente WS recibe el evento `new_report` con el payload correcto```| `entity_changed` | REST (legado) | Evento genérico (sigue siendo aceptado) |



------Notas:



### **Test 2: Actualizar reporte → Recibir evento**### **2️⃣ Notificar Evento por HTTP**- El endpoint `/notify` admite un campo `event` en el JSON. Cualquier valor se reenvía a los clientes.



1. Conectar cliente WebSocket a `ws://localhost:8080/ws?room=reports`- A partir de Semana 6, el servicio REST envía `update_report` para cambios en reportes, y `update_user` para cambios en usuarios.

2. Ejecutar `PUT /reportes/{id}` en el REST API

3. Verificar que el cliente WS recibe el evento `update_report`````



---POST http://localhost:8080/notify/{sala}### Ejemplos con `wscat`



### **Test 3: Agregar comentario → Recibir evento**Content-Type: application/json



1. Conectar cliente WebSocket a `ws://localhost:8080/ws?room=reports````bash

2. Ejecutar `POST /comentarios` en el REST API

3. Verificar que el cliente WS recibe el evento `comment_added`{wscat -c ws://localhost:8080/ws?room=reports



---  "event": "new_report",```



**Semana 6** - Sistema de Informes Universidad 🚀    "message": "Nuevo reporte creado desde backend"

**Cumplimiento 100%** con requisitos del docente ✅

}Desde otra terminal:

````

````bash

**Respuesta:**curl -X POST http://localhost:8080/notify/reports \

```json  -H "Content-Type: application/json" \

{  -d '{"event":"update_report","message":"Reporte #42 actualizado"}'

  "status": "ok",```

  "room": "reports"

}### Ejemplos con DevTools (navegador)

````

````js

**Ejemplo con cURL:**const ws = new WebSocket("ws://localhost:8080/ws?room=reports");

```bashws.onmessage = (e) => console.log("WS:", e.data);

curl -X POST http://localhost:8080/notify/reports \// Simular desde REST o curl el envío de eventos a la sala "reports"

  -H "Content-Type: application/json" \```

  -d '{"event":"new_report","message":"Nuevo reporte de prueba"}'
````

---

### **3️⃣ Healthcheck**

```
GET http://localhost:8080/
```

**Respuesta:**

```json
{
  "status": "ok",
  "service": "ws"
}
```

---

## 🔐 Autenticación (Opcional)

Si `WS_REQUIRE_AUTH=1`, el servidor valida JWT en cada conexión.

### **Enviar Token en Header**

```javascript
const ws = new WebSocket("ws://localhost:8080/ws?room=reports", {
  headers: {
    Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  },
});
```

### **Enviar Token en Query Param**

```javascript
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
const ws = new WebSocket(`ws://localhost:8080/ws?room=reports&token=${token}`);
```

---

## 🏷️ Salas (Rooms)

Cada cliente se suscribe a una **sala específica** al conectarse. Los mensajes solo se envían a clientes de la misma sala.

### **Crear Sala**

Las salas se crean automáticamente cuando el primer cliente se conecta:

```javascript
// Cliente 1: Sala "reports"
const ws1 = new WebSocket("ws://localhost:8080/ws?room=reports");

// Cliente 2: Sala "comments"
const ws2 = new WebSocket("ws://localhost:8080/ws?room=comments");

// Cliente 3: Sala "general" (default)
const ws3 = new WebSocket("ws://localhost:8080/ws");
```

### **Broadcast a Sala Específica**

Los mensajes enviados por un cliente solo llegan a clientes de la misma sala:

```javascript
// Cliente en "reports" envía mensaje
ws1.send("new_report");
// Solo clientes en "reports" reciben el evento
```

---

## 🔄 Ping/Pong (Keepalive)

El servidor envía **ping automático cada 30 segundos** para mantener la conexión viva:

- Si el cliente responde con **pong**, la conexión se mantiene activa
- Si no responde en **60 segundos**, la conexión se cierra automáticamente

Esto evita conexiones zombies y asegura que solo clientes activos permanezcan conectados.

---

## 📊 Diagrama de Flujo

```
Cliente               Servidor WebSocket               Backend/API
  |                          |                              |
  |--- ws://host/ws?room=--- >|                              |
  |<--- [Conectado] ----------|                              |
  |                          |<--- POST /notify/reports ----| (Notificar evento)
  |<--- {"event":"new_report"}|                              |
  |--- "update_report" ------>|                              |
  |<--- {"event":"update..."}-|                              |
  |                          |--- ping ----------------------|
  |--- pong ----------------->|                              |
  |                          |                              |
```

---

## 🛠️ Tecnologías

- **Go** 1.21+
- **Gorilla WebSocket** (librería estándar de facto)
- **JWT** (golang-jwt/jwt/v5) para autenticación opcional
- **Rooms/Salas** con sincronización thread-safe (mutex)

---

## 📝 Notas

- ✅ **Salas aisladas**: Los mensajes no cruzan entre salas
- ✅ **Escalable**: Usa channels de Go para broadcast eficiente
- ✅ **Robusto**: Ping/pong automático y manejo de errores
- ✅ **Flexible**: Auth opcional, CORS configurable
- ✅ **Compatible**: Funciona con navegadores modernos, Node.js, wscat, etc.

---

## 🚀 Integración con Frontend

### **React/Vite Ejemplo**

```typescript
import { useEffect, useState } from "react";

export function useWebSocket(room: string) {
  const [messages, setMessages] = useState<any[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(`ws://localhost:8080/ws?room=${room}`);

    socket.onopen = () => console.log("✅ Conectado a sala:", room);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };

    socket.onerror = (error) => console.error("❌ Error WS:", error);

    socket.onclose = () => console.log("🔌 Desconectado");

    setWs(socket);

    return () => socket.close();
  }, [room]);

  const send = (event: string) => {
    ws?.send(event);
  };

  return { messages, send };
}

// Uso:
// const { messages, send } = useWebSocket('reports');
// <button onClick={() => send('new_report')}>Notificar</button>
```

---

**Semana 6** - Equipo Sistema de Informes 🌐
````````
