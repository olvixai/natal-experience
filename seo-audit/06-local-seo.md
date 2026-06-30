# Auditoría de Local SEO — NatalExperience Tours

**Sitio auditado:** https://natal-experience.vercel.app/ (dominio de producción `natalexperience.com.br` aún no resuelve en DNS — hallazgo crítico técnico ya cubierto por otro agente, no se repite aquí salvo impacto en señales locales)
**Código fuente analizado:** `E:\ANTIGRAVITY\NATALEXPERIENCE`
**Fecha de auditoría:** 2026-06-26
**Negocio:** NatalExperience Tours — agencia de tours / operador turístico físicamente operativo en Natal, RN, Brasil
**Tipo de negocio detectado:** Hybrid (brick-and-mortar + Service Area Business)

---

## 1. Local SEO Score: 21 / 100

| Dimensión | Peso | Puntuación (0-100) | Puntos ponderados |
|---|---|---|---|
| GBP Signals | 25% | 0 | 0.0 |
| Reviews & Reputation | 20% | 15 | 3.0 |
| Local On-Page SEO | 20% | 55 | 11.0 |
| NAP Consistency & Citations | 15% | 25 | 3.75 |
| Local Schema Markup | 10% | 0 | 0.0 |
| Local Link & Authority Signals | 10% | 30 | 3.0 |
| **TOTAL** | 100% | — | **20.75 ≈ 21** |

**Lectura del score:** el sitio tiene un punto de partida razonable en contenido on-page local (páginas dedicadas por destino, NAP visible y consistente en el HTML), pero parte de **cero absoluto** en las dos dimensiones de mayor peso combinado en el ecosistema de descubrimiento local real — GBP (25%) y Schema (10%) — y muy débil en Reviews (20%). Esto es típico de un sitio "pre-lanzamiento" que aún no ha iniciado su huella local fuera del propio dominio. El score es bajo porque la mayoría de los pesos dependen de señales **externas al sitio** (Google Business Profile, reseñas verificables, citations) que hoy no existen, no porque el sitio en sí esté mal construido a nivel de contenido.

---

## 2. Tipo de negocio y vertical de industria

**Tipo de negocio:** Hybrid.
- Dirección física visible y completa en footer global y en `contato.html`: `Rua Túlio Fernandes, 415 - Praia do Meio, Natal - RN, 59010-038, Brasil`.
- Lenguaje de área de servicio también presente: tours hacia Pipa, Maracajaú, São Miguel do Gostoso, Galinhos, Perobas, e incluso "Rota Natal-Fortaleza" (cruza límites estaduales). El negocio opera *desde* una base física pero *sirve* una región amplia del litoral de RN — el patrón clásico de un operador de tours.
- **Nota crítica:** en `contato.html` hay un comentario explícito en el código: `<!-- Map removed per user request -->`. Es decir, en algún momento existió o se consideró un Maps embed y fue retirado deliberadamente. Esto es contraproducente para SEO local — un negocio brick-and-mortar/hybrid debería mostrar el mapa de su ubicación física. Recomendamos revertir esta decisión (ver checklist).
- El enlace de dirección en el footer (`<a href="#">📍 Rua Túlio Fernandes...</a>`) no enlaza a Google Maps — es un placeholder muerto, perdiendo la oportunidad más simple y de mayor impacto: un enlace `https://maps.google.com/?q=` o, mejor, el enlace directo al Place ID de Google Business Profile una vez creado.

**Vertical de industria:** Operador turístico / agencia de viajes receptiva (Tour Operator / Travel Agency), con fuerte componente de **Home Services-like local intent** (transporte/transfer) y **actividades de aventura/naturaleza** (buggy, mergulho, veleiro, voo de helicóptero). No encaja en ninguna de las 6 verticales estándar del framework (restaurante, salud, legal, home services, real estate, automotive) — es la vertical de **turismo/tour operator**, que tiene su propio patrón de schema (`TouristTrip`, `TravelAgency`, `LocalBusiness` + subtipo, `Trip`) y de citations (directorios de turismo regional, OTAs, TripAdvisor) en vez de los citation sources genéricos de Yelp/BBB.

Señales de industria confirmadas en el código:
- Contenido por destino/excursión (`/passeios/*.html`, `/experiencias-exclusivas/*.html`)
- WhatsApp como canal de conversión primario (`data-whatsapp` en CTAs)
- Lenguaje de "passeio", "roteiro sob medida", "guias com certificações em turismo de aventura"
- Sin reservas online tipo motor de e-commerce — confirma que es Local Service / lead-gen, no e-commerce puro, tal como se indicó en el contexto de la tarea.

---

## 3. Investigación de Google Business Profile existente

**Resultado: no se encontró evidencia de un Google Business Profile (Perfil de Negocio de Google) activo para "NatalExperience Tours" en Natal, RN.**

