# Ventanilla Única Inteligente — Software JRLM
## Documento de contexto completo

Autor y dueño: **Jaime Raúl López Mancipe** · Marca: **Software JRLM** (por registrar) · Versión 0.5 · 21 de octubre de 2026
Copyright © 2026 Jaime Raúl López Mancipe. Todos los derechos reservados. **Documento confidencial.**

---

## 0. Instrucciones para Claude (leer primero)

Este documento resume todo lo que el autor y Claude han desarrollado. Con él debes poder continuar el proyecto sin preguntar lo que ya está decidido.

**Forma de trabajar con el autor**
- Responde en español, corto, claro y preciso.
- Si pide una recomendación: **una sola decisión**, no varias opciones.
- Datos concretos antes que adjetivos. Sin lenguaje publicitario.
- El autor es **administrador, no programador**. Claude escribe el código; él lo administra. Explica lo técnico con palabras simples.
- Haz las preguntas necesarias cuando falte información. Las pendientes están en la sección 17.
- Antes de un cambio grande, confirma con el autor.

**Reglas que no se rompen**
1. La IA del sistema **solo clasifica y asigna**. Nunca redacta borradores ni respuestas a PQRS.
2. No usar datos reales de la ventanilla, de Génesis ni del Google Workspace de la alcaldía sin autorización escrita. Probar con datos ficticios o anonimizados.
3. No guardar en el repositorio claves de API, contraseñas, datos personales ni documentos reales. Las claves van en variables de entorno o en `.env`, que git ignora.
4. Todo archivo nuevo lleva la autoría de Jaime Raúl López Mancipe; el software es propietario.
5. Las cuentas del proyecto (GitHub, Google Cloud, Anthropic, dominio) van solo con el correo personal del autor, nunca con correos de la alcaldía.
6. Claude in Chrome solo se usa en páginas públicas y en cuentas propias del autor. No se usa en la ventanilla, en Génesis ni en el Workspace de la alcaldía hasta tener el acta del piloto firmada.

**Dónde está el código**
- Repositorio GitHub `mancipeBOT-dot/PROYECTOS`, rama `claude/municipal-single-window-system-8j87uy`, carpeta `ventanilla-unica/`.
- **El repositorio está público. Pendiente: que el autor lo ponga en privado.**

---

## 1. Qué es el proyecto

Software de autoría propia que se presta **como servicio** a alcaldías municipales de Colombia. Las alcaldías contratan el servicio (suscripción con licencia de uso), **no el desarrollo**.

**Qué hace**
1. Recibe todas las PQRS por cualquier canal.
2. Las convierte a texto (OCR → Markdown) para que la IA gaste menos tokens.
3. La IA las clasifica.
4. Las asigna a la dependencia y al funcionario.
5. Calcula la fecha límite legal en días hábiles, sin festivos.
6. Avisa en la pantalla de cada PC al inicio de cada jornada.

En el mismo servidor se conectan otros módulos: solicitudes internas, agente de actividad, Wi-Fi por identificación, inventarios, el software financiero Génesis, pagos por PSE y reportes.

**Objetivo comercial:** ser proveedor de un servicio integral para alcaldías municipales. Primero un piloto propio con datos simulados (una "proyección"); después se presenta a la alcaldía como proyecto de pago.

**Argumento de venta (medible):** hoy la asignación de PQRS tarda de 1 a 2 días y ocupa a dos personas. Con el sistema tarda minutos.

---

## 2. Por qué paga una alcaldía

| Necesidad | Riesgo si no se resuelve | Norma |
|---|---|---|
| Responder PQRS a tiempo | Sanción disciplinaria, tutelas | Ley 1755 de 2015, Ley 1952 de 2019 |
| Trazabilidad de documentos | Hallazgos de Contraloría y Procuraduría | Ley 594 de 2000 |
| Informe semestral de PQRS de Control Interno | Incumplimiento legal | Ley 1474 de 2011, art. 76 |
| Recaudo (Predial, ICA, servicios públicos) | Menos ingresos propios | Estatuto tributario municipal |
| Reportes al ordenador del gasto | Decisiones sin datos | Decreto 111 de 1996 |

---

## 3. Alcaldía piloto: situación actual (datos reales)

