# Plan de Acción Priorizado — NatalExperience Tours

Leyenda de esfuerzo: 🟢 Bajo (minutos-1h) · 🟡 Medio (1-4h) · 🔴 Alto (días / requiere terceros)

---

## CRÍTICO — Hacer esta semana (bloquean todo lo demás)

| # | Acción | Esfuerzo | Detalle |
|---|---|---|---|
| 1 | Configurar el dominio `natalexperience.com` en Vercel y crear los registros DNS en el registrador (A → 76.76.21.21 para apex, CNAME → cname.vercel-dns.com para www). Verificar propagación y dar de alta el sitio en Google Search Console + enviar sitemap. | 🔴 | `01-technical.md` C1 |
| 2 | Resolver la contradicción "30 años" vs "18 años" de experiencia. Decidir una cifra real (empresa vs. fundador) y unificarla en las 42 páginas (hero, footer, meta descriptions, stats counter). | 🟡 | `02-content.md` C1 |
| 3 | Excluir del despliegue de Vercel los scripts `.py` y `apps-script/` (crear `.vercelignore`); rotar el Sheet ID si el repo/deploy ya fue público. | 🟢 | `01-technical.md` C2 |
| 4 | Unificar el aviso de copyright: una sola cadena `© 2026 NatalExperience Tours. Todos os direitos reservados.` en las ~44 páginas (hoy hay 4 variantes mezclando español/portugués, incluida una híbrida). | 🟢 | `02-content.md` C2 |
| 5 | Crear/reclamar el Google Business Profile como "Tour operator" en Natal, RN. Hoy no existe ninguna presencia indexada. | 🔴 | `06-local-seo.md` |

---

## ALTA PRIORIDAD — Próximas 2 semanas

| # | Acción | Esfuerzo | Detalle |
|---|---|---|---|
| 6 | Implementar JSON-LD: `BreadcrumbList` (26 páginas de tours) + `Product`/`Offer` con `additionalType: TouristTrip` (26 páginas) + `TravelAgency`/`WebSite` (home). Bloques listos en `03-schema.md`. | 🟡 | `03-schema.md` |
| 7 | Optimizar las 115 imágenes: convertir a WebP/AVIF, redimensionar (hero ≤1920px, cards ≤800px), añadir `width`/`height` y `loading="lazy"` (excepto LCP de cada página). Objetivo: bajar de 69MB a <10MB. | 🔴 | `01-technical.md` H2 |
| 8 | Añadir 2-4 enlaces contextuales por artículo de blog hacia los tours relacionados (tabla de mapeo exacta en `01-technical.md` H4) + sección "Artigos relacionados" entre posts. | 🟡 | `01-technical.md` H4 |
| 9 | Reescribir el contenido del blog para que dé respuestas directas con cifras reales en los primeros 40-60 palabras (hoy frases como "o custo-benefício é excelente" sin precio matan la citabilidad). Añadir precio real explícito en TODAS las páginas, eliminando "Sob Consulta" (`voo-helicoptero.html` y otras). | 🟡 | `05-geo-ai-readiness.md` §2 |
| 10 | Ampliar el contenido thin de las páginas VIP (`voo-helicoptero.html`, `veleiro-noronha.html`, `transfer-vip.html`): storytelling real, fotos propias (hoy `veleiro-noronha.html` usa placeholders de texto), detalles específicos (modelo de aeronave/embarcación). | 🟡 | `02-content.md` H1 |
| 11 | Actualizar `robots.txt` con reglas explícitas para bots de IA (permitir GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.; bloquear Bytespider) + `Disallow: /apps-script/` y `/*.py$`. Bloque completo listo en `05-geo-ai-readiness.md`. | 🟢 | `05-geo-ai-readiness.md` §3 |
| 12 | Crear `llms.txt` en la raíz con el contenido propuesto en `05-geo-ai-readiness.md`. | 🟢 | `05-geo-ai-readiness.md` |
| 13 | Activar redes sociales reales (hoy Instagram/Facebook/YouTube son `href="#"`) y enlazarlas también desde el futuro Google Business Profile para reforzar la entidad de marca. | 🟡 | `02-content.md` H4 / `06-local-seo.md` |
| 14 | Resolver cannibalización confirmada entre `litoral-sul-4x4.html` y `litoral-sul-vip-4x4.html` (mismo contenido) — diferenciar o consolidar con redirect. Añadir `litoral-sul-4x4.html` a la navegación de `experiencias.html` (hoy es página huérfana). | 🟡 | `04-keywords-clusters.md` / `01-technical.md` H5 |