Metodología y limitación honesta: Google Search y Google Maps bloquearon el fetch automatizado con una pantalla de consentimiento de cookies (`consent.google.com`), por lo que no pude renderizar resultados nativos de Maps/Search directamente. Se intentó vía Bing y DuckDuckGo como proxies de verificación:
- Bing: cero resultados relevantes para `"NatalExperience Tours" Natal RN` (resultados devueltos fueron de herramientas de test de velocidad de internet, sin relación).
- DuckDuckGo: **"No results found for 'NatalExperience Tours'"** — confirmación explícita de cero indexación bajo ese nombre exacto.

Esto es coherente con el resto de la evidencia ya confirmada por el otro agente (dominio de producción sin DNS, redes sociales del footer son placeholders `#` sin URL real). **Conclusión: con altísima probabilidad no existe un GBP creado, o si existe fue creado sin ninguna actividad de optimización ni vinculación al sitio/redes, por lo que es efectivamente invisible.**

### Recomendación crítica (la de mayor impacto de todo este informe)

Crear/reclamar el Perfil de Negocio de Google **antes** de cualquier otra iniciativa de Local SEO, porque:
1. Es el dimension de mayor peso del scorecard (25%) y hoy aporta 0 puntos.
2. El **factor #1 de ranking en Local Pack 2026 (Whitespark)** es la categoría primaria de GBP (score 193) — sin perfil no hay categoría, no hay Local Pack, no hay Maps.
3. Verificación de negocio en Brasil vía Google normalmente requiere prueba de dirección (correo postal con código, videollamada, o Search Console si hay sitio verificado) — el proceso puede tardar 1-4 semanas, por lo que cuanto antes se inicie, antes empieza a acumular antigüedad/señales de confianza.
4. La regla de los 18 días de Sterling Sky sobre velocidad de reseñas **no puede empezar a aplicar** hasta que exista el perfil donde recibir esas reseñas.

**Pasos de creación recomendados:**
- Categoría primaria sugerida: **"Tour operator"** (o "Agência de turismo" en la taxonomía PT-BR de Google). Evaluar categorías secundarias: "Tour agency", "Travel agency", "Adventure sports center" (dado el peso de buggy/mergulho/voo de helicóptero).
- Usar el NAP exacto confirmado en el sitio (ver sección 4) de forma idéntica, carácter por carácter.
- Subir fotos reales de los tours (no solo banco de imágenes/render) — la sección "Photo evidence" de GBP es una señal de confianza fuerte y barata de conseguir dado que ya hay gran cantidad de imágenes propias en `/img/` (pipa_1-5.jpg, maracajau_*, galinhos.png, gostoso_main.png, etc.) que sugieren que sí hay material visual propio que podría reutilizarse en GBP.
- Activar Google Posts desde el día 1, vinculados a las páginas de destino existentes (Pipa, Maracajaú, Galinhos, São Miguel do Gostoso).
- Vincular el perfil al sitio web real (`https://natal-experience.vercel.app/` mientras el dominio definitivo no resuelva) y mantenerlo sincronizado cuando `natalexperience.com.br` entre en producción — un cambio de URL en GBP sin previo aviso genera fricción de confianza.

---

## 4. Panorama competitivo en el nicho (passeio de buggy Natal / mergulho Maracajaú / tours Natal RN)

**Limitación metodológica importante:** los intentos de obtener el Local Pack en vivo de Google para estas queries fallaron por el muro de consentimiento de cookies de Google, y los intentos vía TripAdvisor devolvieron contenido cacheado/incorrecto del motor de fetch (la página de "Natal, RN" resolvía erróneamente a contenido de Campo Grande, MS, en varios intentos). No se debe interpretar nada de esta sección como una posición de ranking verificada en tiempo real — se recomienda verificación manual humana en una sesión de navegador real, en modo incógnito, geolocalizada en Natal/Brasil, antes de fijar metas de "superar a X posición".

Sí se logró verificar en vivo un competidor real del nicho de buceo en Maracajaú:

**Maracajaú Diver** (verificado por fetch directo):
- Teléfono fijo local con DDD 84 (`(84) 3223-6866`) además de móvil — señal de presencia física antigua y estable, fuerte para confianza de NAP.
- Presencia activa confirmada en Facebook, Instagram y **TripAdvisor con cuenta verificada y reseñas de visitantes**.
- Modelo de negocio especializado (un solo destino, un solo tipo de actividad) — esto le permite dominar long-tail muy específico ("mergulho Maracajaú", "batismo de mergulho Maracajaú") con menos dilución temática que un generalista.

**Patrón competitivo típico de este nicho en Natal/RN (basado en conocimiento de dominio sobre el mercado turístico de Natal, a verificar puntualmente):**

