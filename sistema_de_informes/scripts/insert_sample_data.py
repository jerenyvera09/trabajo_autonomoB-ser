"""
Script para insertar datos de prueba en Supabase
Ejecutar desde: python scripts/insert_sample_data.py
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Configurar path para importar módulos de rest-api
ROOT = Path(__file__).resolve().parents[1]
REST_DIR = ROOT / "services" / "rest-api"
sys.path.insert(0, str(REST_DIR))

from db import SessionLocal
# Importar todas las entidades para evitar problemas de relaciones
from entities.rol import Rol
from entities.usuario import Usuario
from entities.categoria import Categoria
from entities.area import Area
from entities.estado_reporte import EstadoReporte
from entities.reporte import Reporte
from entities.etiqueta import Etiqueta
from entities.comentario import Comentario
from entities.puntuacion import Puntuacion
from entities.archivo_adjunto import ArchivoAdjunto

def insert_data():
    session = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("🚀 INSERTANDO DATOS DE PRUEBA EN SUPABASE")
        print("="*60 + "\n")
        
        # 1. ROLES
        print("📝 [1/7] Insertando roles...")
        roles_data = [
            {"nombre_rol": "Administrador", "descripcion": "Acceso total al sistema", "permisos": "all"},
            {"nombre_rol": "Usuario", "descripcion": "Usuario estándar con permisos de lectura y escritura", "permisos": "read,write"},
            {"nombre_rol": "Visualizador", "descripcion": "Solo puede ver reportes", "permisos": "read"},
        ]
        
        roles = {}
        for rol_data in roles_data:
            existing = session.query(Rol).filter(Rol.nombre_rol == rol_data["nombre_rol"]).first()
            if existing:
                roles[rol_data["nombre_rol"]] = existing
                print(f"  ⏭️  Rol '{rol_data['nombre_rol']}' ya existe")
            else:
                rol = Rol(**rol_data)
                session.add(rol)
                session.flush()
                roles[rol_data["nombre_rol"]] = rol
                print(f"  ✅ Rol '{rol_data['nombre_rol']}' insertado")
        
        session.commit()
        print(f"  📊 Total roles: {len(roles)}\n")
        
        # 2. USUARIOS
        print("👤 [2/7] Insertando usuarios...")
        usuarios_data = [
            {"nombre": "Juan Pérez", "email": "juan.perez@uleam.edu.ec", "password_hash": "hash_admin_123", "id_rol": roles["Administrador"].id_rol, "estado": "activo"},
            {"nombre": "María García", "email": "maria.garcia@uleam.edu.ec", "password_hash": "hash_user_456", "id_rol": roles["Usuario"].id_rol, "estado": "activo"},
            {"nombre": "Carlos López", "email": "carlos.lopez@uleam.edu.ec", "password_hash": "hash_user_789", "id_rol": roles["Usuario"].id_rol, "estado": "activo"},
            {"nombre": "Ana Martínez", "email": "ana.martinez@uleam.edu.ec", "password_hash": "hash_viewer_321", "id_rol": roles["Visualizador"].id_rol, "estado": "activo"},
        ]
        
        usuarios = {}
        for user_data in usuarios_data:
            existing = session.query(Usuario).filter(Usuario.email == user_data["email"]).first()
            if existing:
                usuarios[user_data["email"]] = existing
                print(f"  ⏭️  Usuario '{user_data['nombre']}' ya existe")
            else:
                usuario = Usuario(**user_data)
                session.add(usuario)
                session.flush()
                usuarios[user_data["email"]] = usuario
                print(f"  ✅ Usuario '{user_data['nombre']}' insertado")
        
        session.commit()
        print(f"  📊 Total usuarios: {len(usuarios)}\n")
        
        # 3. CATEGORÍAS
        print("📂 [3/7] Insertando categorías...")
        categorias_data = [
            {"nombre": "Infraestructura", "descripcion": "Problemas relacionados con infraestructura física", "prioridad": "alta", "estado": "activo"},
            {"nombre": "Servicios Públicos", "descripcion": "Servicios municipales y públicos", "prioridad": "media", "estado": "activo"},
            {"nombre": "Seguridad", "descripcion": "Temas de seguridad ciudadana", "prioridad": "alta", "estado": "activo"},
            {"nombre": "Mantenimiento", "descripcion": "Mantenimiento general de instalaciones", "prioridad": "baja", "estado": "activo"},
            {"nombre": "Medio Ambiente", "descripcion": "Asuntos ambientales y ecológicos", "prioridad": "media", "estado": "activo"},
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            existing = session.query(Categoria).filter(Categoria.nombre == cat_data["nombre"]).first()
            if existing:
                categorias[cat_data["nombre"]] = existing
                print(f"  ⏭️  Categoría '{cat_data['nombre']}' ya existe")
            else:
                categoria = Categoria(**cat_data)
                session.add(categoria)
                session.flush()
                categorias[cat_data["nombre"]] = categoria
                print(f"  ✅ Categoría '{cat_data['nombre']}' insertada")
        
        session.commit()
        print(f"  📊 Total categorías: {len(categorias)}\n")
        
        # 4. ÁREAS
        print("📍 [4/7] Insertando áreas...")
        areas_data = [
            {"nombre_area": "Centro", "ubicacion": "Centro de la ciudad", "responsable": "Juan Pérez", "descripcion": "Zona centro y comercial"},
            {"nombre_area": "Norte", "ubicacion": "Zona norte residencial", "responsable": "María García", "descripcion": "Área residencial norte"},
            {"nombre_area": "Sur", "ubicacion": "Zona sur industrial", "responsable": "Carlos López", "descripcion": "Área industrial y comercial sur"},
            {"nombre_area": "Este", "ubicacion": "Zona este universitaria", "responsable": "Ana Martínez", "descripcion": "Campus universitario y educativo"},
        ]
        
        areas = {}
        for area_data in areas_data:
            existing = session.query(Area).filter(Area.nombre_area == area_data["nombre_area"]).first()
            if existing:
                areas[area_data["nombre_area"]] = existing
                print(f"  ⏭️  Área '{area_data['nombre_area']}' ya existe")
            else:
                area = Area(**area_data)
                session.add(area)
                session.flush()
                areas[area_data["nombre_area"]] = area
                print(f"  ✅ Área '{area_data['nombre_area']}' insertada")
        
        session.commit()
        print(f"  📊 Total áreas: {len(areas)}\n")
        
        # 5. ESTADOS
        print("🔖 [5/7] Insertando estados...")
        estados_data = [
            {"nombre": "Pendiente", "descripcion": "Reporte recibido, pendiente de revisión", "color": "#FFA500", "orden": 1, "es_final": False},
            {"nombre": "En Proceso", "descripcion": "Reporte en revisión o atención", "color": "#0000FF", "orden": 2, "es_final": False},
            {"nombre": "Resuelto", "descripcion": "Problema resuelto satisfactoriamente", "color": "#008000", "orden": 3, "es_final": True},
            {"nombre": "Cerrado", "descripcion": "Reporte cerrado sin acción", "color": "#808080", "orden": 4, "es_final": True},
            {"nombre": "Rechazado", "descripcion": "Reporte rechazado por no cumplir criterios", "color": "#FF0000", "orden": 5, "es_final": True},
        ]
        
        estados = {}
        for estado_data in estados_data:
            existing = session.query(EstadoReporte).filter(EstadoReporte.nombre == estado_data["nombre"]).first()
            if existing:
                estados[estado_data["nombre"]] = existing
                print(f"  ⏭️  Estado '{estado_data['nombre']}' ya existe")
            else:
                estado = EstadoReporte(**estado_data)
                session.add(estado)
                session.flush()
                estados[estado_data["nombre"]] = estado
                print(f"  ✅ Estado '{estado_data['nombre']}' insertado")
        
        session.commit()
        print(f"  📊 Total estados: {len(estados)}\n")
        
        # 6. REPORTES
        print("📋 [6/7] Insertando reportes...")
        reportes_data = [
            {
                "titulo": "Bache profundo en Av. Principal",
                "descripcion": "Existe un bache de aproximadamente 50cm de diámetro que representa un peligro para vehículos y motocicletas",
                "ubicacion": "Av. Principal esquina con Calle 10",
                "id_categoria": categorias["Infraestructura"].id_categoria,
                "id_area": areas["Centro"].id_area,
                "id_usuario": usuarios["juan.perez@uleam.edu.ec"].id_usuario,
                "id_estado": estados["Pendiente"].id_estado,
                "creado_en": datetime.now()
            },
            {
                "titulo": "Luz de poste fundida desde hace 2 semanas",
                "descripcion": "El poste de luz frente al parque central no funciona, dejando la zona oscura por las noches",
                "ubicacion": "Parque Central, poste #45",
                "id_categoria": categorias["Servicios Públicos"].id_categoria,
                "id_area": areas["Norte"].id_area,
                "id_usuario": usuarios["maria.garcia@uleam.edu.ec"].id_usuario,
                "id_estado": estados["En Proceso"].id_estado,
                "creado_en": datetime.now()
            },
            {
                "titulo": "Vandalismo en mobiliario urbano",
                "descripcion": "Bancas del parque destruidas y grafitis en las paredes",
                "ubicacion": "Parque Municipal Zona Norte",
                "id_categoria": categorias["Seguridad"].id_categoria,
                "id_area": areas["Norte"].id_area,
                "id_usuario": usuarios["carlos.lopez@uleam.edu.ec"].id_usuario,
                "id_estado": estados["En Proceso"].id_estado,
                "creado_en": datetime.now()
            },
            {
                "titulo": "Fuga de agua en tubería principal",
                "descripcion": "Se observa fuga constante de agua en la tubería de la calle 5, desperdicio considerable",
                "ubicacion": "Calle 5 entre Av. Universidad y Calle 6",
                "id_categoria": categorias["Servicios Públicos"].id_categoria,
                "id_area": areas["Este"].id_area,
                "id_usuario": usuarios["ana.martinez@uleam.edu.ec"].id_usuario,
                "id_estado": estados["Resuelto"].id_estado,
                "creado_en": datetime.now()
            },
            {
                "titulo": "Acumulación de basura en esquina",
                "descripcion": "Basura acumulada por varios días, generando malos olores y atrayendo insectos",
                "ubicacion": "Esquina Calle Industrial con Av. del Trabajo",
                "id_categoria": categorias["Medio Ambiente"].id_categoria,
                "id_area": areas["Sur"].id_area,
                "id_usuario": usuarios["juan.perez@uleam.edu.ec"].id_usuario,
                "id_estado": estados["Resuelto"].id_estado,
                "creado_en": datetime.now()
            },
            {
                "titulo": "Señalización vial deteriorada",
                "descripcion": "Las señales de tránsito están desgastadas y poco visibles",
                "ubicacion": "Intersección Av. Principal con Calle 15",
                "id_categoria": categorias["Infraestructura"].id_categoria,
                "id_area": areas["Centro"].id_area,
                "id_usuario": usuarios["maria.garcia@uleam.edu.ec"].id_usuario,
                "id_estado": estados["Pendiente"].id_estado,
                "creado_en": datetime.now()
            },
            {
                "titulo": "Árbol caído bloqueando acera",
                "descripcion": "Un árbol grande cayó por las lluvias y bloquea completamente la acera",
                "ubicacion": "Calle Los Laureles #234",
                "id_categoria": categorias["Medio Ambiente"].id_categoria,
                "id_area": areas["Norte"].id_area,
                "id_usuario": usuarios["carlos.lopez@uleam.edu.ec"].id_usuario,
                "id_estado": estados["En Proceso"].id_estado,
                "creado_en": datetime.now()
            },
        ]
        
        reportes_count = 0
        for reporte_data in reportes_data:
            existing = session.query(Reporte).filter(Reporte.titulo == reporte_data["titulo"]).first()
            if existing:
                print(f"  ⏭️  Reporte '{reporte_data['titulo'][:40]}...' ya existe")
            else:
                reporte = Reporte(**reporte_data)
                session.add(reporte)
                reportes_count += 1
                print(f"  ✅ Reporte '{reporte_data['titulo'][:40]}...' insertado")
        
        session.commit()
        print(f"  📊 Total reportes insertados: {reportes_count}\n")
        
        # 7. ETIQUETAS
        print("🏷️  [7/7] Insertando etiquetas...")
        etiquetas_data = [
            {"nombre": "Urgente", "color": "#FF0000"},
            {"nombre": "Importante", "color": "#FFA500"},
            {"nombre": "Normal", "color": "#0000FF"},
            {"nombre": "Bajo", "color": "#808080"},
        ]
        
        etiquetas = {}
        for etiq_data in etiquetas_data:
            existing = session.query(Etiqueta).filter(Etiqueta.nombre == etiq_data["nombre"]).first()
            if existing:
                etiquetas[etiq_data["nombre"]] = existing
                print(f"  ⏭️  Etiqueta '{etiq_data['nombre']}' ya existe")
            else:
                etiqueta = Etiqueta(**etiq_data)
                session.add(etiqueta)
                session.flush()
                etiquetas[etiq_data["nombre"]] = etiqueta
                print(f"  ✅ Etiqueta '{etiq_data['nombre']}' insertada")
        
        session.commit()
        print(f"  📊 Total etiquetas: {len(etiquetas)}\n")
        
        # RESUMEN FINAL
        print("="*60)
        print("✅ DATOS INSERTADOS EXITOSAMENTE EN SUPABASE")
        print("="*60)
        print("\n📊 RESUMEN FINAL:")
        print(f"  - Roles: {session.query(Rol).count()}")
        print(f"  - Usuarios: {session.query(Usuario).count()}")
        print(f"  - Categorías: {session.query(Categoria).count()}")
        print(f"  - Áreas: {session.query(Area).count()}")
        print(f"  - Estados: {session.query(EstadoReporte).count()}")
        print(f"  - Reportes: {session.query(Reporte).count()}")
        print(f"  - Etiquetas: {session.query(Etiqueta).count()}")
        print("\n🎉 ¡Actualiza el frontend (http://localhost:5173) para ver los datos!")
        print("="*60 + "\n")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()
    
    return True

if __name__ == "__main__":
    success = insert_data()
    sys.exit(0 if success else 1)
