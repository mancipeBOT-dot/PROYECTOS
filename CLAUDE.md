# Contexto para Claude Code

## Autor y forma de trabajo
- Autor y dueño: Jaime Raúl López Mancipe. Es administrador, no programador: Claude escribe el código y él lo administra.
- Responder en español, corto y directo. Si pide una recomendación: una sola decisión, no varias opciones. Datos concretos antes que adjetivos. Sin lenguaje publicitario.
- Hacer las preguntas necesarias cuando falte información.

## Proyecto principal: `ventanilla-unica/` — Ventanilla Única Inteligente (Software JRLM)
Servicio para alcaldías municipales, de autoría propia. Las alcaldías contratan el servicio (licencia de uso), no el desarrollo.

Qué hace: recibe PQRS (correo central, escáner → Google Drive, página web, Facebook/Instagram), las pasa por OCR a Markdown, las clasifica con IA, las asigna a dependencia y funcionario, calcula términos legales (Ley 1755 de 2015, días hábiles con festivos) y avisa en la pantalla de cada PC a las 8:00 y 14:00. Módulos conectados: solicitudes internas, agente de actividad (tiempos muertos), Wi-Fi por cédula + equipo, Génesis (financiero, solo lectura), PSE Banco de Bogotá, reportes.

**La IA solo clasifica y asigna. Nunca redacta borradores ni respuestas.**

Documentos clave (leer antes de cambiar algo grande):
- `ventanilla-unica/README.md` — índice y decisiones tomadas.
- `ventanilla-unica/documento_funcionamiento.pdf` (fuente: `fuentes/documento.html`; regenerar con `node fuentes/render.js`).
- `ventanilla-unica/propiedad-intelectual.md` — reglas para proteger la autoría.
- `ventanilla-unica/plan-de-inicio.md`, `ventanilla-unica/preguntas.md`.

## Alcaldía piloto (datos reales conocidos)
- 9 dependencias: Despacho del Alcalde, Gobierno, Hacienda, Planeación, Infraestructura, Contratación, Unidad de Servicios Públicos, Desarrollo Social y Económico, Bienes y Servicios (inventario). ~3 PC cada una, Windows 11.
- Control Interno recibe los avisos de PQRS vencidas (no recibe PQRS).
- Google Workspace. Internet: Colombia Más. Génesis en la nube del proveedor. Recaudo: Banco de Bogotá.
- Jornadas 8:00–12:00 y 14:00–18:00.
- Además: Concejo Municipal y Personería, entidades independientes. Se hace seguimiento solo a sus dos secretarias de planta (están en la nómina de la alcaldía). El Concejo tiene sesiones ordinarias (en los periodos de ley; el autor las llama "sincrónicas") y extraordinarias (fuera de esos periodos; "asincrónicas").

## Reglas que no se rompen
1. **No usar datos reales** de la ventanilla, Génesis ni del Workspace de la alcaldía sin autorización escrita. Probar con datos ficticios o anonimizados.
2. **No guardar en el repositorio** claves de API, contraseñas, datos personales ni documentos reales. Las claves van en variables de entorno o en `.env` (ignorado por git).
3. Todo archivo nuevo lleva la autoría de Jaime Raúl López Mancipe; el software es propietario (`ventanilla-unica/LICENCIA.md`).
4. Cuentas del proyecto (GitHub, Google Cloud, Anthropic, dominio) solo con el correo personal del autor, nunca con correos de la alcaldía.

## Código: `ventanilla-unica/backend/` (Python)
```bash
cd ventanilla-unica/backend
python -m venv .venv && .venv/bin/pip install -e ".[dev]"   # en Windows: .venv\Scripts\pip
.venv/bin/python -m pytest
.venv/bin/python -m ventanilla.simulacion        # agregar --ia para usar la API de Claude
```
- IA: `ventanilla/clasificador.py`. Modelo por defecto `claude-opus-5-5` (variable `VUI_MODELO`). Respaldo por palabras clave si la IA falla.
- Catálogo de dependencias y funcionarios ficticios: `datos/alcaldia.json`.
- Almacenamiento en memoria (prototipo). Pendiente: PostgreSQL.

## Siguientes pasos
1. OCR con Docling y lectura de la carpeta de Google Drive / correo central (Gmail).
2. Probar la clasificación con IA real usando 10–20 PQRS anonimizadas.
3. Base de datos PostgreSQL y panel web.
4. Agente de Windows (alertas de jornada).
5. Módulo de Concejo y Personería (por definir con el autor).