Los operadores que dominan el Local Pack / Maps en passeio de buggy y tours en Natal comparten consistentemente estas señales:
1. **Volumen de reseñas en Google de 3 a 4 cifras** (cientos a miles), acumuladas durante años, con velocidad sostenida (no picos artificiales).
2. **Categoría primaria correcta y específica** en GBP — "Tour operator" o "Excursion agency", no "Travel agency" genérico cuando el negocio es operador directo (no solo revendedor).
3. **Decenas a cientos de fotos subidas por el propio negocio y por usuarios** — el algoritmo de Maps pondera fotos de clientes como señal de actividad real reciente.
4. **Listados activos en TripAdvisor y Booking/GetYourGuide/Civitatis** como agregadores de reseñas adicionales, todos con el mismo NAP.
5. **Respuesta a reseñas (positivas y negativas)** dentro de pocos días — señal de gestión activa que Google y los usuarios valoran.
6. **Multilingüismo**: dado el alto componente de turismo internacional en Natal (confirmado en el propio sitio: testimonios de Portugal y Argentina), los líderes del nicho suelen tener reseñas y a veces ficha de GBP en PT, EN y ES.
7. Teléfono con DDD 84 visible y clicable, coherente entre sitio, GBP y redes — exactamente lo que NatalExperience Tours ya tiene a nivel de sitio, pero le falta replicar en GBP/citations.

**Brecha actual de NatalExperience Tours frente a este patrón:** el negocio parte de cero en los 6 puntos anteriores. La buena noticia es que el contenido base (páginas por destino, fotografía propia, testimonios con nombre/origen aunque no verificados) ya cubre el insumo necesario para alimentar un GBP competitivo rápidamente — el trabajo pendiente es de **distribución y verificación**, no de creación de contenido desde cero.

---

## 5. Auditoría de consistencia NAP

| Campo | Footer global (43 páginas) | `contato.html` (bloque "Informações de Contato") | Formato esperado para GBP |
|---|---|---|---|
| Nombre | NatalExperience Tours | NatalExperience Tours | Coincide — usar exactamente así, sin sufijos extra tipo "Ltda" salvo que conste en el CNPJ |
| Dirección | Rua Túlio Fernandes, 415 - Praia do Meio, Natal - RN, 59010-038, Brasil | Rua Túlio Fernandes, 415 - Praia do Meio, Natal - RN, 59010-038, Brasil | Coincide. Formato es correcto para BR (logradouro, número, bairro, cidade - UF, CEP, país) |
| Teléfono | +55 84 99986-8411 (también `tel:+5584999868411`) | +55 84 99986-8411 (también `tel:+5584999868411`) | Coincide |
| Email | natalexperiencetours@gmail.com | natalexperiencetours@gmail.com | Coincide, pero ver nota abajo |

**Conclusión de consistencia interna: NAP 100% consistente dentro del propio sitio.** No se detectaron discrepancias entre footer y página de contacto, ni entre `tel:` href y texto visible. Esto es una base sólida y poco común — muchos sitios fallan justo aquí.

**Validación del teléfono +55 84 99986-8411:**
- `+55` = código de país Brasil. Correcto.
- `84` = DDD (código de área) de Rio Grande do Norte, que cubre Natal y toda la región metropolitana, incluyendo Maracajaú/Maxaranguape y Pipa/Tibau do Sul. **Es coherente y esperado** que un negocio de Natal use DDD 84.
- `99986-8411` = 9 dígitos comenzando en 9, formato correcto de número móvil brasileño post-2012 (todos los móviles en Brasil migraron a 9 dígitos). Es un número de **WhatsApp/móvil**, no de línea fija — coherente con el hecho de que el sitio usa WhatsApp como canal de conversión principal, pero compárese con el competidor verificado (Maracajaú Diver) que expone *además* un fijo con DDD 84 (3223-xxxx). Un número fijo adicional aporta una señal de "negocio establecido con oficina física" que un número 100% móvil no transmite con la misma fuerza ante usuarios ni ante el proceso de verificación de GBP.

**Hallazgos de riesgo para consistencia NAP futura (no son discrepancias hoy, pero son vulnerabilidades):**

1. **Email genérico de Gmail** (`natalexperiencetours@gmail.com`) en lugar de un dominio corporativo propio (`contato@natalexperience.com.br`). Ya señalado en el contexto de la tarea como hallazgo, se reitera aquí porque también afecta la verificación de GBP: Google Business Profile no exige email corporativo, pero los formularios de citations de turismo (Setur-RN, cámaras de comercio) y agregadores B2B (GetYourGuide, Civitatis, Booking Experiences) sí suelen pedir o priorizar dominio propio como señal de legitimidad empresarial. Migrar a email corporativo en cuanto el dominio resuelva es recomendable.