| Elemento | Dato |
|---|---|
| Dependencias (9) | Despacho del Alcalde, Secretaría de Gobierno, Secretaría de Hacienda, Secretaría de Planeación, Secretaría de Infraestructura, Oficina de Contratación, Unidad de Servicios Públicos, Secretaría de Desarrollo Social y Económico, Secretaría de Bienes y Servicios (solo inventario). Nombres oficiales por confirmar |
| Control Interno | Existe; recibe los avisos de PQRS vencidas (no recibe PQRS) |
| Computadores | ~3 por dependencia, Windows 11. Cada PC es de una sola persona |
| Correo | Google Workspace. **Un correo por dependencia, no por funcionario.** Un correo central recibe las PQRS y normalmente lo revisa una persona |
| Ventanilla actual | Página web: un funcionario escanea, sube y asigna la dependencia a mano. La dependencia recibe un correo con el PDF adjunto, sin enlace ni correo del ciudadano para responder. No se sabe quién la aloja |
| Entradas de PQRS | Correo central y radicación presencial (la hacen varias personas). Algunas PQRS llegan directo a una dependencia sin pasar por la ventanilla |
| Escáner | Común, hoja por hoja. Se puede instalar Google Drive para escritorio |
| Constancia al ciudadano | En papel o por correo |
| Tiempo de asignación | 1 a 2 días, con dos personas dedicadas |
| Reasignación | La dependencia la devuelve por competencia desde la ventanilla |
| Varias dependencias | Responde la primera que la recibe, si tiene competencia |
| Asignación interna | Hoy decide el jefe de la dependencia |
| Firma y envío | Firma el jefe de cada dependencia y se envía por correo electrónico |
| Prórrogas | No se usan |
| Contratistas | Existen. El seguimiento de horario se hace solo al personal de planta |
| Software financiero | **Génesis** (es la empresa proveedora). Información en la nube del proveedor. Maneja todos los recursos de Hacienda |
| Recaudo | Banco de Bogotá (PSE). Un solo banco |
| Internet | Colombia Más |
| Página web y redes sociales | Las maneja un contratista, que puede colaborar |
| Jornadas | 8:00–12:00 y 14:00–18:00 |
| Solicitudes de contratación y recursos | Hoy se hacen en persona, sin trazabilidad |
| Resolución de monitoreo | La firma el alcalde |
| Concejo y Personería | Entidades independientes. Se hace seguimiento solo a sus **dos secretarias de planta**, que están en la nómina de la alcaldía y fueron **nombradas por el alcalde** |
| Sesiones del Concejo | Ordinarias (en los periodos de ley; el autor las llamaba "sincrónicas") y extraordinarias (fuera de esos periodos; "asincrónicas") |

**Accesos del autor:** usuario en la ventanilla y en Génesis (solo valida información); contacto con los usuarios de la ventanilla; funcionario clave de cada dependencia; posible acceso al administrador de Google Workspace; dirección de la página web con acceso de usuario común. En su contrato puede usar IA para sus propias actividades.

**Vínculo del autor con la alcaldía:** contratista de prestación de servicios profesionales de asesoría. El contrato **no tiene** cláusula de propiedad intelectual ni de productos, y sus actividades no incluyen crear herramientas. El proyecto es personal; nadie se lo encargó.

---

## 4. Módulos

| # | Módulo | Qué hace |
|---|---|---|
| M1 | Ingesta y OCR | Escáner / correo / web / redes → PDF → texto → Markdown |
| M2 | Clasificación IA | Tipo de PQRS, dependencia, término, prioridad, correo de respuesta |
| M3 | Asignación y fechas | Propone funcionario, el jefe aprueba; vencimiento legal y fecha interna |
| M4 | Alertas de jornada | Pantalla completa en el PC a las 8:00 y 14:00 |
| M5 | Google Calendar / Tasks | Un calendario por dependencia; checklist diario |
| M6 | Solicitudes internas | Contratación, CDP y recursos por correo, con radicado y trazabilidad |
| M7 | Agente de actividad | Llegada, salida, tiempos muertos (> 5 min), tareas; solo personal de planta |
| M8 | Red institucional | Wi-Fi abierta sin Internet hasta autorizar cédula + equipo; bloqueo de redes sociales y WhatsApp |
| M9 | Integración financiera | Génesis en solo lectura |
| M10 | Inventarios | Entradas y salidas; consumo → gasto, devolutivo → activo |
| M11 | Pagos PSE | Banco de Bogotá, recibos con código de barras, conciliación |
| M12 | Reportes | Ordenador del gasto, secretarios, Control Interno, ciudadano |
| M13 | Secretarias Concejo / Personería | Horario, tiempos muertos y tareas: actas, citaciones, correspondencia, PQRS |

---

## 5. Servidores y respaldos

**Decisión:** producción en la nube a nombre del autor + servidor físico propio del autor para los respaldos.

