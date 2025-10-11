# Sistema de Reportes de Infraestructura Universitaria

## Desarrollo Semana 4 - Commit 2

### Integrante Responsable
**Vera Mero Jereny Jhonnayker** (Integrante 3 - Golang)

---

## 🎯 Componente Desarrollado

Implementación del **Servidor WebSocket** utilizando Golang para manejar comunicaciones en tiempo real del sistema de reportes de infraestructura universitaria.

## 📁 Estructura Creada

```
sistema_de_informes/
└── services/
    └── ws/           # Servidor WebSocket
        ├── main.go   # Código principal
        ├── go.mod    # Configuración del módulo
        └── go.sum    # Dependencias verificadas
```

## 🛠️ Proceso de Desarrollo Realizado

### Pasos Realizados por Vera Mero Jereny Jhonnayker:

#### 1. **Configuración del Proyecto Go**
- Creación del archivo `go.mod` para gestionar dependencias
- Instalación de la librería `github.com/gorilla/websocket v1.5.3`

#### 2. **Implementación del Servidor WebSocket**
- **Archivo**: `main.go` 
- **Puerto**: 8080
- **Endpoint**: `/ws`
- **Funcionalidades**:
  - ✅ Gestión de múltiples clientes
  - ✅ Sistema de broadcast de mensajes
  - ✅ Logs de conexión/desconexión
  - ✅ Función echo para pruebas

#### 3. **Pruebas Realizadas**
- Servidor ejecutándose correctamente
- Conexión verificada desde herramientas externas
- Sistema de mensajes funcionando

## 🧪 Cómo Probar

```bash
cd sistema_de_informes/services/ws
go run main.go
```

**Salida esperada**: `Servidor WebSocket iniciado en :8080`

**Para probar**: Conectarse a `ws://localhost:8080/ws` usando [PieSocket WebSocket Tester](https://www.piesocket.com/websocket-tester)

## 📋 Resultado

✅ **Servidor WebSocket funcional** implementado por **Vera Mero Jereny Jhonnayker** (Integrante 3) para comunicaciones en tiempo real del sistema de reportes universitarios.

---

**Fecha**: 11 de octubre de 2025  
**Commit**: `feat(ws): implementación inicial del servidor WebSocket - Semana 4`