2. **Inconsistencia de antigüedad del negocio detectada en el propio código** (no es NAP estricto, pero es una señal de confianza adyacente que un revisor humano o un crawler de IA detectaría igual que detecta discrepancias NAP):
   - Footer global (todas las páginas): *"Há mais de 18 anos criando experiências..."*
   - `quem-somos.html` (meta description, bio del fundador "Junior", y contador animado de estadísticas): *"mais de 30 anos de experiência"*, contador `data-counter="30"`.
   - Esta discrepancia de "18 años" vs "30 años" es exactamente el tipo de señal contradictoria que reduce confianza — tanto para un usuario que lee ambas páginas como, potencialmente, para sistemas de verificación de Google que cruzan información pública (registros CNPJ, antigüedad de dominio, fecha de fundación declarada). **Se recomienda unificar esta cifra en todo el sitio antes de declarar cualquier antigüedad en el GBP** (el campo "año de apertura" en GBP también deberá ser consistente con esta cifra).

3. **Ningún enlace de dirección apunta a un mapa real** — el placeholder `href="#"` en el ícono de dirección debe convertirse en enlace real a Google Maps / Place ID en cuanto exista el GBP.

4. **NAP no está aún replicado en ninguna fuente externa** (no hay GBP, no hay redes sociales reales, no hay citations) — por definición no puede haber discrepancias *entre fuentes* todavía, pero tampoco hay ninguna validación cruzada de la dirección. El riesgo real aparecerá en el futuro si, al crear el GBP o las citations, alguien introduce el NAP con variaciones de formato (ej. "R. Túlio Fernandes" vs "Rua Túlio Fernandes", o "RN" vs "Rio Grande do Norte" vs omitir el estado). **Recomendación: documentar el NAP canónico exacto (ver bloque abajo) y usarlo carácter por carácter en cada citation nueva.**

**NAP canónico recomendado para usar en todas las citations futuras (copiar-pegar exacto):**
```
NatalExperience Tours
Rua Túlio Fernandes, 415 - Praia do Meio, Natal - RN, 59010-038, Brasil
+55 84 99986-8411
```

---

## 6. Validación de Local Schema (LocalBusiness / TravelAgency)

Confirmado por grep en todo el repositorio: **no existe ningún bloque `application/ld+json` con tipo `LocalBusiness`, `TravelAgency`, `TouristTrip` ni ninguna variante de Schema.org en el sitio actualmente.** Otro agente cubre el detalle técnico completo de schema; a nivel de impacto **local** específicamente:

- Sin schema `LocalBusiness`/subtipo, Google no tiene una fuente estructurada que confirme NAP, horario o geo-coordenadas independientemente del GBP — esto retrasa o debilita la asociación entre el sitio web y el futuro Perfil de Negocio (el "entity matching" que Google hace entre web y Maps).
- Subtipo recomendado: no usar `LocalBusiness` genérico. Lo correcto para esta industria es `TravelAgency` (subtipo de `LocalBusiness` en Schema.org) como entidad raíz, y opcionalmente complementar las páginas de cada passeio con `TouristTrip` (propiedades como `itinerary`, `provider`, `touristType`). Ver `skills/seo/references/local-schema-types.md` para el patrón exacto — no se duplica aquí el JSON-LD completo según alcance de esta tarea.
- Propiedades recomendadas mínimas que el schema debería declarar cuando se implemente: `name`, `address` (PostalAddress estructurado, no string plano), `telephone`, `geo` (lat/long con 5 decimales — la dirección en Praia do Meio es geolocalizable con precisión razonable), `openingHoursSpecification` (coherente con los horarios ya visibles en `contato.html`: Lun-Sáb 08h-20h, Dom 09h-18h), `priceRange`, y `sameAs` apuntando a los perfiles reales de redes sociales **una vez que existan** (hoy son placeholders `#`, por lo que añadir `sameAs` con esos enlaces muertos sería peor que omitirlos).
- **Impacto local de la ausencia de schema:** sin `aggregateRating` estructurado tampoco puede aparecer rich snippet de estrellas en SERP aunque se consigan reseñas reales en el futuro — doble penalización (no aparece en Maps por falta de GBP, no aparece con estrellas en el orgánico por falta de schema).

---

## 7. Señales de GBP en la página (checklist detectado vs. faltante)

| Señal | Estado |
|---|---|
| Maps embed / iframe en el sitio | **Faltante** — explícitamente removido (`<!-- Map removed per user request -->` en contato.html) |
| Enlace "Cómo llegar" / Directions | **Faltante** — el ícono de dirección enlaza a `#` |
| Place ID / referencia a Google Place | **Faltante** |
| Botón / widget de reseñas de Google embebido | **Faltante** |
| Indicador de Google Posts o actividad reciente | **Faltante** (no aplica sin GBP) |
| Evidencia fotográfica propia reutilizable para GBP | **Presente** — abundante banco de imágenes propio por destino en `/img/` (pipa_1-5, maracajau_*, galinhos, gostoso_main, perobas, etc.) |
| Botón de WhatsApp / contacto directo | **Presente y bien implementado** — flotante en todas las páginas con mensaje prellenado contextual por passeio |
| Horario de atención visible | **Presente** — Lun-Sáb 08h-20h, Dom 09h-18h (contato.html) |
| Enlaces a redes sociales reales | **Faltante** — placeholders `#` en Instagram/Facebook/YouTube |

