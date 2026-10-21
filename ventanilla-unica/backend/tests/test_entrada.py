import os
import time
from pathlib import Path

import pytest

from ventanilla.entrada import CARPETA_ERRORES, CARPETA_PROCESADOS, procesar_carpeta
from ventanilla.modelos import Canal
from ventanilla.ocr import ResultadoOCR, a_markdown


def crear_pdf(ruta: Path, lineas: list[str]) -> Path:
    """PDF mínimo de una página. Sin líneas = página en blanco, como un escaneo sin capa de texto."""
    texto = "".join(f"({l}) Tj 0 -16 Td " for l in lineas)
    contenido = f"BT /F1 12 Tf 50 750 Td {texto}ET".encode("latin-1") if lineas else b""
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(contenido) + contenido + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    salida = bytearray(b"%PDF-1.4\n")
    posiciones = []
    for i, obj in enumerate(objetos, 1):
        posiciones.append(len(salida))
        salida += b"%d 0 obj\n" % i + obj + b"\nendobj\n"
    inicio_xref = len(salida)
    salida += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objetos) + 1)
    salida += b"".join(b"%010d 00000 n \n" % p for p in posiciones)
    salida += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objetos) + 1, inicio_xref)
    ruta.write_bytes(bytes(salida))
    return ruta


def envejecer(ruta: Path, segundos: int = 60) -> None:
    """Simula que Drive ya terminó de sincronizar el archivo."""
    t = time.time() - segundos
    os.utime(ruta, (t, t))


TEXTO_PREDIAL = [
    "Asunto: Solicitud de paz y salvo del impuesto predial.",
    "Solicito la expedicion del paz y salvo del impuesto predial del predio 01-00-0123.",
    "Respuesta a pedro@correo.ejemplo",
]


class MotorFalso:
    def __init__(self, texto: str):
        self.texto, self.llamadas = texto, 0

    def convertir(self, ruta: Path) -> str:
        self.llamadas += 1
        return self.texto


def test_pdf_con_texto_no_usa_ocr(tmp_path):
    motor = MotorFalso("no debería usarse")
    r = a_markdown(crear_pdf(tmp_path / "a.pdf", TEXTO_PREDIAL), motor)
    assert r.metodo == "texto_pdf" and motor.llamadas == 0
    assert "paz y salvo" in r.markdown and r.paginas == 1


def test_pdf_escaneado_usa_ocr(tmp_path):
    motor = MotorFalso("# Solicitud\nPaz y salvo del impuesto predial")
    r = a_markdown(crear_pdf(tmp_path / "escaneo.pdf", []), motor)
    assert r.metodo == "ocr" and motor.llamadas == 1


def test_carpeta_radica_y_mueve_con_numero_de_radicado(tmp_path, ventanilla):
    envejecer(crear_pdf(tmp_path / "scan001.pdf", TEXTO_PREDIAL))
    (tmp_path / "notas.txt").write_text("se ignora")
    resultados = procesar_carpeta(tmp_path, ventanilla)
    assert len(resultados) == 1
    p = resultados[0].pqrs
    assert p.canal == Canal.PRESENCIAL
    assert p.clasificacion.dependencia == "Secretaría de Hacienda"
    assert p.clasificacion.peticionario.correo_respuesta == "pedro@correo.ejemplo"
    assert (tmp_path / CARPETA_PROCESADOS / f"{p.radicado}.pdf").exists()
    assert not (tmp_path / "scan001.pdf").exists()
    assert (tmp_path / "notas.txt").exists()


def test_espera_a_que_drive_termine_de_sincronizar(tmp_path, ventanilla):
    crear_pdf(tmp_path / "recien.pdf", TEXTO_PREDIAL)  # modificado ahora mismo
    assert procesar_carpeta(tmp_path, ventanilla) == []
    assert (tmp_path / "recien.pdf").exists()


def test_documento_ilegible_va_a_errores_sin_detener_la_carpeta(tmp_path, ventanilla):
    envejecer(crear_pdf(tmp_path / "a_blanco.pdf", []))
    envejecer(crear_pdf(tmp_path / "b_bueno.pdf", TEXTO_PREDIAL))

    def convertir(ruta):
        return a_markdown(ruta, MotorFalso(""))  # el OCR no encuentra texto en la página en blanco

    resultados = procesar_carpeta(tmp_path, ventanilla, convertir)
    assert [bool(r.pqrs) for r in resultados] == [False, True]
    assert (tmp_path / CARPETA_ERRORES / "a_blanco.pdf").exists()


def test_sin_docling_se_detiene_sin_mover_escaneos(tmp_path, ventanilla):
    envejecer(crear_pdf(tmp_path / "escaneo.pdf", []))

    def sin_docling(ruta):
        raise ImportError("No module named 'docling'")

    with pytest.raises(SystemExit):
        procesar_carpeta(tmp_path, ventanilla, sin_docling)
    assert (tmp_path / "escaneo.pdf").exists()
    assert not (tmp_path / CARPETA_ERRORES).exists()


@pytest.mark.skipif(os.getenv("VUI_PRUEBA_OCR") != "1", reason="OCR real: VUI_PRUEBA_OCR=1 (descarga modelos)")
def test_ocr_real_con_docling(tmp_path):
    from PIL import Image, ImageDraw, ImageFont

    imagen = Image.new("RGB", (1700, 600), "white")
    dibujo = ImageDraw.Draw(imagen)
    try:
        fuente = ImageFont.truetype("DejaVuSans.ttf", 44)  # Linux
    except OSError:
        fuente = ImageFont.truetype("arial.ttf", 44)  # Windows
    dibujo.text((60, 80), "Solicito paz y salvo del impuesto predial", fill="black", font=fuente)
    dibujo.text((60, 180), "del predio 01-00-0123. Cédula 1234567.", fill="black", font=fuente)
    ruta = tmp_path / "escaneo.pdf"
    imagen.save(ruta, resolution=200)
    r = a_markdown(ruta)
    assert r.metodo == "ocr"
    assert "predial" in r.markdown.lower()
