# 🌐 Servicio WebSocket - Semana 3

**Estudiante:** Jereny Jhonnayker Vera Mero (Integrante 3)  
**Lenguaje:** Go (Golang)  
**Tecnología:** Gorilla WebSocket  
**Fecha:** Semana 3 - Octubre 2025

---

## 📋 Actividades Realizadas - Semana 3

### 🎯 Objetivo de la Semana

Definición del proyecto, diseño de arquitectura, setup inicial del repositorio y elección del componente a desarrollar con Go.

### ✅ Tareas Completadas

1. **Selección de Tecnología**
   - Elegido **Go (Golang)** como lenguaje especializado
   - Seleccionado **Gorilla WebSocket** como framework para WebSockets
   - Decisión de desarrollar el **Servidor WebSocket** para notificaciones en tiempo real

2. **Definición de Arquitectura**
   - Diseño del componente WebSocket como servicio independiente
   - Definición de puerto: **8080**
   - Planificación de integración con REST API y Frontend

3. **Setup Inicial del Proyecto**
   - Creación de carpeta `services/ws/`
   - Inicialización de módulo Go: `go mod init ws-service`
   - Instalación de dependencia Gorilla: `github.com/gorilla/websocket`

4. **Estructura de Archivos Inicial**

   ```
   services/ws/
   ├── main.go          (archivo principal del servidor)
   ├── go.mod           (dependencias del proyecto)
   └── README.md        (este archivo)
   ```

5. **Documentación Inicial**
   - Creación de README.md con descripción del servicio
   - Documentación de requisitos y tecnologías elegidas

---

## 🛠️ Tecnologías Seleccionadas

| Componente       | Tecnología        | Versión |
| ---------------- | ----------------- | ------- |
| **Lenguaje**     | Go                | 1.20+   |
| **Framework WS** | Gorilla WebSocket | latest  |
| **Puerto**       | -                 | 8080    |

---

## � Requisitos del Sistema

- **Go 1.20 o superior**
- **Gorilla WebSocket** (`github.com/gorilla/websocket`)

---

## 🚀 Instalación Inicial

### Paso 1: Inicializar módulo Go

```bash
cd services/ws
go mod init ws-service
```

### Paso 2: Instalar dependencias

```bash
go get github.com/gorilla/websocket
```

### Paso 3: Verificar instalación

```bash
go mod tidy
```

---

## � Diseño Arquitectónico Inicial

### Responsabilidades del Componente WebSocket

- ✅ Gestión de conexiones WebSocket en tiempo real
- ✅ Broadcast de notificaciones a clientes conectados
- ✅ Integración con REST API para recibir eventos
- ✅ Soporte para múltiples clientes simultáneos

### Flujo de Comunicación Planificado

```
REST API → WebSocket Server → Clientes Conectados (Frontend)
```

### Eventos a Implementar (Planificados)

1. `new_report` - Notificación de nuevo reporte creado
2. `update_report` - Notificación de actualización de reporte
3. `comment_added` - Notificación de nuevo comentario
4. `rating_added` - Notificación de nueva puntuación

---

## 🎯 Integración con otros Componentes

### Conexión con REST API (Python/FastAPI)

- El REST API enviará eventos HTTP al WebSocket Server
- Endpoint planificado: `POST /notify`

### Conexión con Frontend (React/TypeScript)

- El Frontend se conectará vía WebSocket
- URL planificada: `ws://localhost:8080/ws`

### Conexión con GraphQL (TypeScript/Apollo)

- Integración indirecta a través de REST API
- No requiere conexión directa

---

## 📝 Notas de Desarrollo

### Decisiones Técnicas

1. **¿Por qué Go?**
   - Alto rendimiento para conexiones concurrentes
   - Excelente soporte para WebSockets
   - Compilación a binario nativo
   - Goroutines para manejo eficiente de conexiones

2. **¿Por qué Gorilla WebSocket?**
   - Biblioteca estándar de facto en Go
   - Completamente compatible con RFC 6455
   - Manejo robusto de errores
   - Documentación extensa

3. **¿Por qué Puerto 8080?**
   - Puerto estándar para servicios alternativos HTTP
   - No conflictúa con REST (8000) ni GraphQL (4000)
   - Fácil de recordar para desarrollo

---

## � Próximos Pasos (Semana 4)

- [ ] Implementar servidor básico WebSocket
- [ ] Crear endpoint `/ws` para conexiones
- [ ] Implementar sistema de broadcast
- [ ] Agregar endpoint HTTP `/notify` para recibir eventos
- [ ] Probar conexiones múltiples
- [ ] Documentar API del servicio

---

## 👤 Información del Desarrollador

**Nombre:** Jereny Jhonnayker Vera Mero  
**Rol:** Integrante 3 - Desarrollador WebSocket  
**Lenguaje Asignado:** Go (Golang)  
**Componente:** Servidor WebSocket para Notificaciones en Tiempo Real

---

## 📚 Referencias

- [Gorilla WebSocket Documentation](https://github.com/gorilla/websocket)
- [Go Official Documentation](https://golang.org/doc/)
- [WebSocket Protocol RFC 6455](https://tools.ietf.org/html/rfc6455)

---

**Semana 3 - Setup Inicial Completado** ✅
