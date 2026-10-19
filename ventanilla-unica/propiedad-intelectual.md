# Protección del autor y del proyecto

Autor: Jaime Raúl López Mancipe · Marca: **Software JRLM** (por registrar) · Objetivo: proveedor de un servicio integral para alcaldías municipales.

## 1. Qué protege la ley

| Qué | Protección | Norma |
|---|---|---|
| Código, documentos, diagramas | Derecho de autor desde que se crean | Ley 23 de 1982; Decisión Andina 351 de 1993 |
| La idea | **No se protege**; solo la forma concreta escrita | Decisión 351, art. 7 |
| Software como invento | No es patentable como tal | Decisión Andina 486, art. 15 |
| Nombre "Software JRLM" | Marca registrada ante la SIC, 10 años renovables | Decisión 486 |

## 2. Lista de verificación

### A. Hacer ya (antes de mostrarle el proyecto a cualquiera)

- [ ] **Poner el repositorio de GitHub en privado** y activar verificación en dos pasos en GitHub.
- [ ] **Revisar tu contrato de prestación de servicios actual.** Busca las palabras "propiedad intelectual", "derechos de autor", "productos" y "entregables". Si dice que todo lo que produzcas durante el contrato es de la alcaldía, **no presentes el proyecto hasta hablar con un abogado**.
- [ ] **Registrar en la DNDA el documento de funcionamiento y la imagen del flujo** como obra literaria inédita (derechodeautor.gov.co → registro en línea, gratis). Eso te da fecha cierta hoy, antes de que exista el código.
- [ ] **Buscar antecedentes de la marca "Software JRLM"** en la SIC (sic.gov.co → Propiedad industrial → búsqueda de antecedentes marcarios, gratis).
- [ ] **Radicar la solicitud de marca "Software JRLM"** ante la SIC a tu nombre, clases 9 (software) y 42 (software como servicio). Se paga una tasa por clase; revisa la tarifa vigente de la SIC.
- [ ] **Todas las cuentas del proyecto con tu correo personal**, nunca con el correo de la alcaldía: GitHub, Google Cloud, API de IA, dominio, NAS.
- [ ] **Ningún archivo del proyecto en el Google Drive o en el correo de la alcaldía.** El administrador de Workspace puede ver esos archivos, y servirían para alegar que el proyecto se hizo con recursos de la alcaldía.

### B. Mientras desarrollas

- [ ] Trabajar fuera del horario del contrato, en tu propio computador.
- [ ] **No sacar datos reales** de Génesis ni de la ventanilla con tus credenciales de contratista (Ley 1273 de 2009, art. 269A; Ley 1581 de 2012). Lo que conoces del funcionamiento sí lo puedes usar; las bases de datos no.
- [ ] Probar con PQRS de ejemplo **anonimizadas** (sin nombres, cédulas, direcciones, correos ni teléfonos).
- [ ] Registrar en la DNDA el software (soporte lógico) apenas haya una primera versión, y cada versión mayor.
- [ ] Comprar el dominio del producto a tu nombre (ej. `softwarejrlm.co`).

### C. Con terceros (el administrador de la página web y redes, programadores, asesores)

- [ ] **Acuerdo de confidencialidad firmado** antes de mostrarle detalles del proyecto.
- [ ] Si alguien escribe código, diseña o hace documentos para el proyecto: **cesión de derechos patrimoniales a tu favor**, por escrito.
- [ ] Al administrador de la página web solo le das lo que necesita: un código para insertar el formulario. Nunca acceso al servidor ni al repositorio.
- [ ] No exponer el proyecto con detalle técnico en reuniones abiertas, redes ni presentaciones sin confidencialidad.

### D. Antes del piloto en la alcaldía

- [ ] **Acta de prueba piloto** firmada por el alcalde o el secretario general, que diga:
  - El software es de autoría y titularidad exclusiva de Jaime Raúl López Mancipe y está registrado en la DNDA (número de registro).
  - El piloto es una prueba temporal (fechas), sin cesión de derechos ni entrega de código.
  - La alcaldía autoriza el uso de sus datos para el piloto y es responsable de ellos; tú eres encargado del tratamiento.
  - Confidencialidad sobre el funcionamiento del software.
  - Al terminar, los datos se devuelven a la alcaldía y se borran del servidor.
- [ ] Que el acta la revise un abogado.
- [ ] El piloto **no** debe aparecer como obligación ni producto de tu contrato actual.

### E. Para vender el servicio a alcaldías

- [ ] **RUT** con actividad de desarrollo de software y servicios informáticos.
- [ ] **Empresa (SAS)** cuando haya el primer contrato. **Decisión: la marca y los registros de software quedan a tu nombre como persona natural, y tú le das licencia a la SAS.** Así el software no responde por las deudas de la empresa ni se pierde si entra un socio.
- [ ] **Facturación electrónica** ante la DIAN.
- [ ] Inscripción como proveedor en **SECOP II**.
- [ ] **RUP** en la Cámara de Comercio, si vas a participar en procesos que lo exijan.
- [ ] Contrato con cada alcaldía como **licencia de uso / suscripción**, nunca como desarrollo. Cláusulas: software preexistente de tu titularidad; sin cesión de derechos; sin entrega de código; prohibido copiar o descompilar; datos de la alcaldía devueltos al terminar; tú eres encargado del tratamiento.
- [ ] Si una alcaldía exige garantía de continuidad: **depósito del código ante notario**, que solo se libera si dejas de prestar el servicio.
- [ ] Ser titular registrado del software ayuda a justificar la **contratación directa** cuando no hay pluralidad de oferentes (Decreto 1082 de 2015, art. 2.2.1.2.1.4.8). Confírmalo con un abogado en cada caso.
- [ ] Pólizas de cumplimiento cuando el contrato las exija.

### F. Técnico

- [ ] Código solo en el repositorio privado y en tu servidor; copia diaria en tu NAS.
- [ ] La alcaldía usa el sistema por navegador; el agente de Windows se entrega compilado.
- [ ] Cuenta de Google Cloud, claves de API y llaves de cifrado a tu nombre.
- [ ] Bitácora de accesos al sistema.

## 3. Riesgos principales

| Riesgo | Cómo se evita |
|---|---|
| Que la alcaldía alegue que el software es suyo por tu contrato actual | Revisar el contrato (A); desarrollar fuera del contrato (B); registro en la DNDA con fecha anterior al piloto (A); acta de piloto (D) |
| Que copien la idea | Registro en la DNDA y de la marca; confidencialidad con terceros; no entregar código |
| Uso indebido de datos | Datos anonimizados para pruebas; autorización escrita para el piloto |
| Inhabilidad o conflicto de interés al contratar | Concepto de un abogado antes del primer contrato |