---

## 8. Salud de reseñas (Review Health Snapshot)

| Métrica | Valor detectado |
|---|---|
| Reseñas reales verificables en el sitio | 0 |
| Testimonios en texto plano sin verificación | 3 (Carolina Martins - São Paulo; Ricardo & Ana Ferreira - Lisboa; Família González - Buenos Aires) |
| Estrellas mostradas | ★★★★★ (5/5) fijo, hardcodeado en HTML, no dinámico |
| `aggregateRating` en schema | No existe (no hay schema) |
| Enlace a fuente original de cada testimonio (Google/TripAdvisor) | Ninguno |
| Foto/avatar de quien deja el testimonio | Ninguno |
| Fecha del testimonio | Ninguna |
| Reseñas en Google Business Profile | 0 (no existe el perfil) |
| Reseñas en TripAdvisor/Facebook | No verificables (no hay perfiles vinculados) |
| Velocidad de reseñas (regla de 18 días, Sterling Sky) | No aplica — sin perfil no hay reloj de velocidad corriendo |

**Diagnóstico:** los testimonios actuales son una **debilidad de confianza activa**, no solo una oportunidad perdida. Tres testimonios con 5 estrellas perfectas, sin fecha, sin enlace, sin foto y con nombres que no se pueden verificar leen — para un usuario escéptico y para sistemas anti-spam de Google/IA — como contenido potencialmente fabricado, incluso si en la realidad fueran genuinos. Esto es agravado por el hecho de que coexisten con: dominio sin DNS, redes sociales placeholder, y cero huella externa. El patrón conjunto es el que un evaluador de E-E-A-T (o un usuario desconfiado) interpretaría como señal de "sitio nuevo sin trazabilidad", lo cual puede ser literalmente cierto en este caso (negocio en fase de lanzamiento de su presencia digital) pero que el diseño actual no comunica con transparencia.

---

## 9. Estrategia de reviews recomendada

1. **Migrar el bloque de testimonios actual de "afirmación no verificable" a "prueba verificable" en tres fases:**
   - Fase 1 (inmediata, sin depender de GBP): añadir fecha a cada testimonio existente y, si los clientes dieron permiso, enlazar a la conversación de WhatsApp o a una captura de pantalla auténtica si fue dejado por redes sociales. Si no se puede verificar el origen de los 3 testimonios actuales, considerar seriamente retirarlos o etiquetarlos como "depoimentos enviados por e-mail" en vez de implicar que provienen de una plataforma de reseñas pública.
   - Fase 2 (tras crear GBP): sustituir progresivamente por un widget real de reseñas de Google (hay numerosos widgets embebibles gratuitos/freemium que tiran de la API de Google Places) o, como mínimo, un enlace directo "Vea todas nuestras reseñas en Google" con el conteo real.
   - Fase 3: una vez haya volumen en Google, añadir `aggregateRating` en el schema `TravelAgency`, alimentado por el mismo número real que se muestra en GBP (nunca un número distinto entre schema y perfil — sería una discrepancia grave detectable por Google).

2. **Plan de generación activa de reseñas (crítico dado el "18-day rule"):**
   - Automatizar el envío de un mensaje de WhatsApp post-tour (24-48h después de finalizado el passeio) con el enlace corto directo a "dejar reseña en Google" (`https://g.page/r/.../review` se genera automáticamente al verificar el GBP).
   - Priorizar pedir la reseña en el momento de mayor satisfacción (al final del tour, antes del transfer de regreso) en vez de solo por mensaje posterior — los operadores líderes del nicho (sección 4) acumulan volumen alto precisamente por pedir en el momento correcto, no solo por mensaje automatizado.
   - Establecer una meta mínima de cadencia: al menos 1 reseña nueva cada 2-3 semanas para no romper la "regla de los 18 días" de Sterling Sky en ningún momento del año, incluyendo temporada baja.
   - Capacitar al equipo (guías, "Junior" como fundador visible) para mencionar verbalmente la importancia de la reseña — en turismo receptivo la tasa de conversión de "pedido verbal en persona" supera ampliamente al pedido solo por email/WhatsApp frío.

3. **Responder al 100% de las reseñas, positivas y negativas, dentro de 48-72h** una vez existan — es una señal de gestión activa que tanto usuarios como el algoritmo de Maps ponderan, y es gratuita.

