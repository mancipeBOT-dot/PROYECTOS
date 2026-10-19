"""Utilidades de texto: normalización y extracción de datos con expresiones regulares."""

import re
import unicodedata

_CORREO = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_CEDULA = re.compile(r"\b(?:c\.?\s?c\.?|c[eé]dula(?: de ciudadan[ií]a)?)\s*(?:n[o°º]\.?\s*)?([\d][\d.\s]{5,14}\d)", re.IGNORECASE)


def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes, para comparar palabras clave."""
    sin_tildes = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sin_tildes.lower())


def contiene(texto_normalizado: str, frase: str) -> bool:
    return re.search(rf"\b{re.escape(normalizar(frase))}\b", texto_normalizado) is not None


def contar(texto_normalizado: str, frase: str) -> int:
    return len(re.findall(rf"\b{re.escape(normalizar(frase))}\b", texto_normalizado))


def extraer_correo(texto: str) -> str:
    encontrado = _CORREO.search(texto)
    return encontrado.group(0) if encontrado else ""


def extraer_cedula(texto: str) -> str:
    encontrado = _CEDULA.search(texto)
    return re.sub(r"\D", "", encontrado.group(1)) if encontrado else ""


def extraer_asunto(texto: str, max_palabras: int = 15) -> str:
    """Toma la línea 'Asunto:' si existe; si no, la primera oración."""
    linea = re.search(r"asunto\s*:\s*(.+)", texto, re.IGNORECASE)
    base = linea.group(1) if linea else re.split(r"(?<=[.!?])\s", texto.strip(), maxsplit=1)[0]
    return " ".join(base.split()[:max_palabras])
