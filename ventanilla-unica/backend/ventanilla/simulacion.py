"""Piloto simulado: radica PQRS de prueba, mide la asignación y muestra alertas.

Uso:
    python -m ventanilla.simulacion            # clasificador por palabras clave (sin internet)
    python -m ventanilla.simulacion --ia       # con la API de Claude
"""

import argparse
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta

from .catalogo import DATOS, Catalogo
from .clasificador import Clasificador, ClasificadorIA
from .modelos import Canal, Estado
from .servicio import Ventanilla


def main() -> None:
    # En Windows la consola o un archivo redirigido pueden usar cp1252, que no tiene ✔ ni →.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ia", action="store_true", help="clasificar con la API de Claude")
    parser.add_argument("--hoy", type=date.fromisoformat, default=date(2026, 10, 20), help="fecha simulada (AAAA-MM-DD)")
    args = parser.parse_args()

    catalogo = Catalogo.desde_archivo()
    vu = Ventanilla(catalogo, Clasificador(catalogo, ClasificadorIA(catalogo) if args.ia else None))
    casos = json.loads((DATOS / "pqrs_prueba.json").read_text(encoding="utf-8"))

    aciertos_dep = aciertos_tipo = revision = 0
    print(f"Radicando {len(casos)} PQRS de prueba ({'IA' if args.ia else 'palabras clave'})\n")
    for caso in casos:
        fecha = datetime.combine(args.hoy - timedelta(days=caso.get("dias_atras", 0)), datetime.min.time()).replace(hour=9)
        p = vu.radicar(caso["texto"], Canal(caso["canal"]), fecha)
        c = p.clasificacion
        ok_dep = c.dependencia == caso["dependencia_esperada"]
        ok_tipo = c.tipo.value == caso["tipo_esperado"]
        aciertos_dep += ok_dep
        aciertos_tipo += ok_tipo
        marca = "✔" if ok_dep else "✘"
        print(f"{marca} {p.radicado} | {c.dependencia:<32} | {c.tipo.value:<16} | conf. {c.confianza:.2f} | {p.estado.value:<9} | vence {p.vencimiento_legal}")
        if p.estado == Estado.REVISION:
            revision += 1
            vu.confirmar(p.radicado, caso["dependencia_esperada"])  # simula al asignador humano

    n = len(casos)
    print(f"\nDependencia correcta: {aciertos_dep}/{n} ({aciertos_dep / n:.0%})")
    print(f"Tipo correcto:        {aciertos_tipo}/{n} ({aciertos_tipo / n:.0%})")
    print(f"Enviadas a revisión humana: {revision}/{n}")

    carga = Counter(p.funcionario_id for p in vu.abiertas())
    print("\nCarga por funcionario:")
    for fid, total in sorted(carga.items()):
        f = catalogo.funcionario(fid)
        print(f"  {f.nombre:<36} {total}")

    ejemplo = carga.most_common(1)[0][0]
    for bloque in ("manana", "tarde"):
        alerta = vu.alerta(ejemplo, args.hoy, bloque)
        print(f"\nAlerta {bloque} {alerta['fecha']} — {catalogo.funcionario(ejemplo).nombre}:\n  {alerta['mensaje']}")

    esc = vu.escalamientos(args.hoy)
    print(f"\nEscalamientos hoy: {len(esc)}")
    for e in esc:
        print(f"  {e['radicado']} → {e['nivel']} ({e['dias_restantes']} días hábiles)")


if __name__ == "__main__":
    main()
