import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'rest-api'))

from db import engine
from sqlalchemy import text

print("✅ Conexión a Supabase establecida")
print(f"Database URL: {engine.url.database}@{engine.url.host}")

conn = engine.connect()

# Listar tablas
result = conn.execute(text("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public' 
    AND table_type='BASE TABLE'
    ORDER BY table_name
"""))

tables = [row[0] for row in result.fetchall()]
print(f"\n📊 Tablas encontradas ({len(tables)}):")
for table in tables:
    print(f"  - {table}")

# Contar registros en cada tabla
if tables:
    print("\n📈 Registros por tabla:")
    for table in tables:
        try:
            count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = count_result.scalar()
            print(f"  - {table}: {count} registros")
        except Exception as e:
            print(f"  - {table}: Error al contar - {e}")
else:
    print("\n⚠️ No hay tablas en el esquema 'public'")
    print("💡 Necesitas ejecutar el schema SQL o dejar que SQLAlchemy cree las tablas")

conn.close()
