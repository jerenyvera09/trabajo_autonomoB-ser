import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv

"""Pruebas end-to-end simples contra una base de Supabase.
Soporta variables:
- DATABASE_URL_TEST (prioritaria)
- DATABASE_URL (fallback)
- DB_SCHEMA (por defecto 'public'; para tests se recomienda 'test')
"""

# Cargar variables de entorno desde .env.test si existe, luego .env
load_dotenv(dotenv_path=".env.test", override=True)
load_dotenv(override=False)

# Elegir URL de prueba si existe
db_url = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL", "")

# Si estamos usando DATABASE_URL_TEST, forzar DB_SCHEMA=test si no está definido
if os.getenv("DATABASE_URL_TEST") and not os.getenv("DB_SCHEMA"):
    os.environ["DB_SCHEMA"] = "test"

assert db_url and db_url.startswith("postgres"), (
    "DATABASE_URL(_TEST) no configurado o no es Postgres. Define tu URL de Supabase en .env.test o .env."
)
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
        "password": "123456"
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