---

## MEDIA PRIORIDAD — Próximo mes

| # | Acción | Esfuerzo | Detalle |
|---|---|---|---|
| 15 | Añadir headers de seguridad y cache-control en `vercel.json` (bloque completo listo en `01-technical.md` H1). | 🟢 | `01-technical.md` |
| 16 | Recortar las 18 meta descriptions que exceden 160 caracteres (las 10 de `/experiencias-exclusivas/` son las peores, 179-226 car.) sin perder el CTA. Acortar 2 títulos que exceden 60 caracteres. | 🟢 | `01-technical.md` L3 |
| 17 | Añadir `og:title`/`og:description`/Twitter Card propios a las 41 páginas que solo heredan `og:url`/`og:image` — relevante porque el canal de venta principal es compartir por WhatsApp. | 🟡 | `01-technical.md` M5 |
| 18 | Crear página/pillar "Melhor época para visitar Natal" — mayor gap de keyword detectado, sin página propia hoy. | 🟡 | `04-keywords-clusters.md` |
| 19 | Diferenciar más agresivamente título/H1 de las 3 variantes de buggy litoral norte por duración explícita (2h/3h/7h) para reducir cannibalización; añadir tabla comparativa de precios/duración entre las variantes. | 🟡 | `04-keywords-clusters.md` / `02-content.md` |
| 20 | Añadir mini-FAQ con `FAQPage` schema en cada página de tour (duplicando preguntas relevantes ya redactadas en `faq.html`), y completar las 7 preguntas visibles en `faq.html` que faltan en su JSON-LD actual. | 🟡 | `03-schema.md` |
| 21 | Estrategia de reviews reales: pedir reseñas verificables (Google, TripAdvisor) en vez de solo testimonios de texto sin fecha/enlace; implementar `Review`/`AggregateRating` schema solo cuando sean reales. | 🔴 | `06-local-seo.md` |
| 22 | Citations locales: directorios de turismo de RN (Setur-RN), TripAdvisor, sitios regionales — más allá de Google. | 🔴 | `06-local-seo.md` |
| 23 | Revertir el Maps embed removido (`<!-- Map removed per user request -->`) en la página de contacto. | 🟢 | `06-local-seo.md` |
| 24 | Corregir `gen_pages.py`/`apply_seo.py` para que `lastmod` del sitemap use la fecha real de modificación del archivo, no `datetime.now()` global. Ajustar prioridades del sitemap (home=1.0, legales=0.3). | 🟢 | `01-technical.md` M3/M4 |
| 25 | Arreglar el HTML roto en `transfer-vip.html:71` (`</div>iv>`) y renombrar el archivo de imagen con texto en español/timestamp en `buggy-litoral-intermedio.html`. | 🟢 | `02-content.md` H2/H3 |
| 26 | Unificar fechas de footer (©2025 vs ©2026 entre blog y resto del sitio) y revisar/actualizar la fecha de vigencia de `politica-privacidade.html` (dice "abril 2024"). | 🟢 | `02-content.md` C3 |

---

## BAJA PRIORIDAD — Backlog

| # | Acción | Esfuerzo |
|---|---|---|
| 27 | Migrar estilos inline (`style="..."`) a clases CSS reutilizables — facilita adoptar CSP estricta a futuro. | 🔴 |
| 28 | Añadir `defer` a `js/main.js` en las 42 páginas. | 🟢 |
| 29 | Implementar IndexNow (ping a Bing/Yandex) tras resolver el dominio. | 🟢 |
| 30 | Evaluar versión en inglés/español de las páginas de mayor conversión para turismo internacional (requeriría `hreflang` correcto en ese momento). | 🔴 |
| 31 | Crear página informacional propia para Genipabu (demanda de búsqueda independiente confirmada, hoy solo se menciona dentro de otros tours). | 🟡 |
| 32 | Cubrir gaps de audiencia: "onde ficar em Natal", "Natal com crianças", "Natal para lua de mel", contenido de apoyo para `transfer-vip.html` (aeroporto). | 🟡 |

---

## Orden de ejecución sugerido (resumen en una frase)

**Dominio → contradicciones factuales/legales → schema básico → imágenes → enlazado interno blog→ventas → GEO (robots.txt IA + llms.txt) → Google Business Profile → el resto.**
