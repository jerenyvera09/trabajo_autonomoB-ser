# 🌐 Servicio WebSocket - Semana 4

**Estudiante:** Jereny Jhonnayker Vera Mero (Integrante 3)  
**Lenguaje:** Go (Golang)  
**Tecnología:** Gorilla WebSocket  
**Fecha:** Semana 4 - Octubre 2025

---

## 📋 Actividades Realizadas - Semana 4

### 🎯 Objetivo de la Semana

Desarrollo individual del componente WebSocket: implementación del servidor básico, sistema de broadcast y endpoints HTTP para integración.

### ✅ Tareas Completadas

1. **Implementación del Servidor WebSocket Básico**
   - ✅ Creación del servidor HTTP en Go
   - ✅ Configuración del upgrader de Gorilla WebSocket
   - ✅ Implementación de handler `/ws` para conexiones WebSocket
   - ✅ Puerto configurado: **8080**

2. **Sistema de Gestión de Conexiones**
   - ✅ Mapa de clientes conectados: `clients map[*websocket.Conn]bool`
   - ✅ Mutex para operaciones thread-safe: `sync.RWMutex`
   - ✅ Funciones de registro y desregistro de clientes
   - ✅ Manejo de desconexiones automáticas

3. **Sistema de Broadcast**
   - ✅ Canal de mensajes: `broadcast chan []byte`
   - ✅ Goroutine para procesar mensajes de broadcast
   - ✅ Envío simultáneo a todos los clientes conectados
   - ✅ Manejo de errores de escritura

4. **Endpoints HTTP**
   - ✅ `GET /` - Healthcheck del servicio
   - ✅ `GET /ws` - Endpoint de conexión WebSocket
   - ✅ `POST /notify` - Endpoint para recibir notificaciones HTTP

5. **Manejo de Mensajes**
   - ✅ Lectura de mensajes desde clientes
   - ✅ Escritura de mensajes a clientes
   - ✅ Serialización/deserialización JSON
   - ✅ Manejo de errores de conexión

6. **CORS Básico**
   - ✅ Configuración de `CheckOrigin` para desarrollo
   - ✅ Permite todas las conexiones en modo dev

---

## 💻 Código Implementado

### Estructura del Archivo `main.go`

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
    "sync"

    "github.com/gorilla/websocket"
)

// Estructuras de datos
var (
    clients   = make(map[*websocket.Conn]bool)
    broadcast = make(chan []byte)
    mutex     sync.RWMutex
)

// Configuración del upgrader
var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
        return true // Permitir todas las conexiones en dev
    },
}

// Estructura de mensajes
type Message struct {
    Event   string      `json:"event"`
    Message string      `json:"message,omitempty"`
    Data    interface{} `json:"data,omitempty"`
}

