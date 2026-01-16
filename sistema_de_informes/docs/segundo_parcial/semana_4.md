# Semana 4 – Integración Multimodal + Webhooks + Frontend + Testing

**Universidad:** Universidad Laica Eloy Alfaro de Manabí (ULEAM)  
**Carrera:** Ingeniería de Software  
**Asignatura:** Aplicación para el Servidor Web  
**Docente:** Ing. John Cevallos  
**Nivel / Paralelo:** 5to nivel – Paralelo B  
**Fecha:** 16/01/2026  

## Integrantes del grupo
- Carlos  
- Cinthia Zambrano  
- Jereny Vera  

---

## Objetivo de la semana (Semana 4)
De acuerdo con el requerimiento de la Semana 4, el objetivo es demostrar un flujo **end-to-end** que incluya:

- **Webhooks bidireccionales (B2B):**
	- Dirección A: nuestro sistema → partner.
	- Dirección B: partner → nuestro sistema.
- **Integración multimodal (PDF):** carga manual de un PDF, extracción real de texto y uso de ese contenido para disparar lógica.
- **Frontend funcional:** interfaz con módulos de **Chat** y **Pagos**.
- **Testing de integración:** un script automatizado que valide el flujo completo sin depender de acciones manuales.

---

## Qué se implementó (con rutas exactas)

### 1) REST API (PDF Extraction)
- Archivo: `sistema_de_informes/services/rest-api/routers/pdf.py`
- Endpoint: `POST /api/v1/pdf/extract`
- Función: recibe un archivo PDF (`multipart/form-data`) y extrae texto usando **PyPDF2**.

### 2) AI Orchestrator (Tools MCP)
- Archivo: `sistema_de_informes/services/ai-orchestrator/tools/pdf_tool.py`
- Tools agregadas:
	- `pdf_inspect` (query): inspección del texto extraído (cantidad de caracteres/palabras y estimación simple de monto).
	- `pdf_to_partner_payment` (action): usa el texto del PDF para **crear un pago** y luego **disparar un webhook** al partner (cuando se provee `partner_id`).

### 3) Frontend (Semana 4)
- Archivos:
	- `sistema_de_informes/apps/frontend/src/components/PdfUploader.tsx`
	- `sistema_de_informes/apps/frontend/src/components/ChatUI.tsx`
	- `sistema_de_informes/apps/frontend/src/components/Payments.tsx`
	- `sistema_de_informes/apps/frontend/src/App.tsx`

Funcionalidades principales:
- Subida manual de PDF y visualización del texto extraído.
- Chat simple que consume el endpoint `/chat` del AI Orchestrator.
- Módulo de pagos que lista pagos y crea pagos reales contra el Payment Service.

### 4) Script E2E (Integración Semana 4)
- Archivo: `sistema_de_informes/scripts/semana4_integration_test.ps1`
- Función: valida el flujo completo PDF → extracción → tool → pago → webhook → partner + la vía inversa partner → payment.

---

## Flujo end-to-end (qué ocurre en la demo)
1) El usuario sube un **PDF real** (manual desde UI o generado por el script).
2) La REST API extrae el texto del PDF en `POST /api/v1/pdf/extract`.
3) El frontend envía un mensaje al AI Orchestrator y, si existe texto PDF, lo pasa en `toolArgs.text`.
4) El AI Orchestrator ejecuta una tool real:
	 - `pdf_inspect` para evidenciar lectura del texto.
	 - o `pdf_to_partner_payment` para crear un pago basado en el contenido y activar el webhook.
5) El Payment Service crea el pago y puede disparar un webhook firmado al Partner PHP.
6) Se valida también la **bidireccionalidad**: el Partner PHP envía un webhook firmado a `/webhooks/partner` del Payment Service.

---

## Cómo ejecutar / probar (comandos exactos)

### 1) Levantar toda la infraestructura
Desde la raíz del repositorio:

```bash
docker compose up -d --build
```

### 2) Probar E2E (PowerShell)
Desde la raíz del repositorio:

```powershell
powershell -ExecutionPolicy Bypass -File sistema_de_informes/scripts/semana4_integration_test.ps1
```

### 3) Probar UI (Frontend)

```bash
cd sistema_de_informes/apps/frontend
npm install
npm run dev
```

Luego, en la UI:
- Carga un PDF y presiona “Extraer texto PDF”.
- Envía un mensaje en el Chat.
- Crea y lista pagos desde la sección “Pagos”.

---

## URLs locales (verificación)

- **REST API (Health Check):**
	http://localhost:8000/health

- **PDF Extract (POST):**
	http://localhost:8000/api/v1/pdf/extract

- **AI Orchestrator (Health Check):**
	http://localhost:8003/health

- **Payment Service (Health Check):**
	http://localhost:8002/health

- **Partner PHP (Health Check):**
	http://localhost:8088/health

- **n8n (UI):**
	http://localhost:5678
  
	Nota: si el puerto 5678 está ocupado, Docker puede fallar al publicar el puerto. En ese caso, libera el puerto o ajusta el mapeo del servicio n8n.

---

## Resultados esperados (códigos HTTP)

### Interpretación rápida
- **200 OK / 201 Created:** operación exitosa.
- **409 Conflict en /partners/register:**
	- Puede ocurrir si el partner se registra con un `partnerId` que ya existe.
	- No es un fallo del sistema; es un comportamiento esperado para evitar duplicados.
- **401 Unauthorized (HMAC inválido):**
	- Ocurre cuando la firma HMAC no coincide con el body.
	- Se considera una **prueba negativa** correcta: el sistema rechaza webhooks no confiables.

---

## Evidencia sugerida (2–3 capturas)
Para sustentar la entrega de Semana 4, se recomienda capturar:

1) `docker compose ps` mostrando contenedores levantados.
2) Salida de `sistema_de_informes/scripts/semana4_integration_test.ps1` terminando en **[OK]**.
3) UI del frontend mostrando:
	 - Texto extraído del PDF.
	 - Respuesta del chat (incluyendo detalle de tool usada).
	 - Lista/creación de pagos.

---

## Conclusión de la semana
La Semana 4 queda demostrada con un flujo completo y verificable: **multimodal PDF real**, ejecución de **tools reales en el AI Orchestrator**, creación de pagos en el **Payment Service**, y **webhooks bidireccionales** con el partner PHP. Además, el script E2E permite repetir la demostración sin depender de pasos manuales.
