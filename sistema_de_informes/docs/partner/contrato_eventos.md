# Coordinación con Grupo Partner (Semana 1)

Este documento registra la coordinación temprana con el grupo partner para el sistema de informes.

## Descripción del Grupo Partner
- Organización: Grupo externo responsable de integración de eventos entre sistemas.
- Rol: Consumir/emitir eventos relacionados a usuarios y autenticación.
- Responsables: Equipo Partner (contacto: TBD).

## Eventos Propuestos (borrador)
- `user.registered`: Emitido cuando un usuario se registra exitosamente.
- `user.login.succeeded`: Emitido cuando un usuario inicia sesión correctamente.
- `user.logout`: Emitido cuando un usuario cierra sesión y se revocan tokens.
- `token.refresh`: Emitido cuando se rota el refresh token y se emite uno nuevo.

> Nota: Solo se definen nombres y payloads sugeridos. No se implementan webhooks ni integraciones en Semana 1.

## Formato de Payload Sugerido
- `user.registered`
  - `{ id_usuario: number, email: string, nombre: string, fecha: ISO8601 }`
- `user.login.succeeded`
  - `{ id_usuario: number, email: string, fecha: ISO8601, ip: string }`
- `user.logout`
  - `{ id_usuario: number, fecha: ISO8601, motivo: string }`
- `token.refresh`
  - `{ id_usuario: number, fecha: ISO8601, jti_anterior: string, jti_nuevo: string }`

## Nota de Coordinación Temprana
- Alcance limitado a Semana 1: solo definición y acuerdo inicial de eventos.
- No se implementan integraciones end-to-end, webhooks, ni servicios de pago.
- Próximo hito (Semana 2): definición de canales de transporte y políticas de reintento.