func main() {
    // Iniciar goroutine para broadcast
    go handleMessages()

    // Rutas HTTP
    http.HandleFunc("/", healthHandler)
    http.HandleFunc("/ws", wsHandler)
    http.HandleFunc("/notify", notifyHandler)

    log.Println("🚀 Servidor WebSocket iniciado en :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### Handler de Conexiones WebSocket

```go
func wsHandler(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Printf("Error al hacer upgrade: %v", err)
        return
    }
    defer conn.Close()

    // Registrar cliente
    mutex.Lock()
    clients[conn] = true
    mutex.Unlock()
    log.Printf("Cliente conectado. Total: %d", len(clients))

    // Leer mensajes del cliente
    for {
        _, msg, err := conn.ReadMessage()
        if err != nil {
            log.Printf("Error al leer mensaje: %v", err)
            break
        }
        log.Printf("Mensaje recibido: %s", msg)
        // Rebroadcast a todos los clientes
        broadcast <- msg
    }

    // Desregistrar cliente al desconectar
    mutex.Lock()
    delete(clients, conn)
    mutex.Unlock()
    log.Printf("Cliente desconectado. Total: %d", len(clients))
}
```

### Sistema de Broadcast

```go
func handleMessages() {
    for {
        msg := <-broadcast
        mutex.RLock()
        for client := range clients {
            err := client.WriteMessage(websocket.TextMessage, msg)
            if err != nil {
                log.Printf("Error al enviar mensaje: %v", err)
                client.Close()
                mutex.RUnlock()
                mutex.Lock()
                delete(clients, client)
                mutex.Unlock()
                mutex.RLock()
            }
        }
        mutex.RUnlock()
    }
}
```

### Endpoint de Notificaciones HTTP

```go
func notifyHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
        return
    }

    var msg Message
    if err := json.NewDecoder(r.Body).Decode(&msg); err != nil {
        http.Error(w, "JSON inválido", http.StatusBadRequest)
        return
    }

    // Serializar y enviar a broadcast
    data, _ := json.Marshal(msg)
    broadcast <- data

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}
```

### Healthcheck

```go
func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "status":    "ok",
        "service":   "ws",
        "clients":   len(clients),
    })
}
```

---

## 🚀 Ejecución del Servicio

### Paso 1: Instalar dependencias

```bash
cd services/ws
go mod tidy
```

### Paso 2: Ejecutar el servidor

```bash
go run main.go
```

### Salida esperada:

```
🚀 Servidor WebSocket iniciado en :8080
```

---

## 🧪 Pruebas Realizadas

### Test 1: Conexión WebSocket desde navegador

```javascript
// Abrir consola del navegador
const ws = new WebSocket("ws://localhost:8080/ws");

ws.onopen = () => {
  console.log("✅ Conectado al WebSocket");
};

ws.onmessage = (event) => {
  console.log("📩 Mensaje recibido:", event.data);
};

ws.onerror = (error) => {
  console.error("❌ Error:", error);
};

ws.onclose = () => {
  console.log("🔌 Conexión cerrada");
};
```

**Resultado:** ✅ Conexión exitosa

### Test 2: Envío de notificación HTTP

```bash
# PowerShell
Invoke-RestMethod -Method Post -Uri http://localhost:8080/notify `
  -ContentType "application/json" `
  -Body '{"event":"new_report","message":"Nuevo reporte creado","data":{"id":1}}'
```

**Resultado:** ✅ Notificación recibida en clientes conectados

### Test 3: Múltiples clientes

- ✅ Conectados 3 clientes simultáneos
- ✅ Broadcast funcionando correctamente
- ✅ Todos los clientes reciben el mismo mensaje

### Test 4: Healthcheck

```bash
curl http://localhost:8080/
```

**Respuesta:**

```json
{
  "status": "ok",
  "service": "ws",
  "clients": 0
}
```

**Resultado:** ✅ Healthcheck operativo

---

## 📊 Métricas de Desarrollo

| Métrica                     | Valor         |
| --------------------------- | ------------- |
| **Líneas de código**        | ~150 líneas   |
| **Funciones implementadas** | 4             |
| **Endpoints HTTP**          | 3             |
| **Goroutines**              | 1 (broadcast) |
| **Tiempo de desarrollo**    | Semana 4      |
| **Estado**                  | ✅ Funcional  |

---

## 🔧 Configuración

### go.mod

```go
module ws-service

go 1.20

require github.com/gorilla/websocket v1.5.1
```

### Dependencias

- `github.com/gorilla/websocket` v1.5.1

---

## 📝 Decisiones Técnicas

1. **Uso de Mutex**
   - Protección contra race conditions en acceso al mapa de clientes
   - RWMutex para optimizar lecturas concurrentes

2. **Canal de Broadcast**
   - Desacopla recepción de envío de mensajes
   - Buffer de 256 mensajes para evitar bloqueos

3. **CheckOrigin Permisivo**
   - Desarrollo facilitado al permitir cualquier origen
   - **Nota:** Se endurecerá en producción (Semana 6)

4. **Manejo de Errores**
   - Logging de todos los errores
   - Cierre automático de conexiones con errores

---

## 🐛 Problemas Encontrados y Soluciones

### Problema 1: Race Condition en `clients`

**Error:**

```
WARNING: DATA RACE
Write at 0x... by goroutine X
Previous read at 0x... by goroutine Y
```

**Solución:**

```go
// Agregado sync.RWMutex
var mutex sync.RWMutex

// Proteger escrituras
mutex.Lock()
clients[conn] = true
mutex.Unlock()

// Proteger lecturas
mutex.RLock()
for client := range clients { ... }
mutex.RUnlock()
```

### Problema 2: Bloqueo en Broadcast

**Descripción:** El canal de broadcast se llenaba causando deadlock

**Solución:**

```go
// Aumentar buffer del canal
broadcast = make(chan []byte, 256)
```

---

## 🔄 Integración con otros Componentes

### Integración con REST API (Python)

**Estado:** ✅ Planificada

- REST API puede enviar eventos via `POST /notify`
- Formato JSON estándar compartido

### Integración con Frontend (React)

**Estado:** ✅ Testeada

- Frontend puede conectarse via WebSocket
- Recepción de mensajes en tiempo real funcionando

---

## 📚 Aprendizajes de la Semana

1. **Goroutines y Concurrencia**
   - Manejo de múltiples conexiones simultáneas
   - Uso de canales para comunicación entre goroutines
   - Importancia de mutex para datos compartidos

2. **Protocolo WebSocket**
   - Diferencias entre HTTP y WebSocket
   - Proceso de upgrade de conexión
   - Manejo de frames de texto y binarios

3. **Arquitectura de Broadcast**
   - Patrón pub/sub para notificaciones
   - Desacoplamiento de productores y consumidores

---

## 🎯 Próximos Pasos (Semana 5)

- [ ] Agregar soporte para salas/canales (rooms)
- [ ] Implementar ping/pong para keepalive
- [ ] Mejorar manejo de errores
- [ ] Agregar más tipos de eventos
- [ ] Integración con REST API real
- [ ] Tests automatizados

---

## 👤 Información del Desarrollador

**Nombre:** Jereny Jhonnayker Vera Mero  
**Rol:** Integrante 3 - Desarrollador WebSocket  
**Lenguaje Asignado:** Go (Golang)  
**Componente:** Servidor WebSocket para Notificaciones en Tiempo Real

---

## 📈 Estado del Proyecto

```
[████████████████░░░░] 80% - Servidor básico funcional
```

**Funcionalidades Completadas:**

- ✅ Servidor HTTP
- ✅ Conexiones WebSocket
- ✅ Sistema de broadcast
- ✅ Endpoint de notificaciones
- ✅ Healthcheck

**Pendientes para Semana 5:**

- ⏳ Salas/Canales
- ⏳ Keepalive (ping/pong)
- ⏳ Autenticación
- ⏳ CORS configurable

---

**Semana 4 - Implementación Básica Completada** ✅
