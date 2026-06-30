# Auditoría SEO + GEO (AI Search) Completa — NatalExperience Tours
**Fecha:** 2026-06-26
**Sitio:** Agencia de tours/passeios en Natal, RN, Brasil — 42 páginas HTML estáticas
**Código fuente:** `E:\ANTIGRAVITY\NATALEXPERIENCE`
**Deploy accesible verificado:** https://natal-experience.vercel.app/
**Dominio canónico declarado (NO accesible):** https://www.natalexperience.com/

Este documento es el resumen ejecutivo. El detalle completo de cada área está en:
- [`01-technical.md`](01-technical.md) — SEO técnico (robots, sitemap, canonical, seguridad, CWV)
- [`02-content.md`](02-content.md) — Calidad de contenido y E-E-A-T
- [`03-schema.md`](03-schema.md) — Datos estructurados (JSON-LD listos para copiar/pegar)
- [`04-keywords-clusters.md`](04-keywords-clusters.md) — Keywords, cannibalización y arquitectura de clusters
- [`05-geo-ai-readiness.md`](05-geo-ai-readiness.md) — Preparación para LLMs (robots.txt IA, llms.txt, citabilidad)
- [`06-local-seo.md`](06-local-seo.md) — SEO local (GBP, NAP, reviews, competencia)

---

## Score SEO Health (0-100)

| Categoría | Peso | Score actual | Nota |
|---|---|---|---|
| Technical SEO | 22% | 46 | Dominado por el bloqueador de dominio (ver C1) |
| Content Quality | 23% | ~45 | Buena prosa, pero contradicciones factuales graves |
| On-Page SEO | 20% | ~65 | Títulos/meta únicos en 100%, pero 18/42 exceden longitud |
| Schema / Structured Data | 10% | 10 | Solo 1 de 42 páginas tiene JSON-LD |
| Performance (CWV, estimado) | 10% | ~35 | 69MB de imágenes sin optimizar, sin lazy loading |
| AI Search Readiness (GEO) | 10% | 36 | FAQ es buen activo; blog y tours no son citables |
| Images | 5% | ~15 | 0% con width/height/alt sistemático/formato moderno |
| **TOTAL PONDERADO** | | **≈ 42/100** | **Potencial tras arreglar críticos: 75-80/100** |

El score real está artificialmente bajo por un único motivo dominante: **el dominio de producción no existe en DNS**, lo que invalida toda indexación (Google y LLMs) independientemente de cuánto se mejore el contenido. Es, con diferencia, el primer fix.

---

## Los 5 hallazgos más críticos (bloquean todo lo demás)

### 1. El dominio `natalexperience.com` no resuelve en DNS
Verificado con `nslookup`: *"Non-existent domain"*. Robots.txt, sitemap.xml, todos los `canonical` y `og:url` apuntan ahí. El sitio real vive en `https://natal-experience.vercel.app/`. **Mientras esto no se resuelva, Google y los crawlers de IA no pueden indexar nada — cero ROI en cualquier otra mejora.** Solución exacta en `01-technical.md` (C1): añadir el dominio en Vercel → Settings → Domains, crear los registros DNS que Vercel indique en el registrador (ej. registro.br), esperar propagación, verificar en Search Console.

### 2. Contradicción factual: "30 años de experiencia" vs "18 años" — repetida en 30+ archivos
El hero/quem-somos.html dice "mais de 30 anos"; el footer (presente en las 42 páginas) dice "Há mais de 18 anos". Es la afirmación de autoridad más visible del sitio y se contradice a sí misma en cada página. Esto destruye tanto E-E-A-T (Trustworthiness) como la citabilidad por LLMs — un modelo de IA no puede citar con confianza un dato que cambia de página a página dentro del mismo dominio. **Acción:** decidir una sola cifra real (años de la empresa vs. años de experiencia personal del fundador Junior, si son distintos, y decirlo explícitamente).

### 3. Cero datos estructurados (Schema.org) en 41 de 42 páginas
Solo `faq.html` tiene JSON-LD. Ni la home, ni los 16 tours de `/passeios/`, ni los 10 de `/experiencias-exclusivas/` tienen `LocalBusiness`, `Product`/`Offer`, `BreadcrumbList` ni `Review`. `03-schema.md` entrega el JSON-LD completo listo para pegar en cada tipo de página, usando solo datos reales confirmados en el sitio (no se inventó nada).

### 4. 69MB de imágenes sin optimizar — riesgo severo de Core Web Vitals
`img/parachos.png` (7MB), `img/f1.jpg` (5.8MB), etc. Ninguna imagen muestreada tiene `width`/`height`, `loading="lazy"` ni formato moderno (WebP/AVIF). Esto es la causa más probable de un LCP "Poor" (>4s) en cualquier página con hero image, y afecta directamente tanto al ranking en Google (Core Web Vitals es factor de ranking) como a la tasa de conversión móvil.