4. **Diversificar la plataforma de reseñas, no depender solo de Google:** dado que 3 de los top 5 factores de visibilidad en IA (AI visibility) son relacionados con citations, conseguir reseñas también en TripAdvisor (el más relevante para turismo internacional, con peso adicional porque los huéspedes extranjeros de las testimonios actuales — Portugal, Argentina — son exactamente el perfil de usuario que consulta TripAdvisor antes de reservar) multiplica la superficie de prueba social verificable.

---

## 10. Páginas de área de servicio / landing pages locales multi-destino

**Hallazgo positivo importante:** el sitio **ya tiene** una arquitectura de páginas por destino bien construida, lo cual es exactamente el patrón ganador identificado por Whitespark como **"dedicated service pages": factor #1 de ranking local orgánico y factor #2 de visibilidad en IA.** Páginas confirmadas:

- `/passeios/pipa.html`
- `/passeios/maracajau.html`, `/passeios/maracajau-buggy-mergulho.html`, `/passeios/maracajau-catamara.html`
- `/passeios/sao-miguel-do-gostoso.html`
- `/passeios/galinhos.html`
- `/passeios/perobas.html`
- `/passeios/por-do-sol-potengi.html`
- `/passeios/city-tour-buggy.html`
- `/passeios/litoral-sul-4x4.html`, `/litoral-sul-aguas.html`, `/litoral-sul-vip-4x4.html`, `/buggy-litoral-sul-pipa.html`
- `/passeios/buggy-litoral-norte.html`, `/buggy-litoral-intermedio.html`, `/buggy-litoral-alternativo.html`
- `/experiencias-exclusivas/` con variantes VIP de varios de los mismos destinos (vip-sao-miguel, mergulho-maracajau, veleiro-noronha, rota-norte-helicoptero, rota-natal-fortaleza)

Esto ya cubre los 3 destinos satélite mencionados en la tarea (Pipa, Maracajaú, São Miguel do Gostoso) más Galinhos y Perobas. **El trabajo pendiente no es crear estas páginas — ya existen — sino:**

1. **Añadir señales explícitamente locales/geográficas a cada página de destino** que hoy parecen centradas en la experiencia del passeio pero no necesariamente en SEO geográfico: verificar que cada una incluya (a confirmar con lectura completa por el agente de on-page, pero recomendado aquí por relevancia local):
   - Nombre del destino + "Natal RN" o "saindo de Natal" en H1/title/meta description de forma natural.
   - Distancia/tiempo de traslado desde Natal (ej. "Maracajaú está a 45 minutos ao norte de Natal") — contenido único que un competidor genérico no replica fácilmente y que responde directamente a intención de búsqueda local/logística.
   - Mención de que el punto de encuentro/salida es desde la sede en Praia do Meio, Natal — esto refuerza la asociación NAP↔servicio en cada página, no solo en el footer.

2. **Evitar el "doorway page" anti-pattern:** dado que existen variantes muy similares para el mismo destino (ej. `maracajau.html`, `maracajau-buggy-mergulho.html`, `maracajau-catamara.html`, `mergulho-maracajau.html` en experiencias-exclusivas, y `mergulho-natal.html` en blog) — esto es legítimo **solo si cada página representa una oferta de producto genuinamente distinta** (diferente vehículo/embarcación, diferente nivel de exclusividad/precio). Recomendación: auditar manualmente (fuera del alcance de schema/contenido puro) que el contenido de cada variante no sea un simple "swap" de 2-3 palabras sobre la misma plantilla — si lo es, Google las tratará como contenido duplicado/débil y diluirá autoridad entre ellas en vez de sumarla. Con la cantidad de variantes de Maracajaú detectadas (4 páginas), este es el clúster de mayor riesgo de canibalización interna del sitio.

3. **Interlinking entre páginas de destino y futura segmentación de GBP:** si el volumen de negocio lo justifica a futuro, evaluar si conviene un único GBP (recomendado para empezar, dado que es una sola ubicación física) en lugar de múltiples perfiles por destino — múltiples GBP para un solo negocio sin oficina física en cada destino violaría las guidelines de Google (un GBP por ubicación física real, no por landing page temática). **Las páginas de destino deben alimentar contenido al único GBP vía Posts y fotos, no convertirse en perfiles de GBP separados.**

4. **Considerar contenido "service area" explícito en una página agregadora** (ej. ampliar `experiencias.html` o crear una página tipo "Áreas que Atendemos") listando todos los destinos servidos con enlace a cada landing — refuerza tanto la experiencia de usuario como la señal de área de servicio ante Google, complementando (no sustituyendo) las páginas individuales ya existentes.

---

## 11. Estrategia de citations locales (Brasil / turismo) más allá de Google

Dado que 3 de los 5 principales factores de visibilidad en IA están relacionados con citations, y que NatalExperience Tours parte de cero en esta dimensión, se recomienda priorizar:

