"""Conversión de documentos a Markdown para la IA.

Copyright (c) 2026 Jaime Raúl López Mancipe. Todos los derechos reservados.

- PDF con texto (los que llegan por correo, generados en computador): se lee el texto
  directamente, sin OCR. Es instantáneo.
- PDF escaneado o imagen (radicación presencial): OCR con Docling y EasyOCR en español.
  No requiere instalar programas aparte en Windows; los modelos se descargan la primera vez.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Protocol

# Por debajo de esto, la página se considera escaneada (sin capa de texto).
MIN_CARACTERES_POR_PAGINA = 50
EXTENSIONES_IMAGEN = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


@dataclass
class ResultadoOCR:
    markdown: str
    paginas: int
    metodo: str  # "texto_pdf" u "ocr"


class MotorOCR(Protocol):
    def convertir(self, ruta: Path) -> str: ...


class MotorDocling:
    """OCR con Docling. Se crea una vez y se reutiliza: cargar los modelos tarda varios segundos."""

    def __init__(self, idiomas: tuple[str, ...] = ("es",)):
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
        from docling.document_converter import DocumentConverter, ImageFormatOption, PdfFormatOption

        opciones = PdfPipelineOptions(
            do_ocr=True,
            ocr_options=EasyOcrOptions(lang=list(idiomas), force_full_page_ocr=True),
        )
        self._convertidor = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=opciones),
                InputFormat.IMAGE: ImageFormatOption(pipeline_options=opciones),
            }
        )

    def convertir(self, ruta: Path) -> str:
        return self._convertidor.convert(str(ruta)).document.export_to_markdown()


@lru_cache(maxsize=1)
def _motor_por_defecto() -> MotorDocling:
    """Se crea solo cuando llega el primer documento que necesita OCR."""
    return MotorDocling()


def _texto_por_pagina(ruta: Path) -> list[str]:
    from pypdf import PdfReader

    return [pagina.extract_text() or "" for pagina in PdfReader(ruta).pages]


def a_markdown(ruta: Path, motor: MotorOCR | None = None) -> ResultadoOCR:
    """Convierte un PDF o una imagen a Markdown. Usa OCR solo si hace falta."""
    ruta = Path(ruta)
    if ruta.suffix.lower() in EXTENSIONES_IMAGEN:
        return ResultadoOCR((motor or _motor_por_defecto()).convertir(ruta), 1, "ocr")

    paginas = _texto_por_pagina(ruta)
    if paginas and all(len(p.strip()) >= MIN_CARACTERES_POR_PAGINA for p in paginas):
        markdown = "\n\n".join(f"<!-- página {i} -->\n{p.strip()}" for i, p in enumerate(paginas, 1))
        return ResultadoOCR(markdown, len(paginas), "texto_pdf")

    return ResultadoOCR((motor or _motor_por_defecto()).convertir(ruta), len(paginas), "ocr")