**Por qué no solo un servidor físico:** si se va la luz o el Internet donde esté, el sistema se cae, y las PQRS tienen plazos legales. Ningún servidor protege el código por sí solo; lo protegen el registro, no entregar el código y el contrato de licencia.

| Componente | Especificación |
|---|---|
| Producción | Google Cloud, Compute Engine `e2-standard-4` (4 vCPU, 16 GB RAM), 200 GB SSD cifrado con llave del autor (Cloud KMS), Ubuntu Server 24.04 LTS, instantánea diaria con 30 días de retención. Cuenta y facturación a nombre del autor |
| Servidor físico propio | NAS de 2 bahías (ej. Synology DS224+), 2 × 4 TB en espejo (RAID 1), UPS de 30 minutos o más |
| Respaldo diario | 2:00 a. m., copia cifrada de la base de datos, los PDF, los Markdown y el código. Retención: 30 copias diarias y 12 mensuales. Restauración de prueba una vez al mes |
| Resultado | 3 copias en 2 lugares |
| En la alcaldía | Solo el equipo de red (mini PC con OPNsense), entregado en comodato |

**Software del servidor:** Docker Compose · PostgreSQL 16 · MinIO (archivos) · n8n instalado en el servidor (mueve información: Gmail, Drive, redes sociales, Calendar, tareas programadas) · Python + FastAPI (reglas de negocio) · Docling + EasyOCR en español (OCR; los PDF con texto se leen directo con pypdf) · API de Claude (clasificación) · React (panel web) · agente en Python compilado (.exe) para Windows 11 · OPNsense + AdGuard Home (red).

**Regla de arquitectura:** la lógica de negocio vive en el backend, no en n8n. n8n solo mueve información. La licencia de n8n permite el uso interno; si se vende como servicio a varias alcaldías desde un servidor propio, hay que revisarla o pagar la edición Enterprise.

---

## 6. Entradas de información

| Canal | Cómo entra |
|---|---|
| Correo central de PQRS | API de Gmail; el sistema lee solo ese buzón |
| Radicación presencial | Cada PQRS se escanea completa como un solo PDF en una carpeta sincronizada con Google Drive para escritorio; el sistema la lee cada minuto |
| PQRS que llegan directo a una dependencia | Regla de Gmail en el correo de cada dependencia que reenvía al correo central las que dicen "PQRS" o "derecho de petición", más un botón en el panel para radicar las entregadas en persona |
| Página web de la alcaldía | Formulario de PQRS conectado al sistema y consulta de estado por número de radicado |
| Facebook e Instagram | Mensajes privados a las páginas oficiales por la API de Meta; se radican y el ciudadano recibe su número de radicado. Los comentarios públicos solo se radican si quien maneja las redes los marca |
| WhatsApp | Fase posterior (WhatsApp Business Platform, cobra por conversación) |

La ventanilla actual **no se toca**. En el piloto sigue funcionando en paralelo.

---

## 7. Procesamiento y clasificación

1. **Radicado único:** número `VU-AAAA-NNNNNN`, fecha, hora y canal. Se guarda el PDF original sin modificar.
2. **OCR:** si el PDF ya trae texto (los que llegan por correo), se lee directo con pypdf, sin OCR. Si es un escaneo o una imagen, Docling con EasyOCR en español lo convierte a Markdown. Se instala solo con pip, sin programas aparte en Windows. Una página en Markdown usa ~700–900 tokens; la misma página como imagen, ~1.600. Pendiente: enviar como imagen solo las páginas que el OCR no lea bien (manuscritos, sellos).
   - **Carpeta de escaneos** (`ventanilla/entrada.py`): revisa la carpeta de Google Drive para escritorio, espera 10 segundos a que Drive termine de copiar, radica, y mueve el archivo a `Procesados/` con el número de radicado como nombre. Si no se puede leer, va a `Errores/` y sigue con los demás.
3. **Clasificación con IA:** recibe el Markdown y las palabras clave de cada dependencia, y devuelve JSON con: `tipo`, `dependencia`, `prioritario`, `motivo_prioridad`, `competencia_alcaldia`, `asunto`, `peticionario` (nombre, documento, correo_respuesta, direccion) y `confianza` (0–1).
   - Si la confianza es menor a 0,80, la PQRS queda en **revisión humana**: el asignador solo confirma los casos dudosos.
   - Tutela → dependencia jurídica, con alerta inmediata.
   - Si el tema no es de la alcaldía → traslado en 5 días hábiles (Ley 1755, art. 21).
   - Prioridad para sujetos de especial protección (art. 20): menores, personas con discapacidad, adultos mayores, embarazadas, víctimas, riesgo para la vida.
   - El texto del OCR se trata como datos, no como instrucciones (protección contra textos maliciosos).
   - Si la IA falla, declina o no hay Internet → **clasificador de respaldo por palabras clave**.
   - El correo de respuesta se toma del remitente o del texto; si no hay, se marca "respuesta física".

