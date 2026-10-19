# Propiedad intelectual — proyecto personal

## Modelo

1. El autor crea el software por su cuenta, con sus recursos, **antes** de cualquier contrato.
2. El software es del autor.
3. La alcaldía contrata **el servicio** (suscripción / licencia de uso), no el desarrollo.

## Qué protege la ley en Colombia

| Qué | Protección | Norma |
|---|---|---|
| Código, manuales, diagramas | Derecho de autor desde que se crean | Ley 23 de 1982; Decisión Andina 351 de 1993 |
| La idea | **No se protege**; solo la forma concreta escrita | Decisión 351, art. 7 |
| Software como invento | No es patentable como tal | Decisión Andina 486, art. 15 |
| Nombre del producto | Marca ante la SIC, 10 años renovables | Decisión 486 |

## Riesgos

| Riesgo | Por qué | Cómo se evita |
|---|---|---|
| Que el software pase a la alcaldía | Ley 23 de 1982, art. 20 (mod. Ley 1450 de 2011, art. 28): lo creado en cumplimiento de un contrato de prestación de servicios o de trabajo se presume del contratante, salvo pacto escrito | Crearlo fuera de cualquier contrato con la alcaldía y registrarlo antes de contratar |
| Que lo copien | La idea no se protege | No entregar código; registro en la DNDA como prueba de fecha |
| Condición de contratista actual | El autor es contratista de la alcaldía; sus obligaciones no incluyen crear herramientas | Desarrollar fuera del horario del contrato, con equipos y cuentas propias; confirmar con abogado que no hay inhabilidad ni conflicto de interés antes de firmar el servicio |
| Uso de datos reales sin permiso | Ley 1581 de 2012; Ley 1273 de 2009, art. 269A | No copiar datos de la ventanilla ni de Génesis con las credenciales de contratista; desarrollar con documentos de prueba; datos reales solo con autorización escrita |

## Pasos, en orden

| # | Acción | Dónde | Costo |
|---|---|---|---|
| 1 | Poner el proyecto en repositorio privado | GitHub → Settings → General → Change visibility | Gratis |
| 2 | Registrar el software (soporte lógico) apenas haya primera versión, y cada versión mayor | DNDA, en línea | Gratis |
| 3 | Registrar la marca (clases 9 y 42) | SIC | Tasa oficial |
| 4 | Cesión de derechos y confidencialidad con cualquier colaborador | Documento privado | Gratis |
| 5 | Al contratar: licencia de uso no exclusiva, sin cesión de derechos, sin entrega de código, datos de la alcaldía devueltos al terminar | Contrato revisado por abogado | Honorarios |

## Medidas técnicas

- Código solo en el servidor del autor y en el repositorio privado.
- La alcaldía usa el sistema por navegador; el agente de Windows se entrega compilado.
- Cuenta de Google Cloud, dominio y claves de API a nombre del autor.
- Bitácora de cada acceso.
