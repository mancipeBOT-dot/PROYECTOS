# Pasar el proyecto a Claude Code en tu computador

Todo el proyecto vive en GitHub. En el computador solo hay que descargarlo; Claude Code lee el archivo `CLAUDE.md` y retoma el contexto sin que tengas que explicarlo de nuevo.

## 1. Instalar (una sola vez)

| Programa | Para qué | Dónde |
|---|---|---|
| Claude (app de escritorio) | Usar Claude Code en el computador | claude.ai/download |
| Git | Descargar y guardar versiones del proyecto | git-scm.com |
| GitHub Desktop | Iniciar sesión en GitHub sin comandos | desktop.github.com |
| Python 3.12 o superior | Ejecutar el código | python.org (marcar "Add Python to PATH") |
| Node.js LTS | Regenerar el PDF y la imagen | nodejs.org |
| Extensión Claude in Chrome | Que Claude revise páginas en tu navegador | Chrome Web Store, buscar "Claude" |

## 2. Descargar el proyecto
1. Pon el repositorio en privado (GitHub → PROYECTOS → Settings → General → Change visibility → Make private).
2. Abre GitHub Desktop → File → Clone repository → `mancipeBOT-dot/PROYECTOS`.
3. Cambia a la rama `claude/municipal-single-window-system-8j87uy`.
4. Abre esa carpeta en Claude Code (app de escritorio → Code → elegir carpeta).
5. Primer mensaje sugerido: "Lee CLAUDE.md y dime en qué quedamos."

## 3. Cuenta de Anthropic

**Decisión: usa tu cuenta actual con tu correo personal.** No necesitas otra. Cuando exista la empresa (SAS), se crea una organización aparte para facturar a nombre de ella.

Son dos cosas distintas:

| Qué | Para qué | Cómo se paga |
|---|---|---|
| Suscripción de Claude (Pro o Max) | Que Claude Code te ayude a programar | Mensual, en claude.ai |
| API de Claude (console.anthropic.com) | Que el sistema clasifique PQRS por su cuenta | Por uso, con saldo prepagado |

Pasos para la API:
1. Entra a console.anthropic.com con tu correo personal.
2. Carga saldo y pon un **límite de gasto mensual** (Settings → Limits).
3. Crea una clave llamada `ventanilla-desarrollo`.
4. Guárdala como variable de entorno `ANTHROPIC_API_KEY` en tu computador. **Nunca la pegues en el chat ni en archivos del proyecto.**

### Costo estimado de clasificar PQRS

Supuesto: ~1.700 tokens de entrada y ~500 de salida por PQRS.

| Modelo | Por PQRS | 500 PQRS al mes |
|---|---|---|
| `claude-opus-5-5` (por defecto) | ~US$0,017 | ~US$8,5 |
| `claude-haiku-5-5` | ~US$0,0004 | ~US$0,2 |

Se miden con las PQRS reales de prueba antes de decidir el modelo.

## 4. Claude in Chrome: dónde sí y dónde no

| Sí | No (hasta tener el acta de piloto firmada) |
|---|---|
| Página web pública de la alcaldía | Ventanilla única con tu usuario |
| Facebook e Instagram públicos de la alcaldía | Génesis |
| Tus cuentas: GitHub, Google Cloud, Anthropic, SIC, DNDA | Google Workspace de la alcaldía (correos, Drive) |
| Documentación de proveedores (Docling, OPNsense, Meta) | Cualquier página con datos de ciudadanos |

Razón: si Claude navega la ventanilla o Génesis con tus credenciales de contratista, lee datos personales y financieros reales sin autorización (Ley 1581 de 2012). Eso pone en riesgo el proyecto y tu contrato. Para analizar esas herramientas usa **capturas de pantalla con los datos tachados**.

## 5. Permisos que te pedirá Claude Code
Claude Code pide permiso antes de ejecutar comandos o modificar archivos. Acepta los de la carpeta del proyecto; rechaza cualquier acción fuera de ella que no entiendas.