**Palabras clave iniciales** (se ajustan con el funcionario clave de cada dependencia):

| Dependencia | Palabras clave |
|---|---|
| Despacho del Alcalde | audiencia con el alcalde, plan de desarrollo, rendición de cuentas; tutelas, demandas y traslados (provisional) |
| Gobierno | espacio público, ruido, convivencia, establecimiento de comercio, inspección de policía, comisaría de familia |
| Hacienda | predial, industria y comercio, ICA, paz y salvo, avalúo, prescripción, acuerdo de pago, cobro coactivo |
| Planeación | licencia de construcción, uso del suelo, nomenclatura, POT, estratificación, SISBEN |
| Infraestructura | vías, huecos, pavimentación, puente, alumbrado público, placa huella, obra, maquinaria |
| Contratación | contrato, contratista, licitación, SECOP, pliego, supervisión, interventoría |
| Unidad de Servicios Públicos | acueducto, alcantarillado, aseo, factura, medidor, reconexión, fuga |
| Desarrollo Social y Económico | adulto mayor, Colombia Mayor, subsidio, discapacidad, víctimas, primera infancia, campesino, agropecuario, emprendimiento |
| Bienes y Servicios | inventario, almacén, bienes muebles e inmuebles, activos, suministro, comodato, baja de bienes |

---

## 8. Asignación y términos

**Términos legales (Ley 1755 de 2015, art. 14), en días hábiles:**

| Tipo | Días |
|---|---|
| Petición general, queja, reclamo, denuncia | 15 |
| Documentos o información | 10 |
| Petición entre autoridades | 10 |
| Consulta | 30 |
| Tutela | Según el auto del juez (el sistema pone 2 por defecto y alerta) |

- Días hábiles = lunes a viernes sin festivos de Colombia. El conteo empieza el día hábil siguiente a la radicación.
- **Fecha interna = dos tercios del término** (día 10 de 15), para dejar tiempo de revisión y firma.
- **Funcionario:** el sistema propone, dentro de la dependencia, al que maneja el tema; si hay empate, al de menos PQRS abiertas. **El jefe no recibe PQRS automáticamente.**
- **Aprobación del jefe:** el jefe ve las asignaciones pendientes de su dependencia y acepta o cambia el funcionario. La PQRS aparece en el plan del funcionario desde el primer momento, para no perder días.
- **Devolución por competencia:** si la dependencia dice "no es mía", indica el motivo y la PQRS vuelve al asignador. **Los términos no se reinician.** Queda registrado qué dependencias la devolvieron.
- **Plan diario:** las PQRS de cada funcionario se reparten entre los días hábiles que quedan hasta la fecha interna, en bloque de mañana o de tarde.

---

## 9. Seguimiento

| Elemento | Funcionamiento |
|---|---|
| Alerta de jornada | Pantalla completa a las 8:00 y 14:00, o en el primer inicio de sesión después. Rojo: vence en 3 días hábiles o menos. Amarillo: en curso. Verde: nueva. Se cierra con "Entendido", que queda registrado |
| Calendario | Un calendario de Google por dependencia, con el responsable de cada PQRS |
| Checklist | Google Tasks por dependencia |
| Constancia de radicado | Correo automático al ciudadano con el número de radicado y la fecha límite. Es un mensaje fijo, no una respuesta |
| Escalamiento | 3 días hábiles antes del vencimiento → jefe. Vencida → Control Interno |
| Cierre | El jefe firma y se envía desde el correo de la dependencia con el número de radicado en el asunto; el sistema detecta ese correo y cierra la PQRS. Si no lo detecta, se cierra a mano con el número de oficio |
| Consulta ciudadana | Estado por radicado en la página web, sin datos internos |
| Procesos de cada dependencia | Después del piloto se modelan uno por uno (ej. licencias de construcción) y se conectan en un flujo de toda la alcaldía |

---

## 10. Solicitudes internas entre dependencias

1. La dependencia envía un correo a un buzón único con asunto estándar: `[CDP] Secretaría X - objeto`.
2. El sistema la radica, adjunta los documentos y crea el expediente.
3. Ruta: dependencia → Hacienda (CDP) → Contratación (contrato) → Hacienda (RP) → pago.
4. Cada paso registra responsable, fecha de entrada, fecha de salida y estado.
5. Lo pendiente aparece en el checklist diario del responsable.

