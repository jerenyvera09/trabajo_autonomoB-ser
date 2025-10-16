"""
Limpieza local de artefactos que no forman parte del código fuente.
No borra carpetas ni archivos del proyecto, solo caches/compilados y app.db.
"""
from __future__ import annotations
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "services" / "rest-api" / "app.db",
    ROOT / "services" / "rest-api" / "__pycache__",
    ROOT / "services" / "rest-api" / ".pytest_cache",
    ROOT / "services" / "graphql" / "node_modules" / ".cache",
    ROOT / "apps" / "frontend" / "node_modules" / ".cache",
]


def rm_file(p: Path):
    try:
        if p.exists():
            p.unlink()
            print(f"Eliminado archivo: {p}")
    except PermissionError:
        print(f"No se pudo eliminar (en uso): {p}")


def rm_tree(p: Path):
    try:
        if p.exists():
            shutil.rmtree(p)
            print(f"Eliminada carpeta: {p}")
    except PermissionError:
        print(f"No se pudo eliminar (en uso): {p}")


def main():
    for target in TARGETS:
        if target.is_file():
            rm_file(target)
        elif target.is_dir():
            rm_tree(target)
    # Buscar y eliminar caches comunes en todo el repo
    for pattern in ["__pycache__", ".pytest_cache"]:
        for p in ROOT.rglob(pattern):
            rm_tree(p)


if __name__ == "__main__":
    main()