**Tier 1 — Generalistas (impacto amplio, base de confianza):**
- Google Business Profile (cubierto en sección 3 — máxima prioridad)
- Bing Places for Business (gratuito, subestimado, refuerza consistencia NAP en motor alternativo)
- Facebook Page con NAP completo (hoy es un placeholder `#` — crear cuanto antes ya que el footer ya promete su existencia)
- Instagram Business Profile con dirección y WhatsApp en bio (alto valor para turismo, donde la decisión de compra es muy visual)

**Tier 1 específico de turismo (alto valor para esta vertical, mayor prioridad que Yelp/BBB genéricos en este nicho):**
- **TripAdvisor** — listar como "Tour operator" en la categoría de Natal/RN, con NAP idéntico. Es la plataforma de mayor peso de decisión para el turista internacional, perfil que ya demuestran los testimonios actuales del sitio (Portugal, Argentina).
- **GetYourGuide** y **Civitatis** (en español, relevante dado el público hispanoamericano ya presente en testimonios) — funcionan como marketplace + citation + canal de reservas simultáneamente.
- **Booking.com Experiences / Viator (Tripadvisor company)** — mismo razonamiento.

**Directorios de turismo regional/institucional de RN (alta relevancia geográfica, baja competencia, fáciles de conseguir):**
- **Setur-RN** (Secretaria de Estado do Turismo do Rio Grande do Norte) — verificar registro/cadastro de prestadores de serviços turísticos; muchos estados exigen o al menos ofrecen un cadastro oficial (CADASTUR a nivel federal es el más importante — ver siguiente punto).
- **CADASTUR** (Ministério do Turismo, cadastro federal obligatorio para operadoras/agências de turismo en Brasil) — si NatalExperience Tours no está registrado aquí, es tanto un requisito regulatorio como una citation de altísima autoridad (.gov.br) que probablemente supere en peso de enlace a cualquier directorio comercial. **Verificar estado de este registro como prioridad — no es solo SEO, es cumplimiento legal del sector turístico brasileño.**
- **Natal.rn.gov.br / portal de turismo municipal de Natal** — directorios o secciones de "onde se hospedar/o que fazer" del propio municipio.
- **CCNRN / Câmara de Dirigentes Lojistas de Natal** u otras cámaras de comercio locales — citation de autoridad local genérica.
- **ABAV-RN** (Associação Brasileira de Agências de Viagens, sección RN) si aplica al perfil de la empresa.

**Directorios generalistas BR (volumen, fáciles, bajo esfuerzo):**
- Guia Mais, Apontador, Telelistas, Solutudo — directorios brasileños clásicos de NAP, baja autoridad individual pero suman consistencia agregada.

**Recomendación de secuencia:** GBP → CADASTUR (si no existe, es la más urgente por motivo regulatorio) → Facebook/Instagram reales → TripAdvisor → Setur-RN/directorios municipales → GetYourGuide/Civitatis → directorios genéricos BR. En cada paso, copiar el NAP canónico exacto documentado en la sección 5 — ninguna variación de formato.

---

## 12. Limitaciones de esta auditoría (disclaimer)

- **No se pudo verificar en vivo el Local Pack actual de Google** para "passeio de buggy Natal", "tours Natal RN" ni "mergulho Maracajaú" — Google bloqueó el fetch automatizado con pantalla de consentimiento de cookies. Las referencias competitivas de la sección 4 combinan un dato verificado en vivo (Maracajaú Diver) con patrones de mercado conocidos por conocimiento de dominio, explícitamente señalados como tales. **Se recomienda que un humano repita esta búsqueda en un navegador real, en Natal o con geolocalización/IP brasileña, para fijar benchmarks numéricos exactos de reseñas/posición antes de fijar KPIs.**
- **No se pudo confirmar si existe o no un Google Business Profile reclamado pero inactivo/sin optimizar** — solo se pudo confirmar ausencia de indexación pública bajo el nombre exacto vía Bing/DuckDuckGo. Si el negocio (o un tercero) ya creó un perfil sin vincularlo a nada, ese perfil podría existir sin aparecer en estas búsquedas. **Recomendación inmediata y gratuita: el propietario debe entrar a business.google.com con la cuenta de Gmail del negocio y verificar manualmente si ya hay un perfil pendiente de reclamar.**
- **No se evaluó el panorama de Local Pack para AI Overviews / respuestas de IA (Google AI Mode, ChatGPT, Perplexity)** de forma específica — el framework de 2026 indica que 3 de los 5 factores de visibilidad en IA son de citations, lo cual se cubrió a nivel de estrategia (sección 11), pero no se pudo testear consultas reales en estas superficies.
- **No se auditó CADASTUR ni Setur-RN de forma transaccional** (no se pudo confirmar si el negocio ya está o no registrado) — se señala como acción de verificación pendiente, no como hallazgo confirmado de ausencia.
- Proximidad geográfica representa el 55.2% de la varianza de ranking en Local Pack (estudio Search Atlas) — esto está fuera del control de cualquier estrategia de contenido o citations; se menciona aquí únicamente para contextualizar expectativas: ni el mejor GBP ni las mejores citations garantizan el primer puesto si un competidor está físicamente más cerca del usuario que busca.
- Este informe no sustituye una auditoría completa de NAP en citations ya existentes (no se pudo escanear todo el ecosistema de directorios brasileños por límites de la herramienta de búsqueda disponible) ni un análisis de backlinks/autoridad de dominio, que corresponde a otro agente del equipo de auditoría.