---

## 11. Agente de actividad y tiempos muertos

Es el mismo programa que muestra las alertas. Como cada PC es de una sola persona, el equipo identifica al funcionario.

| Dato | Cómo se obtiene |
|---|---|
| Inicio de labores | Primer inicio de sesión o desbloqueo del día; antes no se mide nada |
| Aplicación o página activa | Ventana en primer plano, cada 60 segundos |
| Actividad | Último uso de teclado o mouse |
| Tiempo muerto | Más de 5 minutos sin actividad, o más de 5 minutos fuera de las aplicaciones y páginas asignadas |
| Fin de labores | Cierre de sesión, bloqueo o apagado |

- **No** registra teclas, **no** toma capturas de pantalla, **no** lee documentos ni correos.
- **Solo personal de planta.** A los contratistas no se les mide horario: no hay subordinación y medirlo puede configurar una relación laboral. En sus PC solo van las alertas de PQRS.
- **Secretarias del Concejo y de la Personería:** son de planta y las nombró el alcalde, así que la misma resolución las cubre. Se mide llegada, salida, tiempos muertos y tareas: actas de sesiones ordinarias y extraordinarias, citaciones, correspondencia y PQRS.
- **Reportes:** diario por funcionario y semanal por dependencia.
- **Antes de instalar:** resolución del alcalde, política de tratamiento de datos y aviso a cada funcionario (Ley 1581 de 2012), y socialización. El reporte sirve para evaluar, no sanciona por sí solo.

---

## 12. Wi-Fi por identificación y bloqueo de páginas

**Decisión:** se administra desde el panel del sistema, como parte del servicio. En la alcaldía se instala un mini PC del autor (4 puertos de red, 8 GB RAM) con OPNsense (firewall y portal) y AdGuard Home (filtro), controlados por sus API.

**Cómo obtiene acceso un funcionario:**
1. Se conecta a la red abierta: no pide contraseña, pero no hay Internet.
2. Una página le pide la cédula.
3. El sistema verifica que es un funcionario activo y guarda la identificación del equipo (dirección MAC).
4. El jefe o el administrador aprueba en el panel.
5. El equipo queda con el perfil de su dependencia. Si el funcionario se retira, sus equipos pierden acceso.

| Perfil | Bloqueado |
|---|---|
| Estándar | Facebook, Instagram, TikTok, X, WhatsApp (app y web), YouTube, video, juegos, apuestas |
| Comunicaciones | Igual al estándar, pero permite redes sociales para las cuentas oficiales |
| Hacienda / Tesorería | Estándar + PC solo por cable |

**Cómo se bloquea:** filtro DNS por perfil, bloqueo de los rangos IP de Meta (AS32934) y bloqueo de DNS cifrado (DoH/DoT) y VPN conocidas.

**Limitaciones:**
- Los celulares cambian su dirección MAC por red; al registrarlos hay que desactivar la "dirección privada".
- La MAC se puede copiar; por eso Hacienda va por cable.
- Con datos móviles propios no hay control.

---

## 13. Finanzas: Génesis, inventarios y PSE

**Génesis** (nube del proveedor), **solo lectura**, solicitado por la alcaldía al proveedor y con un usuario propio del sistema (nunca con las credenciales del autor). Por orden de preferencia:
1. API del proveedor.
2. Reportes exportados (CSV o Excel) cada noche a una carpeta de Drive.
3. Si no hay ninguna de las dos, Hacienda los sube a esa carpeta una vez al día.

Datos: Predial, ICA, cartera, servicios públicos y presupuesto (CDP, RP, obligaciones, pagos).

**Inventarios (Bienes y Servicios)**

| Tipo de bien | Al entrar | Al salir | Después |
|---|---|---|---|
| Consumo (papelería, aseo, repuestos) | Inventario de materiales y suministros | **Gasto** de la dependencia que lo recibe | Sale del inventario |
| Devolutivo (computadores, muebles, vehículos) | Bienes en bodega | **Activo** en servicio, con placa, dependencia y responsable | Depreciación mensual; traslados de responsable; sale solo con acta de baja (el valor no depreciado queda como pérdida) |

- Valoración por costo promedio ponderado. Cada entrada exige soporte: factura, contrato o acta.
- Para un elemento nuevo, el sistema sugiere devolutivo si dura más de 12 meses y supera el valor mínimo de la política contable; si no, consumo.
- Reportes: gasto por dependencia, activos por dependencia y responsable, saldo del almacén.
- Las cuentas contables se toman del plan de cuentas de Génesis.
- Es el modelo para el resto: cada dependencia ve su gasto y sus activos, y el ordenador del gasto ve el total.

