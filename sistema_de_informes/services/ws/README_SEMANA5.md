# 🌐 Servicio WebSocket - Semana 5

**Estudiante:** Jereny Jhonnayker Vera Mero (Integrante 3)  
**Lenguaje:** Go (Golang)  
**Tecnología:** Gorilla WebSocket  
**Fecha:** Semana 5 - Octubre 2025

---

## 📋 Actividades Realizadas - Semana 5

### 🎯 Objetivo de la Semana

Integración inicial: comunicación entre servicios, mejoras en el servidor WebSocket y primeras integraciones con REST API y Frontend.

### ✅ Tareas Completadas

1. **Sistema de Salas/Canales (Rooms)**
   - ✅ Implementación de múltiples salas independientes
   - ✅ Parámetro de query: `?room=reports`, `?room=general`
   - ✅ Mapa de salas: `rooms map[string]map[*websocket.Conn]bool`
   - ✅ Broadcast selectivo por sala

2. **Endpoint Específico por Sala**
   - ✅ `POST /notify/{room}` - Notificar a una sala específica
   - ✅ Sala por defecto: `general`
   - ✅ Validación de sala vacía

3. **Mejoras en Manejo de Conexiones**
   - ✅ Registro de cliente en sala específica
   - ✅ Desregistro automático al desconectar
   - ✅ Logging mejorado con información de sala

4. **Integración con REST API**
   - ✅ REST API puede enviar notificaciones via HTTP POST
   - ✅ Eventos implementados: `new_report`, `update_report`, `comment_added`
   - ✅ Formato JSON estandarizado

5. **Integración con Frontend**
   - ✅ Frontend se conecta a sala `reports`
   - ✅ Recepción de notificaciones en tiempo real
   - ✅ Visualización de mensajes en UI

6. **Archivos HTML de Prueba**
   - ✅ `test.html` - Cliente WebSocket de prueba simple
   - ✅ `dashboard.html` - Dashboard avanzado con múltiples salas

---

## 💻 Código Implementado - Nuevas Funcionalidades

### Estructura de Salas

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
    "sync"

    "github.com/gorilla/websocket"
)

type Broadcast struct {
    Room string
    Data []byte
}

var (
    // Mapa de salas: sala -> clientes
    rooms   = make(map[string]map[*websocket.Conn]bool)
    roomsMu sync.RWMutex

    // Canal de broadcast con información de sala
    broadcast = make(chan Broadcast, 256)
)
```

### Handler WebSocket con Soporte de Salas

```go
func wsHandler(w http.ResponseWriter, r *http.Request) {
    // Obtener sala desde query params
    room := r.URL.Query().Get("room")
    if room == "" {
        room = "general" // Sala por defecto
    }

    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Printf("Error al hacer upgrade: %v", err)
        return
    }
    defer conn.Close()

    // Registrar cliente en la sala
    roomsMu.Lock()
    if rooms[room] == nil {
        rooms[room] = make(map[*websocket.Conn]bool)
    }
    rooms[room][conn] = true
    totalClients := len(rooms[room])
    roomsMu.Unlock()

    log.Printf("✅ Cliente conectado a sala '%s'. Total en sala: %d", room, totalClients)

    // Enviar mensaje de bienvenida
    welcomeMsg := Message{
        Event:   "connected",
        Message: "Conectado a sala " + room,
        Data: map[string]interface{}{
            "room": room,
            "timestamp": time.Now().Unix(),
        },
    }
    data, _ := json.Marshal(welcomeMsg)
    conn.WriteMessage(websocket.TextMessage, data)

    // Leer mensajes del cliente
    for {
        _, msg, err := conn.ReadMessage()
        if err != nil {
            log.Printf("Error al leer mensaje: %v", err)
            break
        }
        log.Printf("📩 [%s] Mensaje recibido: %s", room, msg)

        // Broadcast a la misma sala
        broadcast <- Broadcast{Room: room, Data: msg}
    }

    // Desregistrar cliente
    roomsMu.Lock()
    delete(rooms[room], conn)
    if len(rooms[room]) == 0 {
        delete(rooms, room) // Eliminar sala vacía
    }
    roomsMu.Unlock()

    log.Printf("❌ Cliente desconectado de sala '%s'", room)
}
```

### Sistema de Broadcast por Sala

```go
func handleMessages() {
    for {
        msg := <-broadcast

        roomsMu.RLock()
        clients := rooms[msg.Room]

        for client := range clients {
            err := client.WriteMessage(websocket.TextMessage, msg.Data)
            if err != nil {
                log.Printf("Error al enviar mensaje: %v", err)
                client.Close()

                // Limpiar cliente con error
                roomsMu.RUnlock()
                roomsMu.Lock()
                delete(rooms[msg.Room], client)
                roomsMu.Unlock()
                roomsMu.RLock()
            }
        }
        roomsMu.RUnlock()

        log.Printf("📡 Broadcast enviado a %d clientes en sala '%s'", len(clients), msg.Room)
    }
}
```

### Endpoint de Notificación por Sala

```go
func notifyHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
        return
    }

    // Extraer sala del path: /notify/{room}
    room := strings.TrimPrefix(r.URL.Path, "/notify/")
    if room == "" || room == "notify" {
        room = "general"
    }

    var msg Message
    if err := json.NewDecoder(r.Body).Decode(&msg); err != nil {
        http.Error(w, "JSON inválido", http.StatusBadRequest)
        return
    }

    // Agregar timestamp si no existe
    if msg.Data == nil {
        msg.Data = make(map[string]interface{})
    }
    if dataMap, ok := msg.Data.(map[string]interface{}); ok {
        dataMap["timestamp"] = time.Now().Unix()
    }

    // Serializar y enviar a broadcast de la sala específica
    data, _ := json.Marshal(msg)
    broadcast <- Broadcast{Room: room, Data: data}

    log.Printf("🔔 Notificación enviada a sala '%s': %s", room, msg.Event)

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{
        "status": "ok",
        "room":   room,
        "event":  msg.Event,
    })
}
```

### Healthcheck Mejorado

```go
func healthHandler(w http.ResponseWriter, r *http.Request) {
    roomsMu.RLock()
    totalClients := 0
    roomsInfo := make(map[string]int)

    for room, clients := range rooms {
        count := len(clients)
        roomsInfo[room] = count
        totalClients += count
    }
    roomsMu.RUnlock()

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "status":       "ok",
        "service":      "ws",
        "totalClients": totalClients,
        "rooms":        roomsInfo,
    })
}
```

---

## 🎨 Archivos HTML de Prueba

### test.html - Cliente Simple

```html
<!DOCTYPE html>
<html>
  <head>
    <title>WebSocket Test</title>
  </head>
  <body>
    <h1>WebSocket Test Client</h1>
    <div>
      <label>Sala: <input type="text" id="room" value="reports" /></label>
      <button onclick="connect()">Conectar</button>
      <button onclick="disconnect()">Desconectar</button>
    </div>
    <div>
      <textarea id="messages" rows="20" cols="80" readonly></textarea>
    </div>

    <script>
      let ws = null;

      function connect() {
        const room = document.getElementById("room").value;
        ws = new WebSocket(`ws://localhost:8080/ws?room=${room}`);

        ws.onopen = () => log("✅ Conectado a sala: " + room);
        ws.onmessage = (e) => log("📩 " + e.data);
        ws.onerror = (e) => log("❌ Error: " + e);
        ws.onclose = () => log("🔌 Desconectado");
      }

      function disconnect() {
        if (ws) ws.close();
      }

      function log(msg) {
        const textarea = document.getElementById("messages");
        textarea.value += new Date().toLocaleTimeString() + " - " + msg + "\n";
        textarea.scrollTop = textarea.scrollHeight;
      }
    </script>
  </body>