---

## 13. Checklist priorizada de acciones (Local SEO — operador de tours, mercado brasileño)

### Crítico

1. **Crear/reclamar el Google Business Profile** con categoría primaria "Tour operator", NAP canónico exacto (sección 5), y verificación de dirección física. Es el bloqueador de toda la dimensión GBP (25% del score) y del Local Pack.
2. **Verificar y, si falta, completar el registro CADASTUR** (Ministério do Turismo) — requisito regulatorio del sector y citation .gov.br de alta autoridad.
3. **Sustituir los enlaces placeholder `#` de Instagram/Facebook/YouTube por perfiles reales y activos**, con el mismo NAP. Mientras sean `#`, cualquier señal de "presencia social verificada" es cero, y el footer promete una presencia que no existe (riesgo de credibilidad ante usuarios).
4. **Resolver la inconsistencia "18 anos" (footer global) vs "30 anos" (quem-somos.html)** antes de declarar antigüedad en GBP/CADASTUR — una cifra contradictoria en el propio sitio debilita cualquier verificación de antigüedad de negocio.
5. **Reactivar el Maps embed en `contato.html`** (fue removido deliberadamente) y convertir el enlace de dirección del footer (`href="#"`) en un enlace real a Google Maps / Place ID.

### Alto

6. **Implementar schema `TravelAgency`/`LocalBusiness` con geo, NAP estructurado y `openingHoursSpecification`** coherente con los horarios ya visibles (Lun-Sáb 08h-20h, Dom 09h-18h) — coordinar con el agente de schema técnico para no duplicar esfuerzo.
7. **Sustituir o reforzar los 3 testimonios actuales** con fecha, fuente verificable y, en cuanto exista GBP, un widget real de reseñas de Google — los testimonios actuales (5 estrellas fijas, sin fecha, sin enlace) son una debilidad de confianza activa, no neutra.
8. **Lanzar perfil en TripAdvisor** y, si el presupuesto/operativa lo permite, en GetYourGuide/Civitatis — máxima relevancia para el perfil de turista internacional que el propio sitio ya demuestra captar (testimonios de Portugal y Argentina).
9. **Diseñar y automatizar el flujo de solicitud de reseñas post-tour** (WhatsApp 24-48h después + pedido verbal en el momento de mayor satisfacción) con cadencia mínima para no romper la regla de los 18 días de Sterling Sky.

### Medio

10. **Auditar el clúster de páginas de Maracajaú** (4 variantes: maracajau.html, maracajau-buggy-mergulho.html, maracajau-catamara.html, mergulho-maracajau.html) para confirmar que cada una representa una oferta de producto genuinamente distinta y no es un "doorway swap" de la misma plantilla — riesgo de canibalización interna.
11. **Añadir señales explícitas de distancia/tiempo desde Natal en cada página de destino** (Pipa, Maracajaú, Gostoso, Galinhos, Perobas) para reforzar intención de búsqueda local/logística y diferenciación de contenido único.
12. **Registrar el negocio en Setur-RN y directorios municipales de turismo de Natal**, y en directorios genéricos BR (Guia Mais, Apontador) para construir volumen de citations consistentes.

### Bajo

13. **Migrar el email de contacto de Gmail genérico a un dominio corporativo propio** una vez `natalexperience.com.br` resuelva en DNS — mejora percepción de legitimidad en formularios de citations B2B (GetYourGuide, Civitatis, cámaras de comercio).
14. **Crear una página agregadora "Áreas que Atendemos"** que liste todos los destinos servidos con enlace a cada landing existente, complementando (no sustituyendo) las páginas individuales ya construidas.
15. **Considerar exponer un teléfono fijo adicional con DDD 84** (si la operativa del negocio lo permite) junto al móvil/WhatsApp actual, replicando la señal de "negocio establecido con oficina física" observada en el competidor verificado (Maracajaú Diver).

---

*Informe generado como parte de la auditoría SEO integral de NatalExperience Tours. Esta sección cubre exclusivamente Local SEO; ver informes complementarios del equipo de auditoría para hallazgos técnicos (DNS, Core Web Vitals), schema markup completo, y on-page/contenido general.*
