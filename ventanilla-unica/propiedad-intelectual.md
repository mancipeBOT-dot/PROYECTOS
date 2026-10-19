# Propiedad intelectual del software

## 1. Qué protege la ley en Colombia

| Qué | Protección | Norma |
|---|---|---|
| Código fuente, código compilado, manuales, diagramas | Derecho de autor desde que se crean, sin registro obligatorio | Ley 23 de 1982; Decisión Andina 351 de 1993 |
| La idea ("asignar PQRS con IA") | **No se protege**. Solo se protege la forma concreta en que se escribió | Decisión 351, art. 7 |
| El software como invento | No es patentable como tal | Decisión Andina 486, art. 15 |
| El nombre del producto | Marca registrada ante la SIC, 10 años renovables | Decisión 486 |

Conclusión: lo que se protege es el **código y los documentos**, y la defensa real es **no entregarlos** y **dejarlo escrito en el contrato**.

## 2. El riesgo principal: el contrato

Ley 23 de 1982, art. 20 (modificado por la Ley 1450 de 2011, art. 28): en una obra creada por contrato de prestación de servicios **se presume que los derechos patrimoniales pasan al contratante (la alcaldía)**, salvo pacto en contrario por escrito.

Si se firma un contrato de "desarrollo de software" sin cláusula, el software queda de la alcaldía.

**Decisión: contratar como licencia de uso / suscripción del servicio, no como desarrollo.** Cláusulas mínimas:

1. "El software es preexistente y de titularidad exclusiva de [nuestro nombre]. Este contrato otorga una licencia de uso no exclusiva, intransferible y temporal. No hay cesión de derechos patrimoniales." (Este es el pacto en contrario del art. 20).
2. No se entrega código fuente.
3. Prohibición de copiar, descompilar o modificar el software y el agente.
4. Los **datos** (PQRS, radicados, reportes) son de la alcaldía. Al terminar el contrato se entregan exportados (CSV y PDF) en un plazo fijo, ej. 30 días.
5. Nosotros somos **encargados del tratamiento** de datos personales (Ley 1581 de 2012) y cumplimos la política de la alcaldía.
6. Confidencialidad para los funcionarios que conozcan el funcionamiento interno.

Si la alcaldía exige garantía de continuidad: ofrecer **depósito del código (escrow)** ante notario, que solo se libera si dejamos de prestar el servicio. Es mejor que entregar el código.

## 3. Pasos

| # | Acción | Dónde | Costo |
|---|---|---|---|
| 1 | Pasar este proyecto a un **repositorio privado** (el repositorio `PROYECTOS` hoy es público) | GitHub → Settings → General → Change visibility, o repositorio nuevo privado | Gratis |
| 2 | Registrar el software (soporte lógico) cuando haya primera versión funcional, y registrar cada versión mayor | Dirección Nacional de Derecho de Autor (DNDA), en línea | Gratis |
| 3 | Registrar la marca (clases 9 y 42) | Superintendencia de Industria y Comercio (SIC) | Tasa oficial de la SIC |
| 4 | Firmar cesión de derechos y confidencialidad con cualquier persona que programe o diseñe para el proyecto | Documento privado | Gratis |
| 5 | Contrato con la alcaldía con las cláusulas de la sección 2 | Revisión por abogado | Honorarios |

El registro en la DNDA no es obligatorio, pero da **fecha cierta** y es la prueba más fácil ante un conflicto. Los commits de Git con fecha también sirven como prueba complementaria.

## 4. Medidas técnicas

- El código vive solo en nuestro servidor (Google Cloud) y en el repositorio privado.
- La alcaldía accede por navegador; no recibe instaladores del servidor.
- El agente de Windows se entrega compilado, no como código Python.
- La cuenta de Google Cloud, el dominio del sistema y las claves de la API de IA están a nuestro nombre.
- Cada acceso al sistema queda registrado (usuario, fecha, acción).