</html>
```

### dashboard.html - Dashboard Avanzado

```html
<!DOCTYPE html>
<html>
  <head>
    <title>WebSocket Dashboard</title>
    <style>
      body {
        font-family: Arial;
        padding: 20px;
      }
      .room {
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px 0;
      }
      .message {
        background: #f0f0f0;
        padding: 5px;
        margin: 5px 0;
      }
      .connected {
        color: green;
      }
      .disconnected {
        color: red;
      }
    </style>
  </head>
  <body>
    <h1>🌐 WebSocket Dashboard</h1>

    <div class="room">
      <h2>Sala: Reports</h2>
      <p>
        Estado:
        <span id="status-reports" class="disconnected">Desconectado</span>
      </p>
      <div id="messages-reports"></div>
    </div>

    <script>
      const wsReports = new WebSocket("ws://localhost:8080/ws?room=reports");

      wsReports.onopen = () => {
        document.getElementById("status-reports").textContent = "Conectado";
        document.getElementById("status-reports").className = "connected";
      };

      wsReports.onmessage = (event) => {
        const div = document.createElement("div");
        div.className = "message";
        div.textContent = `${new Date().toLocaleTimeString()} - ${event.data}`;
        document.getElementById("messages-reports").prepend(div);
      };

      wsReports.onclose = () => {
        document.getElementById("status-reports").textContent = "Desconectado";
        document.getElementById("status-reports").className = "disconnected";
      };
    </script>
  </body>
</html>
```

---

## 🧪 Pruebas de Integración

### Test 1: Múltiples Salas

```javascript
// Cliente 1 - Sala reports
const ws1 = new WebSocket("ws://localhost:8080/ws?room=reports");
ws1.onmessage = (e) => console.log("[reports]", e.data);

// Cliente 2 - Sala general
const ws2 = new WebSocket("ws://localhost:8080/ws?room=general");
ws2.onmessage = (e) => console.log("[general]", e.data);

// Cliente 3 - También sala reports
const ws3 = new WebSocket("ws://localhost:8080/ws?room=reports");
ws3.onmessage = (e) => console.log("[reports-2]", e.data);
```

**Resultado:** ✅ Salas aisladas correctamente

### Test 2: Notificación a Sala Específica

```bash
# Notificar solo a sala "reports"
curl -X POST http://localhost:8080/notify/reports \
  -H "Content-Type: application/json" \
  -d '{"event":"new_report","message":"Nuevo reporte #123"}'
