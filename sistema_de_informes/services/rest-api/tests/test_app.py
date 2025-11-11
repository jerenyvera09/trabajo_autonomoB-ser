import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from dotenv import load_dotenv

"""Pruebas end-to-end simples contra la API.
Soporta variables:
- DATABASE_URL_TEST (prioritaria)
- DATABASE_URL (fallback)
- DB_SCHEMA (usado en Postgres; ignorado en SQLite)
"""

# Cargar variables de entorno desde .env.test si existe, luego .env
load_dotenv(dotenv_path=".env.test", override=True)
load_dotenv(override=False)

# Asegurar que el directorio del servicio esté en sys.path para importar main.py
SERVICE_DIR = Path(__file__).resolve().parents[1]
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

# Elegir URL de prueba si existe
db_url = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL", "")

if not db_url:
    raise RuntimeError("DATABASE_URL(_TEST) no configurado en .env.test o .env")

# Si estamos usando Postgres de prueba y no hay DB_SCHEMA, usar 'test'
if db_url.startswith("postgres") and os.getenv("DATABASE_URL_TEST") and not os.getenv("DB_SCHEMA"):
    os.environ["DB_SCHEMA"] = "test"

# Asegurar que el proceso FastAPI vea la URL correcta
os.environ["DATABASE_URL"] = db_url

from main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def _register_and_login():
    email = "tester@example.com"
    # Registrar (idempotente)
    client.post("/auth/register", json={
        "nombre": "Tester",
        "email": email,
        "password": "123456"  # contraseña corta para pbkdf2
    })
    # Login
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_crud_reporte_basico():
    headers = _register_and_login()

    # Crear
    payload = {"titulo": "Filtro roto", "descripcion": "Lab A"}
    r = client.post("/reportes", json=payload, headers=headers)
    assert r.status_code == 201, r.text
    rep = r.json()
    rep_id = rep["id_reporte"]

    # Listar
    r = client.get("/reportes", headers=headers)
    assert r.status_code == 200
    assert any(item["id_reporte"] == rep_id for item in r.json())

    # Actualizar
    r = client.put(f"/reportes/{rep_id}", json={"titulo": "Filtro roto (actualizado)"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["titulo"].startswith("Filtro roto")

    # Eliminar
    r = client.delete(f"/reportes/{rep_id}", headers=headers)
    assert r.status_code == 204

def teardown_module(module=None):
    """No se requiere limpieza de archivos; la API ya elimina el reporte creado.
    Para datos adicionales en Supabase, usa esquemas/DB de testing o fixtures.
    """
    pass