**PSE con el Banco de Bogotá**
1. Recibo con código de barras GS1-128.
2. El ciudadano paga por PSE o en una oficina del banco.
3. El banco entrega el archivo diario de recaudo (formato Asobancaria 2001).
4. El sistema concilia los pagos y deja el reporte para cargar en Génesis.

Trámite: la Tesorería lo solicita al ejecutivo de cuenta del Banco de Bogotá.

---

## 14. Reportes

| Destinatario | Contenido | Frecuencia |
|---|---|---|
| Ordenador del gasto | Ejecución presupuestal, recaudo vs. meta, PQRS vencidas por dependencia, solicitudes internas detenidas, gasto y activos por dependencia | Semanal |
| Secretarios / jefes | PQRS por funcionario, vencimientos, solicitudes internas, tiempos muertos | Diario |
| Control Interno | Informe de PQRS (Ley 1474, art. 76) y avisos de vencidas | Semestral con corte mensual |
| Funcionario | Sus tareas del día y su reporte de actividad | Diario |
| Ciudadano | Estado de su PQRS | En línea |

Formato: una página, tablas y semáforo, exportable a PDF.

---

## 15. Seguridad y datos personales

- HTTPS en todo; discos y copias cifrados con llaves del autor.
- Al servidor solo entra el autor (llave SSH y verificación en dos pasos); solo el puerto HTTPS queda abierto.
- **Usuario y contraseña propios del sistema por funcionario**, con verificación en dos pasos, porque el correo de Google es por dependencia. Cada uno ve solo su dependencia; el ordenador del gasto ve todo.
- Bitácora de quién vio, cambió, reasignó o descargó cada documento.
- La alcaldía es **responsable** de los datos y el autor es **encargado del tratamiento** (Ley 1581 de 2012), con un acuerdo firmado.
- La IA solo recibe el texto necesario. La API de Claude no usa esos datos para entrenar.
- Al terminar el servicio, los datos se entregan en CSV y PDF en 30 días y se borran.

---

## 16. Propiedad intelectual y protección del autor

**Qué protege la ley:**
- El código, los documentos y los diagramas tienen derecho de autor desde que se crean (Ley 23 de 1982; Decisión Andina 351 de 1993).
- **La idea no se protege** (Decisión 351, art. 7).
- El software no es patentable como tal (Decisión 486, art. 15).
- La marca se registra ante la SIC y dura 10 años renovables.

**Riesgo principal:** la Ley 23 de 1982, art. 20 (modificado por la Ley 1450 de 2011, art. 28) presume que lo creado en cumplimiento de un contrato de prestación de servicios es del contratante, salvo pacto escrito. El proyecto no está cubierto: el contrato del autor es de asesoría, sin cláusula de propiedad intelectual, y no incluye crear herramientas.

**Sobre el código escrito por IA:**
- Lo claramente humano es del autor: la idea, el diseño, las decisiones y los documentos.
- Los términos de Anthropic le dejan al usuario los derechos sobre lo que se genera.
- La protección más fuerte es que el código no salga del servidor del autor: así queda como **secreto empresarial** (Decisión 486, art. 260).
- Guardar las conversaciones y el historial de GitHub como prueba de que el autor dirigió el trabajo.

**Lista de verificación**
- [ ] Poner el repositorio de GitHub en privado y activar la verificación en dos pasos.
- [ ] Registrar en la DNDA (gratis, en línea) el documento y la imagen del flujo como obra literaria no publicada; después, el software en cada versión mayor.
- [ ] Buscar antecedentes de la marca "Software JRLM" en la SIC y radicarla a nombre del autor, en las clases 9 y 42.
- [ ] Todas las cuentas con el correo personal. Ningún archivo del proyecto en el Drive o el correo de la alcaldía.
- [ ] Desarrollar fuera del horario del contrato, en equipo propio.
- [ ] No copiar datos de Génesis ni de la ventanilla con las credenciales de contratista (Ley 1273 de 2009, art. 269A; Ley 1581 de 2012). Conocer cómo funcionan no es copiarlos.
- [ ] Acuerdo de confidencialidad con el administrador de la página web y con cualquier colaborador; cesión de derechos si alguien escribe código o documentos.
- [ ] Antes del piloto: **acta firmada por el alcalde** que diga que el software es del autor (con su número de registro en la DNDA), que el piloto es temporal sin cesión de derechos ni entrega de código, que la alcaldía autoriza el uso de sus datos y que hay confidencialidad. Que la revise un abogado.
- [ ] Para vender: RUT con actividad de software; empresa (SAS) cuando llegue el primer contrato. La marca y el software quedan a nombre del autor como persona y él le da licencia a la SAS. Facturación electrónica DIAN, inscripción en SECOP II, RUP si se exige y pólizas cuando el contrato las pida.
- [ ] Contrato con cada alcaldía como licencia de uso: software preexistente del autor, sin cesión, sin entrega de código, prohibido copiar o descompilar, datos devueltos al terminar.
- [ ] Si una alcaldía exige garantía de continuidad: depósito del código ante notario.
- [ ] Ser titular registrado ayuda a justificar la contratación directa cuando no hay pluralidad de oferentes (Decreto 1082 de 2015, art. 2.2.1.2.1.4.8); confirmarlo con un abogado en cada caso.
- [ ] Revisión de seguridad independiente antes de usar datos reales.

