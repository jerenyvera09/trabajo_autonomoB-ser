# Semana 1 – Setup y Auth Service

**Universidad:** Universidad Laica Eloy Alfaro de Manabí (ULEAM)  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Docente:** Ing. John Cevallos  
**Nivel / Paralelo:** 5to nivel – Paralelo B  
**Fecha:** 23/12/2025  

## Integrantes del grupo
- Carlos  
- Cinthia Zambrano  
- Jereny Vera  

---

## Objetivo de la semana
De acuerdo con el cronograma oficial del Segundo Parcial, el objetivo de la Semana 1 fue realizar el setup inicial del proyecto, implementar un microservicio de autenticación de forma independiente y preparar la infraestructura base necesaria para el desarrollo posterior del sistema.

---

## Actividades realizadas
Durante esta semana se realizaron las siguientes actividades:

- Configuración del entorno para una arquitectura basada en microservicios.
- Implementación del microservicio de autenticación (Auth Service) de manera independiente.
- Uso de JWT con access token y refresh token.
- Validación local de tokens sin llamadas constantes al servicio de autenticación.
- Revocación de tokens mediante blacklist.
- Control básico de intentos fallidos de login (rate limiting).
- Preparación de la infraestructura con Docker.
- Instalación base de n8n sin creación de workflows ni integraciones.

---

## Estado del sistema
- El sistema desarrollado en el Primer Parcial se mantiene intacto.
- No se realizaron modificaciones sobre los servicios REST, GraphQL, WebSocket ni el Frontend.
- El Auth Service funciona como un servicio independiente y aislado.

---

## Alcance y restricciones
En cumplimiento estricto del alcance definido para la Semana 1:

- No pagos.
- No webhooks.
- No MCP.
- No IA.
- No frontend nuevo.
- No tests automatizados.
- No workflows en n8n.

---

## Infraestructura y ejecución
La infraestructura del sistema se levantó de forma local utilizando Docker, permitiendo la convivencia de los servicios sin afectar al sistema del Primer Parcial.

Los contenedores activos en esta semana son:
- `auth-service`
- `auth-db`
- `n8n`

---

## URLs locales de verificación (Semana 1)

Las siguientes URLs corresponden a servicios levantados localmente mediante Docker y se utilizan únicamente para verificación de infraestructura durante la Semana 1:

- **Auth Service (Health Check):**  
  http://localhost:8001/health  

- **n8n (Instalación base):**  
  http://localhost:5679  

Estas URLs se utilizan solo con fines de validación local y no representan integraciones funcionales ni flujos automatizados en esta etapa del proyecto.

---

## Pruebas manuales realizadas
Las pruebas se ejecutaron manualmente utilizando PowerShell, curl y Docker Desktop, validando el correcto funcionamiento del microservicio de autenticación.

### Pruebas ejecutadas
- Registro de usuarios válidos.
- Login con credenciales correctas (HTTP 200).
- Login con credenciales incorrectas (HTTP 401).
- Activación de rate limiting tras múltiples intentos fallidos (HTTP 429).
- Uso incorrecto de refresh token en endpoints protegidos (HTTP 401).
- Rotación de refresh token y revocación del anterior.
- Logout y verificación de token revocado.
- Registro duplicado de usuario (HTTP 400).
- Validación de tokens mediante `/auth/validate`.

### Interpretación de códigos HTTP
- **200 OK:** operación exitosa.
- **401 Unauthorized:** credenciales inválidas o token revocado (comportamiento esperado).
- **400 Bad Request:** datos inválidos o usuario duplicado.
- **429 Too Many Requests:** protección ante múltiples intentos fallidos de autenticación.

Los resultados obtenidos confirman el correcto manejo de seguridad y estados del sistema.

---

## Coordinación con grupo partner (Pilar 2)
- El grupo partner aún no ha sido definido.
- La coordinación se realizará en la Semana 2.
- En la Semana 1 solo se documenta la intención de integración B2B, sin implementación técnica.

---

## Distribución de responsabilidades del equipo
El trabajo correspondiente a la Semana 1 se organizó de la siguiente manera:

- **Carlos:** documentación del Auth Service y estructura del Segundo Parcial.
- **Cinthia Zambrano:** ejecución y verificación de pruebas manuales del microservicio de autenticación.
- **Jereny Vera:** documentación de la planificación inicial de coordinación con el grupo partner.

---

## Conclusión de la semana
La Semana 1 permitió establecer una base sólida para el Segundo Parcial, dejando configurada la infraestructura, el microservicio de autenticación completamente funcional y validado mediante pruebas manuales. El sistema queda preparado para continuar con las siguientes fases del proyecto de manera ordenada y conforme al cronograma establecido.
