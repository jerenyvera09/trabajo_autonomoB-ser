from __future__ import annotations

import base64
import io
from collections import Counter
from typing import Any, Dict

from tools.base import MCPTool


def _strip_data_url(value: str) -> str:
    v = (value or "").strip()
    if v.startswith("data:") and "," in v:
        return v.split(",", 1)[1]
    return v


def _dominant_rgb(img) -> tuple[int, int, int]:
    # Reduce para un cálculo rápido
    small = img.convert("RGB").resize((64, 64))
    pixels = list(small.getdata())
    (r, g, b), _ = Counter(pixels).most_common(1)[0]
    return int(r), int(g), int(b)


class ImageInspectTool(MCPTool):
    """Tool (query) para analizar una imagen (multimodal) sin APIs externas.

    Args esperados:
      - image_base64: string en base64 (o Data URL) de una imagen (PNG/JPG/etc)

    Devuelve:
      - formato, tamaño, modo y color dominante aproximado.
    """

    name = "image_inspect"
    kind = "query"

    def run(self, args: Dict[str, Any]) -> Dict[str, Any]:
        raw = args.get("image_base64")
        if not isinstance(raw, str) or not raw.strip():
            return {"ok": False, "error": "missing_image", "message": "Provide image_base64 (base64 or data URL)"}

        b64 = _strip_data_url(raw)
        try:
            data = base64.b64decode(b64, validate=False)
        except Exception as e:
            return {"ok": False, "error": "invalid_base64", "message": str(e)}

        try:
            from PIL import Image  # pillow
        except Exception as e:
            return {
                "ok": False,
                "error": "missing_dependency",
                "message": f"Pillow no está instalado: {e}. Agrega 'Pillow' a requirements.txt",
            }

        try:
            with Image.open(io.BytesIO(data)) as img:
                width, height = img.size
                mode = img.mode
                fmt = img.format or "unknown"
                dom = _dominant_rgb(img)

            return {
                "ok": True,
                "format": fmt,
                "width": width,
                "height": height,
                "mode": mode,
                "dominant_rgb": {"r": dom[0], "g": dom[1], "b": dom[2]},
                "note": "Análisis local (multimodal imagen) sin APIs externas.",
            }
        except Exception as e:
            return {"ok": False, "error": "image_parse_failed", "message": str(e)}
