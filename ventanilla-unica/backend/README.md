# Backend — Ventanilla Única Inteligente (prototipo Fase 1)

Copyright © 2026 Jaime Raúl López Mancipe. Todos los derechos reservados. Ver [`../LICENCIA.md`](../LICENCIA.md).

## Qué hace hoy

| Función | Archivo |
|---|---|
| Términos legales en días hábiles con festivos de Colombia (Ley 1755) | `ventanilla/terminos.py` |
| Clasificación con la API de Claude (salida JSON estructurada) | `ventanilla/clasificador.py` |
| Clasificación de respaldo por palabras clave (sin internet) | `ventanilla/clasificador.py` |
| Asignación al funcionario del tema o al de menor carga | `ventanilla/asignacion.py` |
| Plan diario por jornada (mañana / tarde) | `ventanilla/asignacion.py` |
| Alerta de inicio de jornada y escalamiento (jefe / Control Interno) | `ventanilla/asignacion.py` |
| Flujo completo: radicar → revisar → asignar → aprobación del jefe → devolución por competencia → cerrar | `ventanilla/servicio.py` |
| PDF a Markdown: texto directo o OCR (Docling + EasyOCR en español) | `ventanilla/ocr.py` |
| Radicación automática desde la carpeta de escaneos | `ventanilla/entrada.py` |
| Inventarios: entradas, salidas, gasto, activos, depreciación, bajas | `ventanilla/inventario.py` |
| API web | `ventanilla/api.py` |
| Piloto simulado con 22 PQRS ficticias | `ventanilla/simulacion.py` |

Datos de prueba (ficticios): `datos/alcaldia.json` (las 9 dependencias de la alcaldía piloto con 27 funcionarios ficticios) y `datos/pqrs_prueba.json` (22 PQRS inventadas).

Falta para completar la Fase 1: lectura del correo central (Gmail), base de datos PostgreSQL, agente de Windows y conexión con Google Calendar.

## Cómo ejecutarlo

```bash
cd ventanilla-unica/backend
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,ocr]"   # sin ",ocr" si no se van a leer escaneos

.venv/bin/python -m pytest                    # pruebas
.venv/bin/python -m ventanilla.simulacion     # piloto simulado sin IA
.venv/bin/uvicorn ventanilla.api:app --reload # API en http://127.0.0.1:8000/docs
```

### Carpeta de escaneos

```bash
.venv/bin/python -m ventanilla.entrada --carpeta "G:\Mi unidad\Escaneos PQRS"            # una pasada
.venv/bin/python -m ventanilla.entrada --carpeta "G:\Mi unidad\Escaneos PQRS" --cada 60  # cada minuto
```

- PDF con texto: se lee directo, sin OCR.
- PDF escaneado o imagen (JPG, PNG, TIFF): OCR con Docling + EasyOCR en español. La primera vez descarga los modelos (requiere internet).
- Cada archivo radicado se mueve a `Procesados/` con el número de radicado como nombre; los ilegibles, a `Errores/`.
- Prueba de OCR real (lenta): `VUI_PRUEBA_OCR=1 .venv/bin/python -m pytest tests/test_entrada.py`.

### Con IA

Requiere una clave de la API de Claude a tu nombre (console.anthropic.com):

```bash
export ANTHROPIC_API_KEY=...          # nunca la guardes en el repositorio
.venv/bin/python -m ventanilla.simulacion --ia
VUI_USAR_IA=1 .venv/bin/uvicorn ventanilla.api:app
```

Modelo por defecto: `claude-opus-5-5`. Se cambia con la variable `VUI_MODELO` (ej. `VUI_MODELO=claude-haiku-5-5`, más económico; medir su precisión con la simulación antes de usarlo).

Si la IA no responde, declina o no hay internet, el sistema usa el clasificador por palabras clave. Si la confianza es menor a 0,80, la PQRS queda en revisión para el asignador.

## Resultado de la simulación (palabras clave, sin IA)

- Dependencia correcta: 21 de 22 (95 %). La que falló quedó en revisión humana, así que ninguna se asignó mal.
- Tipo correcto: 22 de 22.
- En revisión humana: 4 de 22.
