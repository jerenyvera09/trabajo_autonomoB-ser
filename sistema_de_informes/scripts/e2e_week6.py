import requests
import time

REST = "http://localhost:8000"
GQL = "http://localhost:4000/graphql"

# 1) Register (ignore if already exists)
try:
    r = requests.post(f"{REST}/auth/register", json={"nombre":"Admin","email":"admin@uleam.edu.ec","password":"123456"}, timeout=5)
    print("register:", r.status_code, r.text)
except Exception as e:
    print("register error:", e)

# 2) Login
r = requests.post(f"{REST}/auth/login", json={"email":"admin@uleam.edu.ec","password":"123456"}, timeout=5)
print("login:", r.status_code, r.text)
access = r.json().get("access_token") if r.headers.get('content-type','').startswith('application/json') else None
if not access:
    print("No access token; aborting report creation")
    exit(1)

# 3) Create report (this should notify WS if WS_NOTIFY_URL is set)
payload = {"titulo":"Incidencia prueba Week6","descripcion":"E2E test integración","ubicacion":"Lab A2"}
r = requests.post(f"{REST}/reportes", json=payload, headers={"Authorization": f"Bearer {access}"}, timeout=5)
print("create report:", r.status_code, r.text)

# 4) Query GraphQL analytics (pulls from REST /api/v1/reports)
q = {"query":"query{ reportsAnalytics { total byStatus { clave valor } } }"}
# Give REST a moment to persist
time.sleep(0.5)
try:
    gr = requests.post(GQL, json=q, timeout=5)
    print("graphql:", gr.status_code, gr.text)
except Exception as e:
    print("graphql error:", e)