### 5. El blog nunca enlaza a las páginas de venta — y no es citable por IA
Los 8 artículos de `/blog/` (la superficie con más keywords informacionales de cola larga) no tienen ni un solo enlace hacia `/passeios/` o `/experiencias-exclusivas/`. Además, frases como *"o custo-benefício é excelente"* sin dar el precio real hacen que el blog sea inútil para que un LLM cite una respuesta concreta — mientras que `faq.html` sí da cifras exactas. Es la desconexión entre "contenido que atrae tráfico informacional" y "páginas que venden", y entre "contenido citable" y "contenido genérico".

---

## Hallazgo de seguridad colateral (no es SEO, pero es urgente)

`apps-script/Code.gs` contiene un Google Sheet ID hardcodeado en texto plano, y está trackeado en git sin excluirse del despliegue de Vercel — es servible públicamente como archivo estático junto con los scripts `.py` de la raíz (que también exponen rutas locales del PC del desarrollador). Detalle y solución en `01-technical.md` (C2, H7/L1).

---

## Qué SÍ está bien hecho (no tocar)

- Estructura de URLs limpia, semántica, sin parámetros ni mayúsculas.
- HTML 100% estático (sin CSR) — Googlebot lee todo el contenido sin ejecutar JS.
- Títulos y meta descriptions únicos en el 100% de las 42 páginas (sin duplicados ni ausentes).
- `experiencias.html` enlaza correctamente a 25 de 26 páginas de tours — arquitectura de hub mayormente intencional.
- Las 3 variantes de buggy litoral norte y las 3 de Maracajaú SÍ están bien diferenciadas en contenido (no hay duplicado real, aunque sí cierto riesgo de cannibalización de keywords — ver `04-keywords-clusters.md`).
- `faq.html` ya tiene `FAQPage` JSON-LD bien formado con datos concretos — es el mejor activo de citabilidad IA del sitio hoy.
- NAP (nombre/dirección/teléfono) consistente internamente entre footer y `contato.html`.

---

## Resumen por área (ver detalle en cada archivo)

**Técnico:** dominio caído (crítico), exposición de Sheet ID (crítico), faltan headers de seguridad en `vercel.json`, imágenes sin optimizar, blog sin enlaces a ventas, 1 página huérfana (`litoral-sul-4x4.html`), `lastmod` idéntico en sitemap (artefacto del generador), `robots.txt` no declara bots de IA explícitamente, 18/42 meta descriptions exceden 160 caracteres (todas las de `/experiencias-exclusivas/`).

**Contenido:** contradicción 30/18 años (crítico), mezcla español/portugués en copyright en 25+ páginas incluida una frase híbrida "Todos os derechos reservados" (crítico — marca de contenido IA sin revisar), fechas de footer ©2025 vs ©2026 inconsistentes entre blog y resto del sitio (crítico), páginas VIP (helicóptero, veleiro, transfer) extremadamente thin (1-2 frases genéricas), bug de HTML roto en `transfer-vip.html`, nombre de archivo de imagen en español con timestamp de hoy (evidencia de procesado IA sin limpiar), redes sociales placeholder.

**Schema:** 1/42 páginas con JSON-LD. Recomendado por prioridad: BreadcrumbList → Product+Offer (con additionalType TouristTrip) → TravelAgency+WebSite → FAQPage (ya parcial, falta completar 7 de 14 preguntas) → Review/AggregateRating (solo si los testimonios son reales y verificables) → BlogPosting.

**Keywords/Clusters:** cannibalización confirmada entre `litoral-sul-4x4.html` y `litoral-sul-vip-4x4.html` (mismo contenido), y no resuelta entre las variantes de duración de buggy norte/Maracajaú. Gap de mayor oportunidad: "melhor época para ir a Natal" (alta demanda, cero página propia). Otros gaps: "onde ficar em Natal", transporte aeroporto, "Natal com crianças", "Natal para lua de mel", página propia de Genipabu. El blog no enlaza a los tours (ver hallazgo crítico #5 arriba).

**GEO/IA:** dominio caído invalida todo (ver crítico #1). `faq.html` es citable; blog y páginas de tour no dan respuesta directa en los primeros 40-60 palabras ni mini-FAQ propio. `voo-helicoptero.html` usa "Sob Consulta" como precio — pésimo para citación (un LLM no puede citar un precio inexistente). Diseñado robots.txt explícito para bots de IA (permitir GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.; bloquear solo Bytespider) y llms.txt completo — ambos listos en `05-geo-ai-readiness.md`.

**Local SEO:** Score 21/100. Google Business Profile no encontrado (acción #1 antes que cualquier táctica). NAP consistente internamente, teléfono coherente con DDD 84 (RN). Reviews actuales son testimonios sin fecha ni verificación — debilidad activa, no solo oportunidad perdida. Maps embed fue removido deliberadamente del código (`<!-- Map removed per user request -->`) — se recomienda revertir.

---

## Próximo paso recomendado

Ver [`ACTION-PLAN.md`](ACTION-PLAN.md) para la lista priorizada de qué hacer primero, con esfuerzo estimado.