---

## 17. Estado del código (prototipo, Fase 1)

Ubicación: `ventanilla-unica/backend/` (Python 3.11+). Almacenamiento en memoria por ahora; luego PostgreSQL.

| Archivo | Qué hace |
|---|---|
| `ventanilla/terminos.py` | Días hábiles con festivos de Colombia (librería `holidays`), vencimiento y fecha interna |
| `ventanilla/clasificador.py` | IA con la API de Claude (salida JSON estructurada, respaldo automático del servidor si la IA declina) + clasificador por palabras clave |
| `ventanilla/asignacion.py` | Funcionario por tema y carga, plan diario por jornada, alertas, escalamiento |
| `ventanilla/servicio.py` | Radicar → revisión → asignar → aprobación del jefe → devolución por competencia → cerrar; consulta del ciudadano |
| `ventanilla/ocr.py` | PDF con texto → lectura directa; escaneo o imagen → OCR con Docling + EasyOCR (español) |
| `ventanilla/entrada.py` | Radicación automática desde la carpeta de escaneos (Drive para escritorio) |
| `ventanilla/inventario.py` | Entradas, salidas, gasto, activos, depreciación, traslados, bajas y reportes |
| `ventanilla/api.py` | API web (FastAPI) |
| `ventanilla/simulacion.py` | Piloto simulado con 22 PQRS ficticias |
| `datos/alcaldia.json` | Las 9 dependencias con un jefe y 3 funcionarios ficticios cada una, y correo por dependencia |
| `datos/pqrs_prueba.json` | 22 PQRS inventadas con la respuesta esperada |
| `tests/` | 37 pruebas automáticas (36 normales + 1 de OCR real que se activa con `VUI_PRUEBA_OCR=1`) |

**Resultado de la simulación (palabras clave, sin IA):** dependencia correcta en 21 de 22 (95 %); la que falló quedó en revisión humana, así que ninguna se asignó mal. Tipo correcto en 22 de 22. En revisión humana: 4 de 22. La IA real no se ha probado aún (falta la clave de la API).

**IA:**
- Modelo por defecto `claude-opus-5-5`; se cambia con la variable `VUI_MODELO`.
- Costo estimado (~1.700 tokens de entrada y ~500 de salida por PQRS): `claude-opus-5-5` ~US$0,017 por PQRS (~US$8,5 por 500 al mes); `claude-haiku-5-5` ~US$0,0004 (~US$0,2 por 500 al mes). Hay que medirlo con PQRS reales antes de elegir.

**Cómo ejecutarlo (Windows):**
```
cd ventanilla-unica\backend
python -m venv .venv
.venv\Scripts\pip install -e ".[dev,ocr]"
.venv\Scripts\python -m pytest
.venv\Scripts\python -m ventanilla.simulacion
.venv\Scripts\uvicorn ventanilla.api:app --reload
.venv\Scripts\python -m ventanilla.entrada --carpeta "G:\Mi unidad\Escaneos PQRS" --cada 60
```
Con IA: definir la variable `ANTHROPIC_API_KEY` y agregar `--ia` a la simulación.

**Otros archivos del repositorio:**
- `ventanilla-unica/documento_funcionamiento.pdf` (14 páginas; fuente `fuentes/documento.html`; se regenera con `node fuentes/render.js`).
- `flujo_ventanilla_unica.png` (imagen del flujo).
- `propiedad-intelectual.md`, `plan-de-inicio.md`, `pasar-a-escritorio.md`, `preguntas.md`, `LICENCIA.md`.
- `CLAUDE.md` en la raíz.
- `diagramas/flujo_licencias_construccion.pdf` (proceso de Planeación ya mapeado).

---

## 18. Cuentas y herramientas del autor

