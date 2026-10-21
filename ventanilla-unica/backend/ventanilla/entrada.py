"""Radicación automática desde la carpeta de escaneos (Google Drive para escritorio).

Copyright (c) 2026 Jaime Raúl López Mancipe. Todos los derechos reservados.

El radicador escanea cada PQRS completa como un solo archivo en la carpeta. El sistema:
1. Toma cada archivo nuevo (espera a que Drive termine de sincronizarlo).
2. Lo convierte a Markdown (texto del PDF u OCR).
3. Lo radica, clasifica y asigna.
4. Lo mueve a "Procesados" con el número de radicado como nombre. Si falla, a "Errores".

Uso:
    python -m ventanilla.entrada --carpeta "G:\\Mi unidad\\Escaneos PQRS"            # una pasada
    python -m ventanilla.entrada --carpeta "G:\\Mi unidad\\Escaneos PQRS" --cada 60  # cada 60 s
"""

import argparse
import logging
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

from .modelos import PQRS, Canal
from .ocr import EXTENSIONES_IMAGEN, ResultadoOCR, a_markdown
from .servicio import Ventanilla

log = logging.getLogger(__name__)

EXTENSIONES = {".pdf"} | EXTENSIONES_IMAGEN
SEGUNDOS_ESPERA_SINCRONIZACION = 10  # archivo modificado hace menos de esto: Drive aún lo copia
CARPETA_PROCESADOS = "Procesados"
CARPETA_ERRORES = "Errores"


@dataclass
class ResultadoArchivo:
    archivo: str
    pqrs: PQRS | None = None
    error: str = ""


def _mover(archivo: Path, carpeta: Path, nombre: str) -> Path:
    carpeta.mkdir(exist_ok=True)
    destino = carpeta / nombre
    contador = 1
    while destino.exists():  # nunca sobrescribir
        destino = carpeta / f"{Path(nombre).stem}_{contador}{Path(nombre).suffix}"
        contador += 1
    return Path(shutil.move(str(archivo), destino))


def procesar_carpeta(
    carpeta: Path,
    ventanilla: Ventanilla,
    convertir: Callable[[Path], ResultadoOCR] = a_markdown,
    ahora: Callable[[], float] = time.time,
) -> list[ResultadoArchivo]:
    carpeta = Path(carpeta)
    resultados = []
    for archivo in sorted(carpeta.iterdir()):
        if not archivo.is_file() or archivo.suffix.lower() not in EXTENSIONES:
            continue
        if ahora() - archivo.stat().st_mtime < SEGUNDOS_ESPERA_SINCRONIZACION:
            continue  # se toma en la siguiente pasada
        try:
            resultado = convertir(archivo)
            if not resultado.markdown.strip():
                raise ValueError("El documento no tiene texto legible")
            pqrs = ventanilla.radicar(
                resultado.markdown, Canal.PRESENCIAL, datetime.fromtimestamp(archivo.stat().st_mtime)
            )
            destino = _mover(archivo, carpeta / CARPETA_PROCESADOS, f"{pqrs.radicado}{archivo.suffix.lower()}")
            pqrs.archivo_original = str(destino)
            resultados.append(ResultadoArchivo(archivo.name, pqrs=pqrs))
        except Exception as error:  # un archivo dañado no detiene la carpeta
            log.exception("No se pudo procesar %s", archivo.name)
            _mover(archivo, carpeta / CARPETA_ERRORES, archivo.name)
            resultados.append(ResultadoArchivo(archivo.name, error=str(error)))
    return resultados


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--carpeta", type=Path, required=True, help="carpeta de escaneos sincronizada con Drive")
    parser.add_argument("--cada", type=int, default=0, help="repetir cada N segundos (0 = una sola pasada)")
    parser.add_argument("--ia", action="store_true", help="clasificar con la API de Claude")
    args = parser.parse_args()

    from .catalogo import Catalogo
    from .clasificador import Clasificador, ClasificadorIA

    catalogo = Catalogo.desde_archivo()
    ventanilla = Ventanilla(catalogo, Clasificador(catalogo, ClasificadorIA(catalogo) if args.ia else None))

    while True:
        for r in procesar_carpeta(args.carpeta, ventanilla):
            if r.pqrs:
                c = r.pqrs.clasificacion
                print(f"✔ {r.archivo} → {r.pqrs.radicado} | {c.dependencia} | {c.tipo.value} | vence {r.pqrs.vencimiento_legal}")
            else:
                print(f"✘ {r.archivo} → Errores ({r.error})")
        if args.cada <= 0:
            break
        time.sleep(args.cada)


if __name__ == "__main__":
    main()
