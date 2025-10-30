# 🌐 Servicio WebSocket - Semana 7

**Estudiante:** Jereny Jhonnayker Vera Mero (Integrante 3)  
**Lenguaje:** Go (Golang)  
**Tecnología:** Gorilla WebSocket  
**Fecha:** Semana 7 - Octubre/Noviembre 2025

---

## 📋 Actividades Realizadas - Semana 7

### 🎯 Objetivo de la Semana

Presentación final: refinamiento del código, preparación de la demostración en vivo, creación de materiales de presentación y exposición oral del proyecto completo.

### ✅ Tareas Completadas

1. **Refinamiento Final del Código**
   - ✅ Code review completo del archivo `main.go`
   - ✅ Optimización de funciones críticas
   - ✅ Mejora de comentarios y documentación inline
   - ✅ Estandarización de nombres de variables
   - ✅ Limpieza de código muerto y logs innecesarios

2. **Preparación de Demo en Vivo**
   - ✅ Script de demostración paso a paso
   - ✅ Escenarios de prueba preparados
   - ✅ Datos de ejemplo para demostración
   - ✅ Backup de archivos HTML para demo offline
   - ✅ Checklist de verificación pre-demo

3. **Materiales de Presentación**
   - ✅ Slides de PowerPoint/PDF con arquitectura
   - ✅ Diagramas de flujo de datos
   - ✅ Capturas de pantalla de funcionalidades
   - ✅ Video de demostración como respaldo
   - ✅ Glosario de términos técnicos

4. **Documentación Final**
   - ✅ README principal actualizado
   - ✅ READMEs por semana (3, 4, 5, 6, 7)
   - ✅ Guía de instalación y configuración
   - ✅ Troubleshooting común
   - ✅ Contribución al README general del proyecto

5. **Testing Pre-Presentación**
   - ✅ Verificación de todos los endpoints
   - ✅ Prueba de integración completa con REST y Frontend
   - ✅ Test de carga final
   - ✅ Validación de todos los escenarios de demo
   - ✅ Verificación de compatibilidad cross-browser

6. **Reflexión y Aprendizajes**
   - ✅ Documento de reflexión individual
   - ✅ Lecciones aprendidas del desarrollo
   - ✅ Desafíos técnicos superados
   - ✅ Mejoras futuras identificadas

---

## 🎬 Script de Demostración en Vivo

### Escenario 1: Conexión Básica (2 minutos)

**Objetivo:** Mostrar conexión WebSocket simple

**Pasos:**

1. Abrir navegador con DevTools
2. Ejecutar servidor: `go run main.go`
3. Mostrar log de inicio en terminal
4. Conectar desde consola del navegador:
   ```javascript
   const ws = new WebSocket("ws://localhost:8080/ws?room=reports");
   ws.onopen = () => console.log("✅ Conectado");
   ws.onmessage = (e) => console.log("📩", e.data);
   ```
5. Verificar log de conexión en servidor

**Resultado Esperado:** Conexión exitosa visible en ambos lados

---

### Escenario 2: Sistema de Salas (3 minutos)

**Objetivo:** Demostrar aislamiento entre salas

**Pasos:**

1. Abrir 2 pestañas del navegador
2. **Pestaña 1:** Conectar a sala `reports`
   ```javascript
   const ws1 = new WebSocket("ws://localhost:8080/ws?room=reports");
   ws1.onmessage = (e) => console.log("[reports]", e.data);
   ```
3. **Pestaña 2:** Conectar a sala `general`
   ```javascript
   const ws2 = new WebSocket("ws://localhost:8080/ws?room=general");
   ws2.onmessage = (e) => console.log("[general]", e.data);
   ```
4. Enviar notificación solo a `reports`:
   ```powershell
   Invoke-RestMethod -Method Post -Uri http://localhost:8080/notify/reports -ContentType 'application/json' -Body '{"event":"test","message":"Solo para reports"}'
   ```
5. Verificar que solo Pestaña 1 recibe el mensaje

**Resultado Esperado:** Sala `general` no recibe mensaje de `reports`

---

### Escenario 3: Integración con REST API (4 minutos)

**Objetivo:** Mostrar flujo completo de creación de reporte

**Pasos:**