- **Cuenta de Anthropic:** la actual, con el correo personal. Cuando exista la SAS, se crea una organización aparte.
  - **Suscripción de Claude:** para que Claude Code programe.
  - **API (console.anthropic.com):** para que el sistema clasifique. Se paga por uso; poner un límite de gasto mensual y crear una clave llamada `ventanilla-desarrollo`, que nunca se pega en chats ni en archivos.
- **Trabajo desde el computador:** app de escritorio de Claude (Claude Code), GitHub Desktop, Python 3.12+, Node.js LTS y la extensión Claude in Chrome.
- **Claude in Chrome:**
  - Sí: página web pública y redes de la alcaldía, y las cuentas del autor (GitHub, Google Cloud, Anthropic, SIC, DNDA).
  - No (hasta el acta firmada): ventanilla, Génesis y Workspace de la alcaldía. Para esas, usar capturas con los datos tachados.

---

## 19. Fases

| Fase | Alcance | Criterio para pasar |
|---|---|---|
| 0. Base | Registro en la DNDA, repositorio privado, servidores, palabras clave | Software registrado, respaldo probado |
| 1. Piloto propio (proyección) | Entradas, OCR, IA, asignación, alertas, Calendar con datos simulados o anonimizados | ≥ 90 % de asignaciones correctas; 100 % con fecha límite |
| 2. Piloto en la alcaldía | Hacienda y Planeación, 6 PC, 4 semanas en paralelo con la ventanilla actual (2 semanas comparando, luego asigna el sistema) | Mismo criterio |
| 3. Toda la alcaldía | 9 dependencias y página web | Mismo criterio |
| 4. Redes sociales | Facebook e Instagram | Mensajes radicados con constancia |
| 5. Actividad | Agente y secretarias del Concejo y la Personería | Resolución firmada; agente instalado en los PC de planta |
| 6. Wi-Fi | Equipo de red y panel | Ningún equipo sin registro con Internet |
| 7. Financiero | Génesis, inventarios, solicitudes internas, reportes | Reporte semanal automático |
| 8. Pagos | PSE Banco de Bogotá | Conciliación diaria automática |

---

## 20. Preguntas pendientes para el autor

**Datos que faltan**
1. Enlace de la página web de la alcaldía (para identificar en qué está hecha).
2. Fotos de la etiqueta del router y de los puntos de Wi-Fi (marca y modelo).
3. 10 a 20 PQRS escaneadas sin datos personales, con la dependencia a la que fueron.
4. Nombres oficiales exactos de las 9 dependencias.
5. ¿Qué reportes exporta Génesis y si ofrece API?

**Estructura organizacional**

6. ¿Hay organigrama y manual de funciones? ¿Están publicados?
7. Por dependencia, ¿cuántos funcionarios de planta y cuántos contratistas?
8. ¿Un solo jefe por dependencia, o hay coordinadores?
9. ¿El ordenador del gasto es solo el alcalde, o hay secretarios con delegación?
10. ¿Quién maneja lo jurídico (tutelas, demandas, traslados)? Hoy el sistema lo envía al Despacho del Alcalde de forma provisional.
11. ¿Control Interno es una persona de planta? ¿De quién depende?

**Horarios y novedades**

12. ¿Hay horarios distintos, medio tiempo o trabajo de campo?
13. ¿Cómo se registran las vacaciones, los permisos y las incapacidades? Sin eso, el sistema contaría tiempo muerto a quien no está.
14. ¿Cómo se mide hoy el trabajo de quien sale a terreno?

**Inventarios**

15. ¿Cuál es el valor mínimo de la política contable para que un bien sea activo?
16. ¿Génesis tiene módulo de almacén, o el inventario se lleva en Excel?
17. ¿Los bienes tienen placa? ¿El inventario físico está al día?
18. ¿Quién recibe en el almacén y quién firma las salidas?

**Concejo y Personería**

19. ¿En cuántos días debe quedar lista el acta después de cada sesión?
20. ¿Con cuántos días de anticipación se envían las citaciones?
21. ¿Su correspondencia entra por la misma ventanilla de la alcaldía?

---

## 21. Siguientes pasos de desarrollo

1. Lectura del correo central (Gmail). (El OCR y la carpeta de escaneos ya están hechos.)
2. Probar la clasificación con la IA real usando las PQRS anonimizadas y medir el costo.
3. Base de datos PostgreSQL y panel web (asignador, jefes, funcionarios, ordenador del gasto).
4. Agente de Windows: alertas de jornada y actividad.
5. Módulo de las secretarias del Concejo y la Personería: sesiones, actas, citaciones, correspondencia.
6. Integración con Google Calendar y Tasks.
