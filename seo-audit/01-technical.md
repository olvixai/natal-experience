# Auditoría SEO Técnica — NatalExperience Tours
**Fecha de auditoría:** 2026-06-26
**Método:** Lectura directa de archivos fuente en `E:\ANTIGRAVITY\NATALEXPERIENCE` (el dominio de producción no resuelve en DNS; ver Hallazgo Crítico #1). Despliegue accesible actualmente: `https://natal-experience.vercel.app/`.
**Alcance:** 42 páginas HTML (8 raíz + 16 `/passeios/` + 10 `/experiencias-exclusivas/` + 8 `/blog/`), `robots.txt`, `sitemap.xml`, `vercel.json`, scripts de generación (`.py`), `apps-script/Code.gs`.

---

## Resumen de Score Técnico

| Categoría | Estado | Score (0-100) |
|---|---|---|
| 1. Crawlability (robots.txt, sitemap, noindex) | ⚠️ Parcial | 55 |
| 2. Indexabilidad (canonicals, duplicados, dominio) | ❌ Bloqueado | 20 |
| 3. Seguridad (HTTPS, headers) | ❌ Fail | 25 |
| 4. Estructura de URLs | ✅ Aceptable | 75 |
| 5. Mobile (viewport, touch targets) | ✅ Pass | 80 |
| 6. Core Web Vitals (riesgos desde código fuente) | ❌ Fail | 30 |
| 7. Structured Data (detección superficial) | ⚠️ Parcial | 40 |
| 8. JavaScript Rendering (CSR vs SSR) | ✅ Pass (HTML estático) | 95 |
| 9. IndexNow Protocol | ❌ No implementado | 0 |
| **TOTAL PONDERADO** | | **~46/100** |

El score está dominado por el Hallazgo Crítico #1 (dominio no resuelve), que por sí solo invalida toda la indexabilidad del sitio independientemente de la calidad on-page, que en general es buena.

---

## CRITICAL

### C1. El dominio de producción `natalexperience.com` no resuelve en DNS
**Evidencia:** `nslookup natalexperience.com` → `Non-existent domain`. Todos los `canonical`, `og:url` y `sitemap.xml` referencian este dominio. El despliegue real y accesible está en `https://natal-experience.vercel.app/`.

**Impacto:** Google no puede rastrear ni indexar absolutamente nada. Aunque el sitio se indexara accidentalmente vía el subdominio `.vercel.app`, todas las señales de canonicalización apuntan a un dominio que no existe — lo que generará errores "No se encontró la página" o "URL canónica no válida" en Search Console en cuanto Google intente verificarlo. Cualquier esfuerzo de contenido/schema/keywords hecho hasta que esto se resuelva tiene ROI de indexación = 0.

**Recomendación — pasos exactos:**
1. **En el registrador del dominio** (donde se compró `natalexperience.com`, ej. registro.br): localizar la gestión de DNS del dominio.
2. **En Vercel:** ir al proyecto `natal-experience` → Settings → Domains → Add Domain → introducir `natalexperience.com` y `natalexperience.com`. Vercel mostrará los registros DNS exactos a crear (normalmente un registro `A` apuntando a `76.76.21.21` para el dominio raíz, y un `CNAME` apuntando a `cname.vercel-dns.com` para el subdominio `www`).
3. **En el panel DNS del registrador:** crear esos registros exactamente como los indica Vercel.
4. Esperar propagación DNS (puede tardar de minutos a 48h; dominios `.com.br` vía registro.br suelen propagar en 1-6h).
5. Verificar con `nslookup natalexperience.com` y confirmar que Vercel marque el dominio como "Valid Configuration" (candado verde) en el dashboard.
6. Una vez resuelto, forzar verificación de propiedad en Google Search Console (dominio y prefijo `https://www.`) y enviar el sitemap.
7. Decidir el dominio canónico real: si se usará `www` (como ya están configurados todos los `canonical`/`og:url`), configurar en Vercel el redirect 301 de `natalexperience.com` (sin www) → `https://www.natalexperience.com` para evitar contenido duplicado entre apex y subdominio.

---

### C2. `apps-script/Code.gs` expone un Google Sheet ID en texto plano y está trackeado en git/producción
**Evidencia:** `E:\ANTIGRAVITY\NATALEXPERIENCE\apps-script\Code.gs` línea 1: `const SHEET_ID = '1K-sHm6QKT78yoUoH-f40df5lb5FS8jJjyOM-HWdy9Vo';` — confirmado vía `git ls-files` que el archivo está trackeado (no ignorado), y `.gitignore` solo excluye `.vercel`. Al ser un sitio estático servido íntegro desde la raíz del repo, Vercel serviría este archivo como un recurso estático público accesible en `https://www.natalexperience.com/apps-script/Code.gs` salvo que se excluya explícitamente.

**Impacto:** No es una API key explotable por sí sola, pero expone el identificador del Google Sheet donde se almacenan los leads (nombre, email, teléfono, mensaje de clientes) — facilita reconocimiento/targeting si el Sheet no tiene permisos estrictos. Es una mala práctica de higiene de repositorio independientemente del riesgo real.

**Recomendación:**
- Añadir `apps-script/` y todos los `*.py` al `.gitignore` (ver hallazgo H7) y a un `.vercelignore` para que no se desplieguen como archivos públicos.
- Si el archivo ya fue público alguna vez (verificar historial de despliegues de Vercel), rotar el `SHEET_ID` (mover a una nueva hoja) y revisar permisos de acceso del Sheet.
- Mover `SHEET_ID` a un Script Property de Apps Script en lugar de hardcodearlo, como buena práctica adicional.

---

## HIGH

### H1. `vercel.json` carece de headers de seguridad y de cache-control
**Evidencia:** `E:\ANTIGRAVITY\NATALEXPERIENCE\vercel.json` contiene únicamente `{"name": "natal-experience"}`. No hay configuración de `headers`, `redirects`, ni `cleanUrls`.

**Impacto:** Sin headers de seguridad, el sitio es más vulnerable a clickjacking, MIME-sniffing y ataques XSS reflejados; Lighthouse/PageSpeed penalizará "Best Practices" por la ausencia de CSP/HSTS. Sin `Cache-Control` explícito en assets estáticos (imágenes, CSS, JS), Vercel aplica su default (generalmente aceptable para HTML pero subóptimo para assets versionados), perdiendo oportunidad de cache agresivo que ayuda a CWV en visitas repetidas.

**Recomendación — `vercel.json` sugerido:**
```json
{
  "name": "natal-experience",
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "Permissions-Policy", "value": "geolocation=(), camera=(), microphone=()" }
      ]
    },
    {
      "source": "/(css|js|img)/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/(.*).html",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/index.html",
      "destination": "/",
      "permanent": true
    }
  ]
}
```
Notas:
- CSP completa no se incluye en el ejemplo por riesgo de romper inline `style="..."` (usado extensivamente en el sitio, ver H6) y `<script>` inline en `blog/guia-natal.html`; si se añade CSP, debe incluir `'unsafe-inline'` para `style-src`/`script-src` hasta que se eliminen los estilos/scripts inline, o usar nonces.
- El redirect de `/index.html` → `/` evita contenido duplicado entre `https://dominio/` y `https://dominio/index.html` (ver H3).
- Considerar añadir aquí también el redirect 301 de apex→www (o viceversa) mencionado en C1 si Vercel no lo gestiona ya vía el panel de dominios.

---

### H2. Imágenes sin optimizar: riesgo severo de LCP
**Evidencia:** `img/` pesa **69 MB** en total. Ejemplos concretos:
- `img/parachos.png` — 7.05 MB
- `img/f1.jpg` — 5.77 MB
- `img/f2.jpg` — 4.20 MB
- `img/f4.jpg` — 3.16 MB
- `img/maracajau-snorkeling.png` — 2.11 MB

Ninguna etiqueta `<img>` revisada (0 de 29 muestreadas en `index.html`/`passeios/pipa.html`) tiene atributos `width`/`height` ni `loading="lazy"`. Todas las imágenes son `.jpg`/`.png` (63 + 52 archivos), ninguna en formato moderno WebP/AVIF.

**Impacto:** Cualquier imagen hero/above-the-fold de varios MB en PNG/JPG sin compresión moderna es la causa #1 de LCP >4s (rango "Poor") en sitios estáticos de turismo con fotografía pesada. La ausencia de `width`/`height` (o `aspect-ratio` en CSS) también contribuye directamente a CLS al no reservar espacio antes de que la imagen cargue.

**Recomendación:**
1. Convertir todas las imágenes a WebP (calidad 75-82) o AVIF, con fallback `<picture>` si se requiere compatibilidad amplia.
2. Redimensionar todo a un máximo realista de visualización (hero ~1920px ancho, cards ~600-800px) — ya existe `optimize_images.py` en el repo que hace resize a 1200px máx, pero solo se ejecuta manualmente sobre 3 archivos sueltos de `Downloads`; no es un pipeline aplicado a todo `img/`.
3. Añadir `width` y `height` explícitos (o `aspect-ratio` vía CSS) a cada `<img>`.
4. Añadir `loading="lazy"` a todas las imágenes excepto la hero/LCP de cada página (que debe cargar eager y, si es posible, con `fetchpriority="high"`).
5. Servir imágenes desde Vercel con el header de cache agresivo indicado en H1.
6. Tras la conversión, `f1.jpg` (5.77MB) y `parachos.png` (7MB) deberían poder bajar de 200-400KB sin pérdida visual perceptible.

---

### H3. Contenido duplicado potencial: `/` vs `/index.html`
**Evidencia:** `sitemap.xml` lista `https://www.natalexperience.com/` (sin `index.html`), y el `canonical` de `index.html` apunta correctamente a `/`. Sin embargo, no existe ningún redirect que fuerce `/index.html` → `/`, y el archivo es servible bajo ambas rutas en cualquier hosting estático (incluido Vercel por defecto).

**Impacto:** Riesgo bajo-medio de contenido duplicado si algún enlace externo o interno antiguo apunta a `/index.html` explícitamente; Google normalmente resuelve esto vía canonical, pero es una corrección trivial de eliminar por completo el riesgo.

**Recomendación:** Implementar el redirect 301 incluido en el bloque `vercel.json` de H1.

---

### H4. Enlazado interno: el blog nunca enlaza hacia las páginas de conversión (passeios / experiencias-exclusivas)
**Evidencia:** Verificado sistemáticamente en los 8 artículos de `/blog/` (`buggy-vale-a-pena.html`, `guia-natal.html`, `melhores-lagoas-natal.html`, `melhores-passeios.html`, `mergulho-natal.html`, `norte-ou-sul.html`, `pipa-bate-e-volta.html`, `roteiro-5-dias-natal.html`): **ninguno contiene un solo `href` hacia `/passeios/*` o `/experiencias-exclusivas/*`**. El único enlace "propio" de cada artículo es su `og:url` (no es un link de navegación real). Tampoco hay enlaces entre artículos del blog entre sí (cada uno es una isla).

**Impacto:** Esto es una pérdida significativa de:
- **Link equity interno**: las páginas de blog (que son las más aptas para rankear por keywords informacionales de cola larga, ej. "Maracajaú ou Perobas") no transfieren autoridad a las páginas de producto/conversión, que son las que generan reservas.
- **Conversión**: un usuario que aterriza en `blog/mergulho-natal.html` (que compara Maracajaú vs Perobas) no tiene ningún CTA contextual hacia `passeios/maracajau.html` o `passeios/perobas.html` — debe volver manualmente al menú y buscar.
- **Topical authority / SEO semántico**: motores de búsqueda (y LLMs en respuestas IA) interpretan mejor la relación entre contenido informacional y transaccional cuando existe enlazado explícito.

**Recomendación:** Añadir 2-4 enlaces contextuales por artículo de blog hacia las páginas de tour relevantes. Mapeo sugerido inmediato:
| Artículo blog | Debería enlazar a |
|---|---|
| `blog/buggy-vale-a-pena.html` | `passeios/buggy-litoral-norte.html`, `passeios/buggy-litoral-alternativo.html` |
| `blog/guia-natal.html` | `experiencias.html`, varios passeios mencionados |
| `blog/melhores-lagoas-natal.html` | `passeios/litoral-sul-aguas.html` |
| `blog/melhores-passeios.html` | múltiples `/passeios/*` (es un listicle, debería ser el artículo con más enlaces salientes) |
| `blog/mergulho-natal.html` | `passeios/maracajau.html`, `passeios/perobas.html`, `passeios/maracajau-catamara.html` |
| `blog/norte-ou-sul.html` | `passeios/buggy-litoral-norte.html`, `passeios/litoral-sul-4x4.html` |
| `blog/pipa-bate-e-volta.html` | `passeios/pipa.html`, `passeios/buggy-litoral-sul-pipa.html` |
| `blog/roteiro-5-dias-natal.html` | el mayor número posible (es contenido "hub") |

Adicionalmente, añadir una sección "Artigos relacionados" al final de cada post de blog enlazando 2-3 artículos más del mismo blog.

---

### H5. Página huérfana de navegación: `passeios/litoral-sul-4x4.html`
**Evidencia:** Esta página **no aparece enlazada en `experiencias.html`** (el hub que lista las 26 páginas de tours) ni en ninguna navbar/footer. Solo tiene 2 enlaces entrantes, ambos desde botones secundarios "Ver detalhes" en `experiencias-exclusivas/passeio-aviao.html` y `experiencias-exclusivas/voo-helicoptero.html` — páginas de temática no relacionada (vuelos), lo cual sugiere que el enlace es un remanente de generación automatizada y no un enlace editorial intencional.

**Impacto:** La página recibe casi cero link equity interno relevante, y un usuario navegando normalmente por `experiencias.html` → "Passeios Clássicos" nunca la encontrará. Es indexable y está en el sitemap, pero la falta de descubribilidad interna reduce su probabilidad de rastreo frecuente y de ranking.

**Recomendación:** Añadir `passeios/litoral-sul-4x4.html` a la grilla de tours clásicos en `experiencias.html` (sección Litoral Sul), junto a `litoral-sul-aguas.html` y `litoral-sul-vip-4x4.html`.

---

### H6. Uso extensivo de `style="..."` inline en lugar de clases CSS
**Evidencia:** Ejemplo en `passeios/buggy-litoral-norte.html`: `<h1 style="font-size: clamp(1.8rem, 4vw, 2.8rem); margin-bottom: var(--space-sm);">`. Este patrón se repite en las páginas de `/passeios/` y `/experiencias-exclusivas/` generadas por `gen_pages.py`.

**Impacto:** No es un bloqueador de indexación, pero (a) infla el HTML transferido en cada página (peor TTFB relativo / parsing), (b) impide aplicar una Content-Security-Policy estricta sin `'unsafe-inline'` en `style-src` (ver H1), y (c) dificulta el mantenimiento de diseño consistente entre las 42 páginas.

**Recomendación:** Migrar estos estilos inline a clases utilitarias en `css/style.css` (ej. `.h1--tour-title`). No es urgente para SEO directo, pero facilita adoptar CSP en el futuro.

---

## MEDIUM

### M1. `robots.txt` no declara explícitamente los crawlers de IA/LLM
**Evidencia:** `E:\ANTIGRAVITY\NATALEXPERIENCE\robots.txt` actual:
```
User-agent: *
Allow: /
Sitemap: https://www.natalexperience.com/sitemap.xml
```
El wildcard `User-agent: *` con `Allow: /` técnicamente ya permite a todos los bots (incluidos GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, etc.) rastrear el sitio, así que **no hay bloqueo activo**. Sin embargo, no hay declaración explícita por bot, lo cual es la práctica recomendada en 2026 para sitios que buscan visibilidad en respuestas de IA generativa (AI Overviews, ChatGPT browsing, Perplexity, Claude).

**Recomendación — `robots.txt` sugerido:**
```
User-agent: *
Allow: /

# AI / LLM crawlers — explícitamente permitidos (visibilidad en respuestas de IA)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

Sitemap: https://www.natalexperience.com/sitemap.xml
```
Nota: dado que el objetivo del sitio es maximizar reservas turísticas, permitir explícitamente estos bots favorece que la marca aparezca citada en respuestas de ChatGPT/Perplexity/Gemini/Claude cuando un usuario pregunte "mejores passeios em Natal" — esto es deseable para este caso de negocio. Si en el futuro se quisiera restringir el entrenamiento de modelos sin restringir la búsqueda conversacional, se puede bloquear específicamente `GPTBot`/`CCBot` (entrenamiento) mientras se permite `OAI-SearchBot`/`ChatGPT-User` (búsqueda en tiempo real), pero no se recomienda para este negocio.

### M2. `robots.txt` no bloquea rutas/archivos que no deberían ser rastreables
**Evidencia:** El proyecto contiene en su raíz: `apply_seo.py`, `correct_phone_9.py`, `final_fix.py`, `fix_corruption.py`, `gen_pages.py`, `optimize_images.py`, `safe_fix.py`, y el directorio `apps-script/`. Ninguno de estos está bloqueado en `robots.txt`, y al ser un despliegue estático sin `.vercelignore`/exclusiones, son potencialmente servibles como archivos públicos en producción.

**Recomendación:** Añadir al `robots.txt`:
```
Disallow: /apps-script/
Disallow: /*.py$
```
Esto es complementario (no sustituto) de la solución real, que es **no desplegar estos archivos en absoluto** (ver C2 y H7) — `robots.txt` solo es una directiva de cortesía para bots que la respetan, no un control de acceso real.

### M3. `sitemap.xml`: `lastmod` idéntico en las 42 URLs (artefacto del script generador, no refleja actualización real)
**Evidencia:** Las 42 entradas tienen `<lastmod>2026-06-14</lastmod>` sin excepción. Confirmado en `gen_pages.py` y `apply_seo.py`: ambos scripts regeneran `sitemap.xml` completo en cada ejecución usando `datetime.now().strftime("%Y-%m-%d")` como `lastmod` para **todas** las URLs, independientemente de si esa página específica cambió.

**Impacto:** Google usa `lastmod` como señal (débil pero real) de frescura para priorizar rastreo. Un `lastmod` idéntico en todas las páginas es un patrón reconocible que Google tiende a ignorar/descontar como señal poco fiable, reduciendo su utilidad para priorización de crawl budget.

**Recomendación:** Modificar `gen_pages.py`/`apply_seo.py` para que `lastmod` se derive del timestamp real de última modificación del archivo (`os.path.getmtime(filepath)`) en lugar de `datetime.now()` global. Alternativamente, mantener un registro manual de fecha de última edición de contenido por página.

### M4. `sitemap.xml`: prioridades y changefreq genéricos sin diferenciación real
**Evidencia:** Solo 3 valores de prioridad en todo el sitemap: `0.9` (passeios + exclusivas), `0.8` (páginas raíz), `0.7` (blog). Todos con `changefreq=weekly`. La home (`/`) comparte la misma prioridad (0.8) que `politica-cookies.html` y `politica-privacidade.html`, lo cual subestima la home y sobrestima páginas legales de bajo valor SEO.

**Recomendación:**
- Home (`/`): `priority=1.0`.
- Páginas legales (`politica-cookies.html`, `politica-privacidade.html`): `priority=0.3`, `changefreq=yearly` (raramente cambian).
- `experiencias.html`, `blog.html`, `contato.html`, `faq.html`: `priority=0.8` está bien.
- Tours y exclusivas: `priority=0.9` está bien, pero `changefreq` debería ser `monthly` salvo que realmente se actualicen precios/disponibilidad semanalmente.
- Nota: `priority` y `changefreq` son señales que Google **ignora explícitamente** desde hace años (lo confirma su propia documentación), así que esta corrección es de bajo impacto real en rastreo — se incluye aquí por completitud y porque no cuesta nada corregirlo, pero no debe priorizarse sobre hallazgos Critical/High.

### M5. Ausencia de Open Graph completo (`og:title`, `og:description`, `og:type`) en 41 de 42 páginas
**Evidencia:** Solo `index.html` tiene `og:title`, `og:description` y `og:type`. Las 41 páginas restantes tienen únicamente `og:url` y `og:image` (heredados del script `apply_seo.py`, que solo inyecta esos dos tags), pero carecen de `og:title`/`og:description` propios.

**Impacto:** Cuando estas páginas se comparten en WhatsApp (canal de conversión principal de este negocio, visible en los CTAs "Reserve pelo WhatsApp!"), Facebook o Instagram, las plataformas caerán de vuelta al `<title>`/meta description genéricos del HTML o, en el peor caso, mostrarán una vista previa pobre sin descripción. Esto es particularmente relevante porque el modelo de negocio depende fuertemente de compartir enlaces de tours específicos por WhatsApp.

**Recomendación:** Extender `apply_seo.py` para inyectar también `og:title` (puede reusar el `<title>` sin el sufijo "| NatalExperience Tours") y `og:description` (puede reusar el `meta description`) y `og:type=website` en todas las páginas, no solo en `index.html`. También añadir Twitter Card básico (`twitter:card=summary_large_image`, `twitter:title`, `twitter:description`) ya que actualmente **0 de 42 páginas** tienen estas etiquetas.

### M6. Posible keyword cannibalization en el clúster "Litoral Norte / Buggy"
**Evidencia:** Tres páginas con propósito y keywords muy solapados:
- `passeios/buggy-litoral-norte.html` → H1 "Litoral Norte Completo", desc "Passeio de buggy pelo litoral norte... A partir de R$ 780"
- `passeios/buggy-litoral-intermedio.html` → H1 "Litoral Norte Especial", desc "...3 horas... A partir de R$ 500"
- `passeios/buggy-litoral-alternativo.html` → H1 "Litoral Norte Alternativo", desc "...2 horas... A partir de R$ 400"

Las tres compiten por la misma intención de búsqueda raíz ("passeio de buggy litoral norte Natal", "passeio buggy Genipabu") diferenciándose solo por duración/precio, no por keyword distinta.

**Impacto:** Riesgo medio de que Google no sepa cuál de las tres priorizar para queries genéricas como "passeio de buggy em Natal" o "buggy litoral norte preço", diluyendo la señal de relevancia entre las tres en lugar de consolidarla en una. También existe un cuarto título potencialmente solapado: `passeios/maracajau-buggy-mergulho.html` ("Litoral Norte (Maracajaú de Buggy)").

**Recomendación:**
- Diferenciar más agresivamente los `<title>`/H1/contenido por **duración y nivel de servicio** explícitos en la keyword principal, no solo en el nombre comercial: ej. "Passeio de Buggy Litoral Norte 2h (Dunas de Genipabu) | Natal Experience" vs "...Dia Completo (8h)...".
- Considerar consolidar contenido informacional común (historia de Genipabu, qué llevar, seguridad) en una única sub-sección o en `blog/buggy-vale-a-pena.html`, enlazando desde ahí a las 3 variantes de duración mediante una tabla comparativa — esto también resuelve parcialmente H4.
- Asegurar que el internal linking entre estas 3 páginas (actualmente: `pipa.html` enlaza a `buggy-litoral-norte.html`, pero no he confirmado enlace cruzado entre las 3 variantes entre sí) las posicione claramente como "variantes de un mismo producto" vía breadcrumbs o un selector de duración, en lugar de competir como artículos independientes.

### M7. JavaScript: `main.js` sin `defer`/`async`, ubicado antes del cierre de `</body>` pero sin atributo de carga
**Evidencia:** `<script src="js/main.js"></script>` (línea 535 de `index.html`, y equivalente en el resto de páginas) — está al final del documento, lo cual ya mitiga buena parte del render-blocking, pero no usa `defer`, y `blog/guia-natal.html` además tiene un `<script>` inline adicional cuyo contenido no fue auditado en profundidad (puede ser tracking o interactividad menor).

**Impacto:** Bajo, dado que el script ya está al final del `<body>`. Pero añadir `defer` es trivial y mejora ligeramente el tiempo hasta interactividad (relevante para INP).

**Recomendación:** Cambiar a `<script src="js/main.js" defer></script>` de forma consistente en las 42 páginas (vía el mismo script de generación).

---

## LOW

### L1. Scripts `.py` de mantenimiento y `apps-script/` versionados sin excluir de git/despliegue
**Evidencia:** `.gitignore` (`E:\ANTIGRAVITY\NATALEXPERIENCE\.gitignore`) contiene únicamente la línea `.vercel`. Confirmado vía `git ls-files` que **todos** los siguientes están trackeados: `apply_seo.py`, `correct_phone_9.py`, `final_fix.py`, `fix_corruption.py`, `gen_pages.py`, `optimize_images.py`, `safe_fix.py`, `apps-script/Code.gs`. Son scripts de generación/mantenimiento de contenido (confirmado por lectura de `gen_pages.py` y `apply_seo.py`: generan HTML de tours desde plantillas y regeneran `sitemap.xml`/`robots.txt`), no afectan el contenido público per se, pero no tienen ninguna razón para ser servidos como parte del sitio en producción.

**Recomendación:**
- Añadir a `.gitignore` (o, preferiblemente, mantenerlos en git para versionado del workflow, pero excluirlos del **despliegue**):
  ```
  # .vercelignore (nuevo archivo)
  *.py
  apps-script/
  __pycache__/
  ```
- Si se prefiere no versionarlos en absoluto en este repo (ej. si contienen rutas locales como `C:\Users\hecgo\Downloads` — confirmado en `optimize_images.py` línea 4), moverlos a un repositorio/carpeta de tooling separada fuera del directorio servido por Vercel.
- En cualquier caso, un `.vercelignore` es la corrección mínima necesaria para evitar que terminen accesibles públicamente en `https://www.natalexperience.com/gen_pages.py`, etc.

### L2. Falta de `hreflang`
**Evidencia:** 0 de 42 páginas tienen `hreflang`. El sitio es monolingüe (`pt-BR` declarado consistentemente en `<html lang="pt-BR">` en las 4 muestras verificadas).

**Análisis:** No es un error — `hreflang` solo es necesario cuando existen versiones del mismo contenido en distintos idiomas/regiones. Dado que NatalExperience Tours es un negocio que probablemente también recibe turistas internacionales (Argentina, Europa) buscando en inglés/español, **se recomienda evaluar a futuro** una versión en inglés y/o español de al menos las páginas de mayor conversión (`experiencias.html`, tours top), momento en el cual sí se requerirá implementar `hreflang` correctamente. Para validación detallada de hreflang cuando llegue ese momento, usar el sub-skill `seo-hreflang`. Por ahora, **no se marca como issue** — es una oportunidad de expansión, no un defecto del estado actual monolingüe.

### L3. `<title>` y meta description: 3 páginas exceden longitud recomendada
**Evidencia (medido con conteo exacto de caracteres):**

| Página | Title (60 máx) | Description (160 máx) |
|---|---|---|
| `blog/melhores-lagoas-natal.html` | **75 car.** (excede) | 163 (excede levemente) |
| `experiencias-exclusivas/rota-norte-helicoptero.html` | 45 | **226 car.** (excede) |
| `experiencias-exclusivas/transfer-vip.html` | 36 | **216 car.** (excede) |
| `experiencias-exclusivas/rota-natal-fortaleza.html` | 51 | **214 car.** (excede) |
| `experiencias-exclusivas/buggy-vip.html` | 48 | **216 car.** (excede) |
| `passeios/litoral-sul-4x4.html` | 43 | **212 car.** (excede) |
| `experiencias-exclusivas/veleiro-noronha.html` | 55 | **204 car.** (excede) |
| `passeios/perobas.html` | 58 | **212 car.** (excede) |
| `experiencias-exclusivas/mergulho-maracajau.html` | 53 | **207 car.** (excede) |
| `experiencias-exclusivas/passeio-aviao.html` | 61 (límite) | **202 car.** (excede) |
| `passeios/galinhos.html` | 44 | **198 car.** (excede) |
| `experiencias-exclusivas/rota-secreta-praias.html` | 56 | **200 car.** (excede) |
| `experiencias-exclusivas/vip-sao-miguel.html` | 58 | **198 car.** (excede) |
| `passeios/por-do-sol-potengi.html` | 45 | **200 car.** (excede) |
| `passeios/litoral-sul-4x4.html` | — | 212 |
| `passeios/sao-miguel-do-gostoso.html` | 45 | **186 car.** (excede) |
| `experiencias-exclusivas/voo-helicoptero.html` | 53 | 179 (excede levemente) |
| `passeios/litoral-sul-vip-4x4.html` | 65 (excede) | 186 (excede) |
| `index.html` | 67 (excede) | 179 (excede levemente) |

**Patrón identificado:** Todas las páginas de `/experiencias-exclusivas/` (10 de 10) exceden los 160 caracteres de meta description, generalmente entre 179-226 caracteres — Google truncará la vista previa en SERP con "...", cortando la llamada a la acción "Reserve pelo WhatsApp!" que casi todas incluyen al final (es decir, la parte truncada es precisamente el CTA, lo cual reduce su efectividad en el snippet de búsqueda).

**Recomendación:** Recortar todas las meta descriptions de `/experiencias-exclusivas/` a 150-155 caracteres, moviendo el CTA "Reserve pelo WhatsApp!" antes del límite o eliminándolo de la description (no es indispensable ahí, Google ya muestra el dominio/marca). Acortar `index.html` title de 67 a ≤60 caracteres y `blog/melhores-lagoas-natal.html` de 75 a ≤60.

**Nota positiva:** No se encontraron títulos duplicados, descriptions duplicadas, títulos ausentes ni descriptions ausentes en ninguna de las 42 páginas — la cobertura básica de title/description es completa y única en el 100% del sitio.

### L4. Ausencia de `meta name="robots"` explícito (no es un defecto, pero falta granularidad)
**Evidencia:** 0 de 42 páginas tienen `<meta name="robots">`. Por defecto esto equivale a `index, follow`, que es el comportamiento deseado para las 42 páginas actuales — no hay error aquí.

**Recomendación (preventiva):** Si en el futuro se añaden páginas de utilidad (páginas de agradecimiento post-formulario, páginas de error custom, landing pages de campañas pagas duplicadas), añadir explícitamente `<meta name="robots" content="noindex, follow">` en esas páginas específicas para evitar indexación accidental de contenido transaccional/duplicado.

### L5. No hay implementación del protocolo IndexNow (Bing, Yandex, Naver)
**Evidencia:** No se encontró ningún script, endpoint o referencia a IndexNow en el proyecto.

**Impacto:** Bajo para el mercado brasileño (donde Google domina ampliamente la cuota de búsqueda), pero IndexNow es gratuito y de implementación trivial, y notifica instantáneamente a Bing/Yandex cuando se publica o actualiza una página, sin esperar al siguiente rastreo.

**Recomendación:** Una vez resuelto el dominio (C1), implementar un ping simple a `https://api.indexnow.org/indexnow?url={URL}&key={API_KEY}` cada vez que se publique o actualice una página, generando una API key gratuita en https://www.bing.com/indexnow. Dado que el sitio es estático y se genera vía scripts Python, esto se puede automatizar fácilmente añadiendo una llamada HTTP al final de `apply_seo.py` que recorra el `sitemap.xml` recién generado.

---

## Hallazgos positivos (no requieren acción)

- Estructura de URLs limpia y semántica: rutas en minúsculas, separadas por guiones, sin parámetros de query, organizadas lógicamente por categoría (`/passeios/`, `/experiencias-exclusivas/`, `/blog/`). No hay URLs con mayúsculas mixtas, espacios codificados, ni IDs numéricos opacos.
- 100% de las páginas usan HTTPS en todos los enlaces internos verificados (ningún `href="http://"` encontrado).
- `<html lang="pt-BR">` y `<meta charset="UTF-8">` presentes y consistentes en todas las muestras verificadas.
- `viewport` meta tag correcto (`width=device-width, initial-scale=1.0`) presente en las 42 páginas — base sólida de mobile-friendliness.
- Sitio 100% HTML estático sin dependencia de renderizado JS (CSR) — no hay riesgo de problemas de indexación por contenido inyectado vía JavaScript; Googlebot puede leer el contenido completo en el HTML crudo. `main.js` es solo interactividad complementaria.
- `experiencias.html` enlaza correctamente a 25 de las 26 páginas de tours (única excepción: `litoral-sul-4x4.html`, ver H5), demostrando una arquitectura de hub intencional y mayormente bien ejecutada.
- Sin títulos ni meta descriptions duplicadas o ausentes en ninguna de las 42 páginas.
- JSON-LD (`FAQPage`) presente en `faq.html` — implementación detectada y bien formada en una revisión superficial (la validación profunda de schema corresponde a otro informe en paralelo).