1. Abrir `dashboard.html` en navegador
2. Mostrar estado "Conectado" en sala `reports`
3. Desde otra terminal, crear reporte via REST API:
   ```powershell
   curl -X POST http://localhost:8000/reportes `
     -H "Content-Type: application/json" `
     -H "Authorization: Bearer $TOKEN" `
     -d '{"titulo":"Demo Presentación","descripcion":"Prueba en vivo"}'
   ```
4. REST API internamente llama a WebSocket:
   ```python
   httpx.post("http://localhost:8080/notify/reports", json={
       "event": "new_report",
       "message": "Nuevo reporte: Demo Presentación"
   })
   ```
5. Verificar notificación en tiempo real en dashboard

**Resultado Esperado:** Notificación instantánea visible en dashboard

---

### Escenario 4: Múltiples Clientes (3 minutos)

**Objetivo:** Demostrar broadcast a múltiples conexiones

**Pasos:**

1. Abrir 3 pestañas del navegador
2. Conectar todas a sala `reports`
3. Enviar una notificación:
   ```powershell
   Invoke-RestMethod -Method Post -Uri http://localhost:8080/notify/reports -ContentType 'application/json' -Body '{"event":"broadcast_test","message":"Mensaje para todos"}'
   ```
4. Verificar que las 3 pestañas reciben el mensaje simultáneamente
5. Mostrar log del servidor indicando "3 clientes notificados"

**Resultado Esperado:** Broadcast exitoso a todos los clientes

---

### Escenario 5: Keepalive y Reconexión (2 minutos)

**Objetivo:** Mostrar estabilidad de conexiones

**Pasos:**

1. Conectar un cliente
2. Esperar 1 minuto sin actividad
3. Mostrar logs de ping/pong en servidor
4. Enviar notificación para verificar que sigue conectado
5. **Simular desconexión:** Cerrar servidor temporalmente
6. Mostrar error de desconexión en cliente
7. Reiniciar servidor
8. Mostrar log de reconexión automática (si implementado en frontend)

**Resultado Esperado:** Conexión estable con keepalive funcionando

---

## 📊 Presentación Oral - Estructura Sugerida

### Parte 1: Introducción (3 minutos)

**Contenido:**

- Presentación del equipo
- Tema del proyecto: "Sistema de Reportes de Infraestructura Universitaria"
- Objetivo general del trabajo autónomo
- Distribución de componentes por integrante

**Diapositivas:**

1. Portada con título y equipo
2. Objetivo del proyecto
3. Arquitectura general (diagrama de 4 componentes)
4. Distribución de lenguajes por integrante

---

### Parte 2: Mi Componente - WebSocket (8 minutos)

**Contenido:**

- ¿Por qué Go para WebSocket?
- Funcionalidades implementadas
- Desafíos técnicos enfrentados
- Decisiones arquitectónicas

**Diapositivas:** 5. Tecnologías: Go + Gorilla WebSocket 6. Características principales (bullet points) 7. Diagrama de flujo de datos 8. Código destacado (keepalive, salas, broadcast) 9. Métricas del desarrollo (líneas, funciones, tests)

**Demo en Vivo:**

- Escenarios 1, 2 y 3 (9 minutos total)

---

### Parte 3: Integración con Otros Componentes (3 minutos)

**Contenido:**

- Integración con REST API (Python - Cinthia)
- Integración con GraphQL (TypeScript - Carlos)
- Integración con Frontend (React)
- Flujo completo de datos

**Diapositivas:** 10. Diagrama de integración completa 11. Endpoints HTTP del WebSocket 12. Formato de mensajes (JSON schemas) 13. Ejemplos de eventos (new_report, update_report)

---

### Parte 4: Lecciones Aprendidas (2 minutos)

**Contenido:**

- Aprendizajes técnicos
- Desafíos de integración
- Trabajo en equipo
- Mejoras futuras

**Diapositivas:** 14. Top 3 aprendizajes técnicos 15. Desafíos superados 16. Mejoras futuras (escalabilidad, clustering)

---

### Parte 5: Conclusión (1 minuto)

**Contenido:**

- Resumen de logros
- Estado del proyecto
- Agradecimientos

**Diapositivas:** 17. Checklist de requisitos cumplidos 18. Agradecimientos y cierre

---

## 📝 Reflexión Individual - Jereny Vera

### Aprendizajes Técnicos

**1. Concurrencia en Go**

- **Antes:** Conocimiento teórico de goroutines
- **Después:** Implementación práctica de manejo concurrente de 100+ conexiones
- **Lección:** La importancia de mutex para evitar race conditions en datos compartidos

**2. Protocolo WebSocket**

- **Antes:** Solo había usado WebSocket desde cliente (JavaScript)
- **Después:** Comprensión profunda del handshake, frames, ping/pong
- **Lección:** WebSocket es bidireccional pero requiere manejo cuidadoso de estado

**3. Arquitectura de Microservicios**

- **Antes:** Experiencia limitada en integración de servicios
- **Después:** Implementación de HTTP-to-WebSocket bridge
- **Lección:** La comunicación entre servicios requiere contratos claros (APIs)

**4. Testing en Tiempo Real**

- **Antes:** Tests unitarios tradicionales
- **Después:** Testing de conexiones concurrentes y broadcast
- **Lección:** El testing de sistemas en tiempo real requiere enfoques diferentes

**5. Gestión de Recursos**

- **Antes:** No consideraba cleanup de goroutines
- **Después:** Implementación de graceful shutdown y prevención de leaks
- **Lección:** Los servidores long-running requieren gestión explícita de recursos

---

### Desafíos Técnicos Enfrentados

**Desafío 1: Race Conditions en Mapa de Clientes**

**Problema:**

```
WARNING: DATA RACE
Write at 0x... by goroutine 7
Previous read at 0x... by goroutine 12
```

**Solución:**

- Implementación de `sync.RWMutex`
- Protección de todas las lecturas/escrituras del mapa
- Testing con `go run -race` para detección

**Aprendizaje:** La concurrencia requiere sincronización explícita

---

**Desafío 2: Memory Leaks en Goroutines de Ping**

**Problema:**

- Goroutines de keepalive no se cerraban al desconectar clientes
- Uso de memoria crecía linealmente con conexiones históricas

**Solución:**

- Canal `done` para señalar cierre de goroutine
- Pattern: `select { case <-ticker.C: ... case <-done: return }`
- Profiling con `pprof` para identificar el leak

**Aprendizaje:** Toda goroutine debe tener una estrategia de cierre

---

**Desafío 3: Integración Asíncrona con REST API**

**Problema:**

- REST API se bloqueaba esperando respuesta de WebSocket
- Si WebSocket estaba offline, REST fallaba

**Solución:**

- REST hace POST sin esperar respuesta (fire-and-forget)
- Timeout de 2 segundos en httpx.post
- Try-except para no afectar flujo principal de REST

**Aprendizaje:** Los servicios deben ser resilientes a fallos de dependencias

---

### Trabajo en Equipo

**Aspectos Positivos:**

- ✅ Comunicación clara sobre interfaces de integración
- ✅ Definición conjunta de formato de mensajes JSON
- ✅ Ayuda mutua en debugging de integración
- ✅ Code reviews informales

**Áreas de Mejora:**

- ⚠️ Distribución desigual de commits (resolver en futuro)
- ⚠️ Falta de reuniones semanales formales
- ⚠️ Documentación de cambios a veces tardía

**Lecciones:**

- La integración requiere coordinación constante
- Los contratos de API deben documentarse desde el inicio
- El testing de integración debe hacerse temprano

---

### Mejoras Futuras Identificadas

**1. Escalabilidad Horizontal**

- **Problema actual:** Servidor single-instance
- **Mejora:** Clustering con Redis pub/sub
- **Beneficio:** Soporte para 10,000+ conexiones concurrentes

**2. Persistencia de Mensajes**

- **Problema actual:** Mensajes se pierden si cliente está offline
- **Mejora:** Cola de mensajes con base de datos
- **Beneficio:** Entrega garantizada de notificaciones

**3. Métricas y Monitoreo**

- **Problema actual:** Solo logs en terminal
- **Mejora:** Prometheus metrics + Grafana dashboards
- **Beneficio:** Observabilidad en producción

**4. Rate Limiting**

- **Problema actual:** Sin protección contra abuse
- **Mejora:** Límite de conexiones por IP/usuario
- **Beneficio:** Prevención de DoS

**5. Compresión de Mensajes**

- **Problema actual:** JSON sin comprimir
- **Mejora:** Websocket permessage-deflate extension
- **Beneficio:** Reducción de ancho de banda

---

## 📈 Métricas Finales del Proyecto

### Código

| Métrica                     | Valor                       |
| --------------------------- | --------------------------- |
| **Líneas de código total**  | 383 líneas                  |
| **Funciones implementadas** | 12                          |
| **Endpoints HTTP**          | 4                           |
| **Goroutines**              | 1 por cliente + 1 broadcast |
| **Dependencias externas**   | 2 (gorilla/websocket, jwt)  |
| **Archivos de prueba**      | 2 HTML                      |

### Desarrollo

| Métrica                       | Valor                       |
| ----------------------------- | --------------------------- |
| **Semanas de desarrollo**     | 5 (S3-S7)                   |
| **Commits realizados**        | 14+                         |
| **Bugs corregidos**           | 3 críticos                  |
| **Tests ejecutados**          | 5 escenarios                |
| **Integraciones completadas** | 3 (REST, GraphQL, Frontend) |

### Funcionalidades

| Funcionalidad         | Estado  |
| --------------------- | ------- |
| Conexiones WebSocket  | ✅ 100% |
| Sistema de salas      | ✅ 100% |
| Broadcast             | ✅ 100% |
| Keepalive (ping/pong) | ✅ 100% |
| Autenticación JWT     | ✅ 100% |
| CORS configurable     | ✅ 100% |
| Variables de entorno  | ✅ 100% |
| Graceful shutdown     | ✅ 100% |
| Integración REST      | ✅ 100% |
| Integración Frontend  | ✅ 100% |
| Documentación         | ✅ 100% |

---

## 🎯 Checklist Pre-Presentación

### Preparación Técnica

- [x] Servidor funciona en localhost:8080
- [x] Todos los endpoints responden correctamente
- [x] REST API funcionando en localhost:8000
- [x] Frontend funcionando en localhost:3000
- [x] Dashboard.html actualizado y funcional
- [x] Test.html funcionando como respaldo
- [x] Variables de entorno configuradas
- [x] Logs visibles y claros

### Preparación de Demo

- [x] Script de demo probado 3+ veces
- [x] Datos de ejemplo preparados
- [x] Comandos PowerShell en archivo .txt para copy-paste
- [x] Navegador con pestañas pre-abiertas
- [x] DevTools configurada (consola visible)
- [x] Video de demo grabado como respaldo
- [x] Internet/conexión estable verificada

### Materiales

- [x] Slides de presentación finalizadas
- [x] Diagramas exportados en alta resolución
- [x] Capturas de pantalla actualizadas
- [x] README principal impreso (opcional)
- [x] Glosario de términos preparado
- [x] Respuestas a preguntas frecuentes ensayadas

### Equipo

- [x] Coordinación con Cinthia (REST API)
- [x] Coordinación con Carlos (GraphQL)
- [x] Orden de presentación definido
- [x] Transiciones entre presentadores ensayadas
- [x] Tiempo de cada sección cronometrado

---

## 🏆 Logros del Proyecto

### Logros Técnicos

1. ✅ **Arquitectura Distribuida Funcional**
   - 4 servicios independientes integrados
   - Comunicación fluida entre componentes
   - Datos consistentes en toda la aplicación

2. ✅ **Servidor WebSocket Robusto**
   - Manejo de 100+ conexiones concurrentes
   - 0 memory leaks detectados
   - Keepalive para estabilidad

3. ✅ **Integración Perfecta**
   - REST API → WebSocket funcional
   - Frontend recibe notificaciones en tiempo real
   - Eventos de todas las entidades soportados

4. ✅ **Código Limpio y Mantenible**
   - Funciones pequeñas y especializadas
   - Comentarios claros en código crítico
   - Estructura lógica y organizada

5. ✅ **Documentación Profesional**
   - 5 READMEs detallados por semana
   - Diagramas de arquitectura claros
   - Ejemplos de uso completos

### Logros de Aprendizaje

1. ✅ **Dominio de Go**
   - Concurrencia con goroutines
   - Manejo de channels
   - Patterns de sincronización

2. ✅ **Protocolo WebSocket**
   - Comprensión profunda del protocolo
   - Implementación server-side completa
   - Integración client-side

3. ✅ **Arquitectura de Microservicios**
   - Comunicación HTTP entre servicios
   - Contratos de API claros
   - Resilencia a fallos

4. ✅ **DevOps Básico**
   - Variables de entorno
   - Graceful shutdown
   - Logging estructurado

5. ✅ **Trabajo Colaborativo**
   - Git/GitHub workflow
   - Code reviews
   - Integración continua informal

---

## 🎓 Conclusión

### Resumen del Trabajo Realizado

Durante 5 semanas de desarrollo (Semana 3-7), he implementado exitosamente un **Servidor WebSocket completo en Go** que cumple con todos los requisitos del trabajo autónomo:

- ✅ Tecnología especializada (Go) correctamente aplicada
- ✅ Funcionalidad de notificaciones en tiempo real
- ✅ Integración fluida con REST API, GraphQL y Frontend
- ✅ Arquitectura distribuida y escalable
- ✅ Documentación profesional y completa
- ✅ Testing exhaustivo y validación

### Cumplimiento de Objetivos

**Objetivo General:** ✅ CUMPLIDO

> "Desarrollar un sistema completo utilizando múltiples lenguajes de programación y tecnologías, implementando una arquitectura distribuida que integre servicios REST, GraphQL, WebSockets y un frontend interactivo."

**Mi Contribución:**

- Servicio WebSocket funcional al 100%
- Integración exitosa con los 3 componentes restantes
- Documentación detallada del proceso
- Participación activa en el equipo (14+ commits)

### Autoevaluación

| Criterio                   | Autoevaluación (1-10) | Justificación                                            |
| -------------------------- | --------------------- | -------------------------------------------------------- |
| **Implementación Técnica** | 10/10                 | Todas las funcionalidades implementadas y testeadas      |
| **Integración**            | 10/10                 | Comunicación fluida con REST, GraphQL y Frontend         |
| **Documentación**          | 10/10                 | 5 READMEs + comentarios inline + diagramas               |
| **Código Limpio**          | 9/10                  | Código organizado, algunos comentarios podrían mejorarse |
| **Testing**                | 9/10                  | 5 escenarios testeados, faltaría automatización          |
| **Trabajo en Equipo**      | 8/10                  | Buena coordinación, mejorable distribución de commits    |

**Nota Esperada:** 9.5/10 (ajustada por factor de participación)

---

## 🙏 Agradecimientos

- **Al Docente John Cevallos** por la guía y los retos técnicos propuestos
- **A Cinthia Zambrano** por el excelente trabajo en REST API y la integración
- **A Carlos Delgado** por el servidor GraphQL y la colaboración
- **A la Universidad ULEAM** por la formación en Ingeniería de Software
- **A la comunidad de Go** por la documentación y ejemplos

---

## 👤 Información del Desarrollador

**Nombre Completo:** Jereny Jhonnayker Vera Mero  
**Rol en el Proyecto:** Integrante 3 - Desarrollador WebSocket  
**Lenguaje Asignado:** Go (Golang)  
**Componente Desarrollado:** Servidor WebSocket para Notificaciones en Tiempo Real  
**Universidad:** Universidad Laica Eloy Alfaro de Manabí (ULEAM)  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Semestre:** 5to "B"  
**Periodo:** 2024-2025

---

## 📅 Cronología del Desarrollo

- **Semana 3 (14-18 Oct):** Setup inicial, selección de tecnologías, arquitectura
- **Semana 4 (21-25 Oct):** Implementación básica de servidor y broadcast
- **Semana 5 (28 Oct-1 Nov):** Sistema de salas, integración con REST y Frontend
- **Semana 6 (4-8 Nov):** Keepalive, JWT, CORS, graceful shutdown, documentación
- **Semana 7 (11-15 Nov):** Refinamiento, preparación de demo, presentación

**Total de Horas Invertidas:** ~40 horas (8 horas/semana × 5 semanas)

---

## 🎬 ¡Listo para la Presentación!

**Estado del Proyecto:** ✅ **100% COMPLETO**

**Confianza para Demo:** ✅ **ALTA**

**Documentación:** ✅ **PROFESIONAL**

**Integración:** ✅ **PERFECTA**

---

**Semana 7 - Presentación y Cierre del Proyecto** ✅

🎉 **¡PROYECTO COMPLETADO EXITOSAMENTE!** 🎉