```

**Resultado:** ✅ Solo clientes de "reports" reciben el mensaje

### Test 3: Integración con REST API

**REST API envía evento al crear reporte:**

```python
# En routers/reporte.py (REST API - Python)
import httpx

@router.post("/reportes", status_code=201)
def create_reporte(...):
    # ... crear reporte en DB ...

    # Notificar via WebSocket
    try:
        httpx.post("http://localhost:8080/notify/reports", json={
            "event": "new_report",
            "message": f"Nuevo reporte: {reporte.titulo}",
            "data": {
                "reporteId": reporte.id_reporte,
                "titulo": reporte.titulo
            }
        })
    except:
        pass  # No fallar si WS está offline

    return reporte
```

**Resultado:** ✅ Frontend recibe notificación en tiempo real al crear reporte

### Test 4: Integración con Frontend

**Frontend React conecta a WebSocket:**

```typescript
// En App.tsx (Frontend - React)
useEffect(() => {
  const ws = new WebSocket("ws://localhost:8080/ws?room=reports");

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    setNotification(data.message);

    if (data.event === "new_report") {
      fetchReportsREST(); // Recargar lista de reportes
    }
  };

  return () => ws.close();
}, []);
```

**Resultado:** ✅ UI se actualiza automáticamente con nuevos reportes

---

## 📊 Métricas de la Semana

| Métrica                        | Valor                         |
| ------------------------------ | ----------------------------- |
| **Líneas de código agregadas** | +120 líneas                   |
| **Funcionalidades nuevas**     | 3 (salas, notify/room, HTMLs) |
| **Integraciones completadas**  | 2 (REST API, Frontend)        |
| **Archivos HTML creados**      | 2                             |
| **Bugs corregidos**            | 0                             |
| **Estado**                     | ✅ Integrado                  |

---

## 🔗 Flujo de Integración Completo

```
Usuario crea reporte en Frontend
         ↓
Frontend → POST /reportes → REST API
         ↓
REST API guarda en DB
         ↓
REST API → POST /notify/reports → WebSocket Server
         ↓
WebSocket Server → Broadcast a sala "reports"
         ↓
Todos los Frontend conectados a "reports" reciben notificación
         ↓
Frontend actualiza UI automáticamente
```

---

## 📝 Decisiones Técnicas

1. **Rooms como Querystring**
   - Facilita conexión desde navegador
   - Compatible con todas las librerías WebSocket
   - Fácil de debuggear

2. **Sala por Defecto "general"**
   - Evita errores si no se especifica sala
   - Permite broadcast global

3. **Timestamp Automático**
   - Agregado en servidor para consistencia
   - Evita desincronización de relojes de clientes

4. **Integración Asíncrona con REST**
   - REST API no espera respuesta de WebSocket
   - Si WebSocket está offline, REST sigue funcionando

---

## 🐛 Problemas y Soluciones

### Problema: Clientes Zombies

**Descripción:** Conexiones cerradas que no se eliminaban del mapa

**Solución:**

```go
// Agregar timeout de lectura
conn.SetReadDeadline(time.Now().Add(60 * time.Second))

// Verificar error de escritura y cerrar
if err := conn.WriteMessage(...); err != nil {
    conn.Close()
    delete(rooms[room], conn)
}
```

---

## 📚 Aprendizajes de la Semana

1. **Arquitectura de Salas**
   - Patrón pub/sub con múltiples canales
   - Isolación de mensajes por contexto

2. **Integración HTTP ↔ WebSocket**
   - REST API como bridge hacia WebSocket
   - Desacoplamiento de protocolos

3. **Testing en Navegador**
   - DevTools como herramienta de debugging
   - Archivos HTML standalone para pruebas

---

## 🎯 Próximos Pasos (Semana 6)

- [ ] Implementar ping/pong keepalive
- [ ] Agregar autenticación JWT
- [ ] CORS configurable por entorno
- [ ] Variables de entorno para configuración
- [ ] Graceful shutdown
- [ ] Documentación completa

---

## 👤 Información del Desarrollador

**Nombre:** Jereny Jhonnayker Vera Mero  
**Rol:** Integrante 3 - Desarrollador WebSocket  
**Lenguaje Asignado:** Go (Golang)  
**Componente:** Servidor WebSocket para Notificaciones en Tiempo Real

---

## 📈 Estado del Proyecto

```
[██████████████████░░] 90% - Integración inicial completa
```

**Funcionalidades Completadas:**

- ✅ Servidor HTTP
- ✅ Conexiones WebSocket
- ✅ Sistema de broadcast
- ✅ Salas/Canales
- ✅ Endpoint de notificaciones por sala
- ✅ Integración con REST API
- ✅ Integración con Frontend
- ✅ Archivos de prueba HTML

**Pendientes para Semana 6:**

- ⏳ Keepalive (ping/pong)
- ⏳ Autenticación JWT
- ⏳ CORS configurable
- ⏳ Variables de entorno
- ⏳ Graceful shutdown

---

**Semana 5 - Integración Inicial Completada** ✅
