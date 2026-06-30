# Auditoría GEO (Generative Engine Optimization) — NatalExperience Tours

**Fecha:** 2026-06-26
**Sitio auditado (deploy real accesible):** https://natal-experience.vercel.app/
**Dominio canónico declarado (robots.txt, sitemap.xml, todas las `<link rel="canonical">`):** https://www.natalexperience.com.br/ — **NO RESUELVE EN DNS** ("Non-existent domain")
**Código fuente:** `E:\ANTIGRAVITY\NATALEXPERIENCE`
**Idioma:** pt-BR (turismo receptivo en Natal, Rio Grande do Norte, Brasil)
**Páginas auditadas:** 42 (home, experiencias.html, quem-somos.html, faq.html, blog.html, contato.html, 16 `/passeios/`, 10 `/experiencias-exclusivas/`, 8 `/blog/`, 2 legales)

---

## 0. Bloqueador crítico (antes de cualquier optimización GEO)

Todo el trabajo de GEO de este informe es **inútil en la práctica** hasta resolver esto:

- `robots.txt` → `Sitemap: https://www.natalexperience.com.br/sitemap.xml`
- `sitemap.xml` → 42 URLs, todas con `https://www.natalexperience.com.br/...`
- Cada página → `<link rel="canonical" href="https://www.natalexperience.com.br/...">` y `og:url` apuntando al mismo dominio inexistente.
- El dominio `www.natalexperience.com.br` **no resuelve en DNS**. El sitio real y accesible está en `https://natal-experience.vercel.app/`.

**Consecuencia para GEO:** los crawlers de IA (GPTBot, PerplexityBot, ClaudeBot, OAI-SearchBot) descubren contenido a través de: (a) rastreo directo, (b) índice de Bing/Google (Copilot y Google AIO dependen de estos índices), o (c) enlaces compartidos. Si el dominio canónico no resuelve, ningún motor puede indexar nada bajo esa URL, y todo el `og:url`/canonical apunta a un agujero negro. Aunque Vercel sea rastreable, las señales de canonicalización contradicen la URL real, lo que puede hacer que buscadores y LLMs descarten o deduplique incorrectamente el contenido.

**Acción obligatoria antes de cualquier otra recomendación de este informe:**
1. Comprar/activar el dominio `natalexperience.com.br` y apuntar DNS al deploy de Vercel, O
2. Cambiar **todas** las referencias canónicas (`canonical`, `og:url`, `sitemap.xml`, `robots.txt`) al dominio Vercel real (o a un dominio propio que sí resuelva) antes de invertir en contenido/llms.txt/robots.txt — de lo contrario cualquier mejora de contenido será invisible para los crawlers.

Este informe asume que el bloqueador de dominio se resuelve y entrega las mejoras de GEO en paralelo para que estén listas en el momento del lanzamiento del dominio correcto.

---

## 1. Verificación de accesibilidad y citabilidad general del sitio

`https://natal-experience.vercel.app/` es accesible y se renderiza correctamente (confirmado vía fetch). Hallazgos generales de citabilidad:

- La home es **parcialmente autocontenida**: presenta categorías de tours, rango de precios (R$400–R$980 buggy, R$170–R$280 Maracajaú, R$75 Pipa) y duración (2–8h), pero para precios exactos y detalles de itinerario remite a páginas internas — correcto desde el punto de vista de UX, pero significa que la home por sí sola no es la mejor fuente citable; las páginas de detalle de tour y el FAQ deben cargar ese peso.
- El footer (presente en las 42 páginas) contiene la única declaración de "años de experiencia" que un LLM vería de forma consistente en casi cualquier página — y es precisamente la que **contradice** al hero/quem-somos.html (ver sección 6).
- No hay JSON-LD de `Organization`, `LocalBusiness` o `TouristTrip` (auditado en detalle por otro agente) — esto reduce significativamente la probabilidad de que un LLM "ancle" datos NAP (Name-Address-Phone) y de precio de forma estructurada, obligándolo a inferir desde texto libre, lo que aumenta la probabilidad de error/alucinación al citar.

---

## 2. Passage-level citability: FAQ y blog

### 2.1 `faq.html` — el mejor activo de citabilidad del sitio (calificación: BUENO, con margen de mejora)

`faq.html` (`E:\ANTIGRAVITY\NATALEXPERIENCE\faq.html`) ya implementa:
- Esquema **`FAQPage` JSON-LD** completo y bien formado (7 preguntas en el `<head>`, líneas 12-75) — esto es exactamente lo que Google AI Overviews y Bing Copilot buscan para extracción directa.
- Preguntas en formato de pregunta natural ("Qual é a melhor época do ano para visitar Natal RN...?", "Quanto custa o passeio de buggy em Genipabu?") — coincide con el patrón de queries reales de usuarios/LLMs.
- Respuestas con datos concretos: "R$ 600 a R$ 800 por buggy", "85 km ao sul de Ponta Negra", "1 hora e 20 minutos", "40 km da Praia de Ponta Negra".

**Problemas de citabilidad detectados:**
- **Longitud de pasajes fuera del rango óptimo (134-167 palabras):** la mayoría de las respuestas HTML visibles (no el JSON-LD, que es más corto) tienen entre 90-150 palabras pero varias exceden 160-180 palabras al combinar 2-3 ideas en un solo bloque (ej. la respuesta de "Maracajaú ou Perobas" mezcla 3 sub-respuestas con `<br>` en un solo `<p>`, dificultando la extracción de una "respuesta única" limpia).
- **Inconsistencia entre el texto del JSON-LD y el texto visible en HTML.** Ej.: el JSON-LD de "buggy em Genipabu" dice "a partir de R$ 600", el HTML visible dice "R$ 600 a R$ 800... mais taxas de R$ 15 a R$ 20". Un LLM que cruce ambas fuentes (snapshot cacheado vs. render) puede citar cifras distintas — mismo patrón de riesgo que la contradicción de "18 vs 30 años".
- **Falta de atribución temporal/fecha de actualización** en la página o en el FAQPage schema (no hay `dateModified`), lo que reduce la confianza del LLM en que el precio sigue vigente.
- Las respuestas usan `<br>` dentro de un único `<p>` para listas (Maracajaú vs Perobas, roteiro 3 vs 5 días) en vez de `<ul>/<li>` reales — HTML semánticamente pobre para extracción estructurada; trafilatura y extractores boilerplate-strip suelen preservar mejor listas `<li>` que saltos de línea `<br>`.

### 2.2 Blog (`/blog/`) — calificación: DEFICIENTE para citabilidad de IA

Se revisaron `buggy-vale-a-pena.html`, `norte-ou-sul.html`, `guia-natal.html` y `roteiro-5-dias-natal.html`. Patrón consistente en los 4:

- **Sin JSON-LD `Article`/`BlogPosting`** (sin `datePublished` real verificable más allá del texto visual "📅 05 de Janeiro, 2026").
- **Sin datos concretos extraíbles.** Ejemplo textual de `buggy-vale-a-pena.html`: *"O valor do passeio pode variar conforme temporada, tipo de buggy e roteiro escolhido, mas na maioria dos casos, o custo-benefício é excelente"* — esto es **lo opuesto** a una respuesta citable. Un LLM no puede extraer un precio de esa frase. Compárese con la respuesta equivalente en `faq.html`, que sí da R$ 600-800. Este artículo de blog, que en teoría responde "¿vale la pena el buggy?", nunca da el precio ni el rango horario.
- **Párrafos de transición sin valor informativo** ("Mas afinal, o passeio de buggy em Natal realmente vale a pena?" como párrafo aislado de una sola frase) — diluyen la densidad de información por pasaje, empeorando la proporción señal/ruido que los extractores tipo trafilatura entregan al LLM.
- **H2 no siempre en formato pregunta.** "A Experiência em Genipabu", "Buggy no Litoral Sul?", "Privativo ou Compartilhado?" — mezcla de formatos; los H2 que sí son preguntas (p.ej. "Qual é o melhor para você?" en `norte-ou-sul.html`) generan respuestas más extraíbles que los que son solo etiquetas temáticas.
- **roteiro-5-dias-natal.html es el mejor del grupo**: usa subtítulos H2 por día ("Dia 1: ...", "Dia 2: ...") con datos concretos (85 km, 100 metros de duna, 7 km de costa) y una lista `<ul><li>` real para comparar Maracajaú vs. Perobas — es el único post de blog con estructura semi-tabular.
- Ningún artículo de blog enlaza de vuelta a `faq.html` o usa su contenido para evitar contradicciones; en cambio, repiten de memoria datos (ej. "85 km" aparece igual en `faq.html` y en `roteiro-5-dias-natal.html`, pero el precio del buggy norte NUNCA aparece en el blog, solo en FAQ y en `/passeios/`).

**Conclusión de la sección 2:** Existe una working answer engine (`faq.html`) con buenos datos, pero estos datos no se replican/citan de forma consistente en el blog, que es la superficie con más palabras clave de "intención informativa" (justo el tipo de contenido que ChatGPT/Perplexity prefieren citar antes que páginas de venta). El blog necesita reescritura orientada a respuesta directa, no solo SEO clásico de "guía de viaje".

### 2.3 Páginas de tours (`/passeios/`, `/experiencias-exclusivas/`)

Ejemplo analizado en detalle: `passeios/buggy-litoral-norte.html` y `experiencias-exclusivas/voo-helicoptero.html`.

**Fortalezas (buggy-litoral-norte.html):**
- Precio explícito y prominente: "A partir de R$ 780" (sidebar + sticky CTA mobile).
- Duración explícita: "~7 horas". Hora de salida: "08:00 - 09:00 (Hotel)".
- Listas reales `<ul class="tour-list">` para "O Que Está Incluído" / "Não Está Incluído" / "O Que Levar" — esto es buena estructura semántica, fácilmente extraíble.
- Itinerario hora por hora (08:00, 15:30) en `<p><strong>`.

**Debilidades (aplicables a las 16 páginas de `/passeios/` y especialmente a las 10 de `/experiencias-exclusivas/`):**
- **No hay bloque de "respuesta directa" en los primeros 40-60 palabras tras el H1.** El primer párrafo bajo "Sobre o Passeio" es descriptivo/emocional ("é a experiência mais icônica de Natal... aventura inesquecível...") en vez de responder de inmediato "¿qué es, cuánto cuesta, cuánto dura?" en una frase. Eso retrasa la señal más citable.
- **Cero formato de pregunta-respuesta en la página de producto.** No hay mini-FAQ por tour (ej. "¿Cuánto cuesta el buggy en Genipabu?", "¿Es seguro para niños?", "¿Qué pasa si llueve?") aunque esas respuestas ya existen en `faq.html` — son candidatas perfectas para duplicar (con `FAQPage` schema) en cada página de tour relevante, ya que los LLMs citan con más frecuencia la página más específica/profunda para la query exacta.
- **`voo-helicoptero.html` (y se presume varias de `/experiencias-exclusivas/`) usa "Sob Consulta" como precio.** Esto es el peor escenario posible para citabilidad: un LLM no puede citar un precio inexistente, así que omitirá la página o (peor) inventará una cifra alucinada basada en datos de internet no verificados sobre vuelos en helicóptero en general. Se recomienda **siempre** dar al menos un rango/precio de referencia ("A partir de R$ X para até 4 passageiros", aunque sea "preço de partida estimado, sujeito a confirmação").
- No hay tabla comparativa de precios/duración entre tours similares (ej. comparar los 4 paseos de buggy: litoral-norte, litoral-sul-pipa, litoral-alternativo, litoral-intermedio) en ninguna página central — esto sería un imán de citación tipo "tabla" que ChatGPT/Perplexity adoran reproducir.

---

## 3. robots.txt mejorado — reglas explícitas para bots de IA

### 3.1 Estado actual

```
User-agent: *
Allow: /

Sitemap: https://www.natalexperience.com.br/sitemap.xml
```

Esto permite todo por defecto, pero **no declara intención** respecto a crawlers de IA. Riesgo: si en el futuro el cliente quiere bloquear bots de entrenamiento (CCBot, etc.) sin saberlo está permitiéndolos por el wildcard `*`, y no hay forma de auditar/demostrar a un cliente o stakeholder qué bots están explícitamente permitidos para búsqueda de IA.

### 3.2 Decisión por bot (objetivo: visibilidad en LLMs + Google/Bing tradicional)

| Bot | Empresa | Función | Decisión | Justificación |
|---|---|---|---|---|
| `GPTBot` | OpenAI | Entrenamiento de modelos GPT | **Permitir** | El cliente quiere visibilidad en ChatGPT. Bloquear `GPTBot` no impide que ChatGPT cite la página (eso lo hace `OAI-SearchBot`), pero si se bloquea, OpenAI puede excluir el dominio de fuentes "de confianza" para algunos productos. Para una agencia de turismo que busca exposición de marca, permitir es la opción correcta. |
| `OAI-SearchBot` | OpenAI | Indexación para ChatGPT Search (respuestas con citas en vivo) | **Permitir** | Es el crawler que directamente alimenta las citas que ChatGPT muestra a usuarios buscando "passeios em Natal". Bloquearlo elimina la posibilidad de aparecer citado en ChatGPT Search. |
| `ChatGPT-User` | OpenAI | Acciones en tiempo real cuando un usuario pide a ChatGPT que abra/lea una URL específica | **Permitir** | Si un turista pide a ChatGPT "abre el sitio de NatalExperience y dime los precios", este user-agent necesita acceso. Bloquearlo rompe esa experiencia activamente solicitada por el usuario final. |
| `ClaudeBot` | Anthropic | Rastreo para grounding de respuestas de Claude (incluye Claude with web search) | **Permitir** | Mismo argumento que OAI-SearchBot — visibilidad en respuestas de Claude. |
| `Claude-User` / `Claude-SearchBot` | Anthropic | Variantes de fetch en tiempo real / indexación de búsqueda | **Permitir** | Mismo criterio: visibilidad activa solicitada por el cliente. |
| `anthropic-ai` | Anthropic | Legado/entrenamiento general | **Permitir** | Riesgo de uso en entrenamiento de modelo, pero el beneficio de marca (ser una fuente conocida/citada por Claude) supera el costo para un negocio local que vive de visibilidad, no de contenido propietario monetizable. |
| `PerplexityBot` | Perplexity | Rastreo para respuestas con citas de Perplexity AI | **Permitir** | Perplexity es una de las superficies de búsqueda con IA de mayor crecimiento; el cliente explícitamente quiere visibilidad aquí. |
| `Perplexity-User` | Perplexity | Fetch en tiempo real bajo petición de usuario | **Permitir** | Igual que ChatGPT-User. |
| `Google-Extended` | Google | Controla uso del contenido en Gemini/AI Overviews (independiente de Googlebot clásico) | **Permitir** | Crítico: si se bloquea `Google-Extended`, el contenido puede seguir apareciendo en Google Search normal, pero **se excluye de Google AI Overviews y Gemini** — justo uno de los 4 motores objetivo declarados por el cliente. Debe permitirse explícitamente. |
| `Applebot-Extended` | Apple | Controla uso del contenido en Apple Intelligence / Siri (no afecta indexación clásica de Applebot/Spotlight) | **Permitir** | Apple Intelligence y Siri están integrando respuestas generativas; para una agencia de turismo orientada también a visitantes internacionales (testimonios de Lisboa, Buenos Aires), tener presencia en el ecosistema Apple es positivo y de bajo riesgo. |
| `Bingbot` | Microsoft | Indexación clásica de Bing — alimenta directamente Bing Copilot | **Permitir** (ya permitido por `*`, pero se declara explícito) | Bing Copilot usa el índice de Bing; sin Bingbot no hay Copilot. |
| `CCBot` | Common Crawl | Dataset abierto usado por múltiples LLMs (incluyendo modelos open-source) para entrenamiento | **Permitir, con reserva documentada** | Common Crawl es una fuente de entrenamiento amplia que alimenta indirectamente muchos modelos (incluidos los de Perplexity y otros). Bloquear no impide el entrenamiento de los grandes labs (tienen sus propios bots), solo reduce exposición en modelos más pequeños/open-source. Dado que el objetivo del cliente es maximizar menciones de marca, se recomienda **permitir**, pero queda documentado como la opción "bloqueable sin gran pérdida" si en el futuro el cliente cambia de estrategia (p. ej. por temas de derechos de imagen/precios). |
| `Bytespider` | ByteDance (TikTok) | Rastreo agresivo, históricamente con mal comportamiento (ignora rate limits) y sin buscador de IA con citación pública relevante en el mercado occidental/brasileño | **Bloquear** | No aporta valor de visibilidad de búsqueda con IA para el mercado objetivo (turistas que buscan en pt-BR/es/en vía ChatGPT, Google, Perplexity, Bing). Tiene historial documentado de sobrecarga de servidores. Bloquear protege el hosting de Vercel sin pérdida de visibilidad relevante. |
| `Amazonbot` | Amazon | Alexa/Amazon AI | **Permitir** | Bajo riesgo, beneficio potencial en asistentes Alexa para turismo. |
| `Meta-ExternalAgent` | Meta | Entrenamiento + posible uso en Meta AI | **Permitir** | Meta AI está integrado en WhatsApp e Instagram — canales que esta agencia ya usa activamente (CTA de WhatsApp en todo el sitio). Coherente con el canal de venta real del negocio. |
| `DuckAssistBot` | DuckDuckGo | Respuestas de IA de DuckDuckGo | **Permitir** | Bajo riesgo, visibilidad adicional. |

### 3.3 Contenido propuesto para `robots.txt`

Reemplazar el contenido de `E:\ANTIGRAVITY\NATALEXPERIENCE\robots.txt` por:

```
# robots.txt — NatalExperience Tours
# Política: maximizar visibilidad en buscadores tradicionales y en motores de
# busca com IA (ChatGPT, Perplexity, Claude, Google AI Overviews, Bing Copilot).
# Atualizado em 2026-06-26.

User-agent: *
Allow: /

# ===== Crawlers de busca tradicional (sempre permitidos) =====
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# ===== IA / Respostas com citação em tempo real (alta prioridade) =====
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# ===== Treinamento de modelos de IA (visibilidade de marca a médio prazo) =====
User-agent: GPTBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: DuckAssistBot
Allow: /

User-agent: CCBot
Allow: /

# ===== Bloqueados: sem benefício de visibilidade comprovado para o mercado- =====
# ===== alvo (pt-BR/es/en, turismo) e com histórico de comportamento agressivo =====
User-agent: Bytespider
Disallow: /

# ===== Sitemap =====
Sitemap: https://www.natalexperience.com.br/sitemap.xml
```

**Nota crítica:** este `robots.txt` debe publicarse en el dominio que realmente se use (ver Sección 0). Si se mantiene Vercel como dominio de producción, cambiar la línea `Sitemap:` a `https://natal-experience.vercel.app/sitemap.xml` o al dominio final que se active.

---

## 4. llms.txt propuesto

No existe actualmente `llms.txt` en la raíz (`E:\ANTIGRAVITY\NATALEXPERIENCE\llms.txt` no existe). El estándar emergente (llmstxt.org) espera un Markdown con: H1 (nombre), blockquote de resumen, secciones H2 con listas de enlaces `[título](url): descripción`.

### Contenido propuesto — guardar como `E:\ANTIGRAVITY\NATALEXPERIENCE\llms.txt`

```markdown
# NatalExperience Tours

> Agência de turismo receptivo em Natal, Rio Grande do Norte, Brasil. Operamos
> passeios clássicos (buggy, mergulho, praias) e experiências exclusivas
> (helicóptero, veleiro, transfers VIP) na região de Natal, Genipabu, Pipa,
> Maracajaú, Perobas e São Miguel do Gostoso. Atendimento em português,
> espanhol e inglês via WhatsApp.

Este arquivo lista as páginas mais relevantes do site para sistemas de IA que
buscam responder perguntas sobre turismo em Natal RN: preços de passeios,
duração, melhor época para visitar, roteiros e experiências disponíveis.
Todos os preços estão em Reais (BRL) e sujeitos a alteração por temporada;
confirme valores atualizados em contato direto.

## Informações Essenciais

- [Perguntas Frequentes](/faq.html): Respostas diretas sobre melhor época para
  visitar Natal, preços de buggy em Genipabu, distância até Pipa, comparação
  Maracajaú vs. Perobas, distância do aeroporto, roteiro de 3-5 dias, segurança
  para crianças/idosos, reservas, pagamentos e política de chuva.
- [Quem Somos](/quem-somos.html): História da empresa e do fundador Junior,
  guia local em Natal.
- [Contato](/contato.html): WhatsApp, e-mail, endereço (Rua Túlio Fernandes,
  415 - Praia do Meio, Natal - RN, 59010-038, Brasil) e telefone
  +55 84 99986-8411.

## Passeios Clássicos (Preços e Duração)

- [Litoral Norte Completo (Buggy)](/passeios/buggy-litoral-norte.html): Buggy
  pelas dunas de Genipabu, Lagoa de Pitangui e Jacumã. ~7 horas. A partir de
  R$ 780 por buggy (até 4 pessoas).
- [Litoral Sul / Pipa (Buggy)](/passeios/buggy-litoral-sul-pipa.html): Buggy
  pelo litoral sul até a Praia de Pipa. ~7 horas. A partir de R$ 800 por buggy.
- [Litoral Alternativo (Buggy)](/passeios/buggy-litoral-alternativo.html):
  Roteiro de buggy alternativo ao tradicional Genipabu.
- [Litoral Intermédio (Buggy)](/passeios/buggy-litoral-intermedio.html):
  Roteiro intermediário de buggy.
- [City Tour de Buggy](/passeios/city-tour-buggy.html): Tour histórico e
  urbano de Natal em buggy.
- [Pipa - Dia Inteiro](/passeios/pipa.html): Passeio bate e volta à Praia de
  Pipa, falésias e Baía dos Golfinhos. A partir de R$ 75 por pessoa.
- [Maracajaú - Mergulho nos Parrachos](/passeios/maracajau.html): Snorkel e
  mergulho de cilindro em piscinas naturais de até 3m de profundidade. A
  partir de R$ 220 por pessoa.
- [Maracajaú de Catamarã](/passeios/maracajau-catamara.html): Mesma região,
  opção de transporte por catamarã.
- [Maracajaú: Buggy + Mergulho](/passeios/maracajau-buggy-mergulho.html):
  Combo de buggy e mergulho em um único dia.
- [Perobas (Parrachos do Rio do Fogo)](/passeios/perobas.html): Piscinas
  naturais rasas (0,5-1m), ideais para famílias e crianças. ~8 horas. A
  partir de R$ 185.
- [Litoral Sul 4x4](/passeios/litoral-sul-4x4.html): Passeio off-road pelo
  litoral sul. R$ 170 por pessoa.
- [Litoral Sul 4x4 VIP](/passeios/litoral-sul-vip-4x4.html): Versão privativa
  do passeio 4x4 no litoral sul.
- [Litoral Sul - Águas](/passeios/litoral-sul-aguas.html): Passeio com foco em
  praias e águas do litoral sul.
- [São Miguel do Gostoso](/passeios/sao-miguel-do-gostoso.html): Vilarejo de
  kitesurf ao norte de Natal. Dia inteiro. A partir de R$ 125.
- [Galinhos](/passeios/galinhos.html): Vilarejo de pescadores e dunas no
  litoral norte do RN.
- [Pôr do Sol no Rio Potengi](/passeios/por-do-sol-potengi.html): Passeio de
  barco ao entardecer em Natal.

## Experiências Exclusivas (Premium / VIP)

- [Voo Panorâmico de Helicóptero](/experiencias-exclusivas/voo-helicoptero.html):
  Sobrevoo de 15-30 min sobre dunas e litoral de Natal. Preço sob consulta.
- [Rota Norte de Helicóptero](/experiencias-exclusivas/rota-norte-helicoptero.html):
  Sobrevoo expandido do litoral norte.
- [Passeio de Avião](/experiencias-exclusivas/passeio-aviao.html): Voo
  panorâmico em avião de pequeno porte.
- [Veleiro para Fernando de Noronha](/experiencias-exclusivas/veleiro-noronha.html):
  Charter de veleiro com destino a Fernando de Noronha.
- [Buggy VIP](/experiencias-exclusivas/buggy-vip.html): Versão privativa e
  premium do passeio clássico de buggy.
- [Mergulho VIP em Maracajaú](/experiencias-exclusivas/mergulho-maracajau.html):
  Versão exclusiva do mergulho em Maracajaú.
- [São Miguel do Gostoso VIP](/experiencias-exclusivas/vip-sao-miguel.html):
  Versão privativa do passeio a São Miguel do Gostoso.
- [Transfer VIP](/experiencias-exclusivas/transfer-vip.html): Transporte
  privativo aeroporto-hotel e entre destinos.
- [Rota Secreta das Praias](/experiencias-exclusivas/rota-secreta-praias.html):
  Roteiro exclusivo por praias menos conhecidas do RN.
- [Rota Natal-Fortaleza](/experiencias-exclusivas/rota-natal-fortaleza.html):
  Roteiro estendido entre Natal e Fortaleza.

## Blog / Guias de Viagem

- [O Que Fazer em Natal RN: Guia Completo](/blog/guia-natal.html): Visão
  geral das principais atrações: Genipabu, Pipa, Maracajaú/Perobas.
- [Melhores Passeios em Natal](/blog/melhores-passeios.html): Ranking dos
  passeios mais procurados pelos turistas.
- [Melhores Lagoas de Natal](/blog/melhores-lagoas-natal.html): Guia das
  lagoas de água doce na região (Pitangui, Jacumã e outras).
- [Mergulho em Natal: Maracajaú vs. Perobas](/blog/mergulho-natal.html):
  Comparação detalhada entre os dois destinos de mergulho.
- [Roteiro de 5 Dias em Natal](/blog/roteiro-5-dias-natal.html): Itinerário
  dia a dia cobrindo Ponta Negra, Genipabu, Pipa, Maracajaú/Perobas e
  centro histórico.
- [Passeio de Buggy Vale a Pena?](/blog/buggy-vale-a-pena.html): Análise de
  custo-benefício do passeio de buggy mais procurado de Natal.
- [Pipa Bate e Volta](/blog/pipa-bate-e-volta.html): Guia do passeio de um
  dia a Praia de Pipa saindo de Natal.
- [Litoral Norte ou Sul: Qual Escolher?](/blog/norte-ou-sul.html):
  Comparação entre as duas regiões de passeio de buggy.

## Optional

- [Política de Privacidade](/politica-privacidade.html)
- [Política de Cookies](/politica-cookies.html)
```

**Notas de implementación:**
- Sustituir todos los precios de este `llms.txt` por una revisión manual del cliente antes de publicar — varios ya están desactualizados o ausentes en el código fuente actual (ej. helicóptero "sob consulta").
- Una vez resuelto el problema de dominio (Sección 0), todas las rutas deben usar el dominio final absoluto, no relativo, ya que algunos parsers de `llms.txt` esperan URLs completas. Si se confirma `www.natalexperience.com.br`, reemplazar cada `/passeios/...` por `https://www.natalexperience.com.br/passeios/...`.
- Mantener el archivo bajo control de versiones y actualizarlo cada vez que se publique un nuevo tour o cambien precios — un `llms.txt` desactualizado es tan dañino para la confianza de un LLM como no tenerlo.

---

## 5. Mejoras estructurales recomendadas para `/passeios/` y `/experiencias-exclusivas/`

Aplicar a las 26 páginas de tour (16 + 10). Orden de prioridad de implementación:

### 5.1 Bloque de "respuesta rápida" inmediatamente bajo el H1 (alto impacto, bajo esfuerzo)

Insertar un párrafo de 40-60 palabras, antes de cualquier copy emocional, que responda directamente: qué es, duración, precio desde, para quién es. Ejemplo para `buggy-litoral-norte.html`:

> *"O passeio Litoral Norte Completo é um tour de buggy de aproximadamente 7 horas pelas dunas de Genipabu, Lagoa de Pitangui e Lagoa de Jacumã, saindo do seu hotel em Natal às 08h. Preço a partir de R$ 780 por buggy privativo (até 4 pessoas). Ideal para famílias, casais e grupos que buscam aventura e paisagens icônicas do Rio Grande do Norte."*

Este patrón es la unidad mínima que un LLM puede extraer y citar sin necesitar el resto de la página.

### 5.2 Mini-FAQ específico por tour con `FAQPage` JSON-LD (alto impacto, esfuerzo medio)

Cada página de tour debería tener 3-5 preguntas específicas (no genéricas, ya cubiertas en `faq.html`), por ejemplo para `voo-helicoptero.html`:
- "Quanto custa o voo de helicóptero em Natal?"
- "Quanto tempo dura o voo panorâmico?"
- "Quantas pessoas podem voar juntas?"
- "Preciso de algum documento para o voo?"

Replicar el patrón JSON-LD ya usado en `faq.html` (líneas 12-75) en cada página de tour, con datos específicos de ese tour. Esto multiplica la superficie de "respuestas ricas" que Google AI Overviews y ChatGPT pueden extraer directamente de la página más específica posible, en lugar de depender solo del FAQ general.

### 5.3 Eliminar precios "Sob Consulta"; sustituir por rango de referencia (alto impacto, bajo esfuerzo)

Aplica al menos a `voo-helicoptero.html` y probablemente a varias de `/experiencias-exclusivas/` (veleiro, avião, transfer VIP — pendiente de auditoría página por página, pero el patrón del sidebar `"Sob Consulta"` sugiere que es sistemático en esa carpeta). Sustituir por: *"A partir de R$ X para até 4 passageiros (voos maiores sob consulta)"*. Un precio "ancla" siempre es más citable que "consulte-nos", incluso si el precio final varía.

### 5.4 Tabla comparativa de tours similares (impacto medio-alto, esfuerzo medio)

Crear (en `experiencias.html` o en una nueva página `comparativo-passeios.html`) una tabla HTML real (`<table>`, no divs) comparando los 4 tours de buggy y los 3 paquetes de mergulho/snorkel por: precio desde, duración, nivel de dificultad, indicado para (familias/aventureiros/casais). Las tablas HTML semánticas son uno de los formatos que más fácilmente se extraen y se citan textualmente en respuestas de IA generativa (Perplexity y Google AIO en particular suelen reproducir tablas completas).

### 5.5 Convertir listas con `<br>` dentro de un único `<p>` a `<ul><li>` reales (impacto medio, esfuerzo bajo)

Aplica a `faq.html` (Maracajaú vs Perobas, roteiro 3 vs 5 dias) y previsiblemente a textos similares en blog. HTML semánticamente correcto es más fiable para trafilatura/extractores boilerplate-strip que usan los pipelines de RAG de los buscadores de IA.

### 5.6 Reescribir el blog con la misma disciplina de datos concretos que ya existe en faq.html (impacto alto, esfuerzo medio-alto)

Los 8 posts de blog deben incorporar, en los primeros 1-2 párrafos de cada sección H2, al menos un dato verificable (precio, distancia, duración, profundidad, fecha) en vez de lenguaje puramente persuasivo ("vale a pena", "experiência incrível"). Usar `faq.html` como fuente única de verdad para evitar que el blog contradiga los datos del FAQ (ver problema de inconsistencia de precios señalado en 2.1/2.2).

### 5.7 Agregar JSON-LD `Article`/`BlogPosting` con `datePublished`/`dateModified` real a cada post (impacto medio, esfuerzo bajo)

Actualmente la fecha solo existe como texto visual ("📅 05 de Janeiro, 2026"). Sin marcado estructurado, los LLMs no pueden verificar con confianza la fecha de publicación/actualización, factor que pondera en cómo Google AI Overviews y Bing Copilot jerarquizan "freshness" de la fuente.

---

## 6. Señales de autoridad de marca / entidad

### 6.1 Contradicción factual de antigüedad (alto impacto negativo, ya verificado en el código)

- `index.html` (meta description, línea 7; hero subtitle, línea 74): **"Mais de 30 anos"**.
- `quem-somos.html` (meta description, línea 7; page-hero subtitle, línea 25; bio del fundador Junior, línea 40): **"mais de 30 anos"** (3 apariciones).
- Footer compartido — presente de forma **idéntica en las 42 páginas del sitio** (confirmado: 42 coincidencias de "Há mais de 18 anos" o "anos criando" en el grep total del proyecto): **"Há mais de 18 anos criando experiências inesquecíveis"**.

Esto es la contradicción factual más repetida y más visible del sitio para cualquier crawler: en cualquier página que un LLM indexe, el footer dice 18 años, pero las páginas "ancla" de marca (home, quem-somos) dicen 30. Un LLM que sintetice "¿cuántos años de experiencia tiene NatalExperience?" tiene 50/50 de probabilidad de citar el dato incorrecto, y en el peor caso puede señalar la propia inconsistencia al usuario (dañando la percepción de fiabilidad de la marca en la respuesta generada). **Se debe decidir una sola cifra verdadera y propagarla de forma idéntica en las 42 páginas** (la cifra del footer es la de mayor alcance/repetición, por lo que probablemente sea la más fácil de corregir centralizadamente si el footer es un include/componente compartido — confirmar con el agente que audita la arquitectura de templates).

### 6.2 NAP (Name-Address-Phone) — consistencia

- Nombre: "NatalExperience Tours" — consistente en todas las páginas revisadas.
- Dirección: "Rua Túlio Fernandes, 415 - Praia do Meio, Natal - RN, 59010-038, Brasil" — consistente en el footer de todas las páginas revisadas, pero el enlace de la dirección es `href="#"` (no enlaza a Google Maps/Google Business Profile) — **se pierde la oportunidad de reforzar la entidad geográfica vinculando a un perfil verificable**.
- Teléfono: `+55 84 99986-8411` — consistente, con `tel:` correcto.
- E-mail: `natalexperiencetours@gmail.com` — consistente. Nota: usar un dominio Gmail genérico (en vez de `@natalexperience.com.br`) es una señal débil de autoridad/profesionalismo para un LLM o para verificación humana de la entidad, y no ayuda al "entity graph" que vincula dominio + marca + contacto.

### 6.3 Redes sociales y presencia verificable externa (alto impacto negativo)

- Los iconos de Instagram, Facebook y YouTube en el footer son `href="#"` en todas las páginas — **no hay un solo perfil social verificable enlazado desde el sitio**.
- No se encontró ninguna referencia a Wikipedia, Reddit, TripAdvisor, Google Business Profile o LinkedIn en ninguna de las 42 páginas (`href="#"` placeholders son el único patrón presente).
- Según la correlación de señales de marca con citación en IA (YouTube ~0.737, Reddit alto, Wikipedia alto, Domain Rating solo ~0.266), **NatalExperience Tours actualmente no activa ninguna de las señales de alta correlación**. Esto es la brecha de autoridad más grande detectada: incluso con contenido perfecto en el propio dominio, los LLMs construyen "confianza en la entidad" mayormente a partir de menciones de terceros verificables (reseñas en TripAdvisor/Google, videos de YouTube de turistas o de la propia empresa, menciones en foros de Reddit de viajeros a Natal, perfil de Google Business).
- Sin presencia en YouTube (la señal más correlacionada con citación en IA según los datos de la industria), la empresa pierde la vía más eficaz de figurar en respuestas de ChatGPT/Perplexity sobre "mejores passeios em Natal".

### 6.4 Testimonios sin schema `Review`/`AggregateRating`

- Confirmado (contexto ya verificado por el usuario): testimonios de clientes de São Paulo, Lisboa y Buenos Aires existen como texto plano, sin `Review` schema. Esto significa que, aunque el contenido humano-legible es positivo y geográficamente diverso (señal de alcance internacional), un LLM no puede extraerlo como "prueba social estructurada" ni mostrarlo como rating/reseña en una respuesta enriquecida. Se recomienda envolver cada testimonio en JSON-LD `Review` anidado bajo `LocalBusiness`, con `reviewRating`, `author`, y si es posible `datePublished`.

### 6.5 Ausencia de autoría/expertise individual citable

- `quem-somos.html` presenta a "Junior" como fundador con 30 años de experiencia (cifra contradictoria, ver 6.1), pero no hay `Person` schema, no hay enlace a un perfil profesional verificable (LinkedIn), y no se le atribuye autoría a ningún contenido del blog (los 8 posts no tienen autor declarado). Para E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) — señal que tanto Google como los LLMs usan para ponderar confianza — la falta de autoría nombrada en contenido informativo (blog) es una brecha fácil de cerrar.

---

## 7. GEO Health Score estimado (0-100)

Aplicando el framework de 5 dimensiones declarado, basado en la evidencia recolectada (nota: sin acceso a herramientas de tracking de citación en vivo tipo DataForSEO en esta sesión, por lo que las puntuaciones de citabilidad/autoridad son estimaciones cualitativas fundamentadas en el código fuente, no medición de citación real):

| Dimensión | Peso | Estimación | Justificación breve |
|---|---|---|---|
| Citability | 25% | 55/100 | `faq.html` fuerte (FAQPage schema + datos concretos); blog débil (sin datos, sin schema); páginas de tour con buena estructura pero sin Q&A propio ni bloque de respuesta directa. |
| Structural Readability | 20% | 60/100 | Buen uso de H1/H2/H3 y listas `<ul>` en páginas de tour; uso de `<br>` en vez de listas en algunas respuestas FAQ; blog con H2 inconsistentes (mezcla pregunta/etiqueta). |
| Multi-Modal Content | 15% | 30/100 | Imágenes con `alt` descriptivo presentes, pero sin YouTube, sin transcripciones de video, sin infografías/tablas de datos. Hero usa video de Cloudinary sin transcripción ni datos estructurados `VideoObject`. |
| Authority & Brand Signals | 20% | 20/100 | Contradicción de antigüedad activa, cero redes sociales verificables, cero presencia en Wikipedia/Reddit/YouTube/TripAdvisor, testimonios sin schema, sin autoría en blog, email en dominio genérico Gmail. |
| Technical Accessibility | 20% | 15/100 (sin contar el bloqueador de dominio) | Sitio HTML estático, presumiblemente bien servido (SSR-equivalente, no SPA) — sería alto si no fuera por el dominio canónico roto, que es un fallo crítico de accesibilidad técnica (toda señal de canonicalización apunta a un dominio inexistente). |

**GEO Health Score ponderado: ≈ 36/100**, arrastrado principalmente por Authority & Brand Signals y Technical Accessibility. Si se resuelve solo el bloqueador de dominio (Sección 0), Technical Accessibility subiría a ~70-75/100 y el score global subiría a ~46-48/100 sin cambiar una línea de contenido — es la intervención de mayor ROI inmediato.

### Puntuaciones por plataforma (estimación cualitativa)

| Plataforma | Estimación | Razonamiento |
|---|---|---|
| Google AI Overviews | Bajo-Medio | Depende del índice de Google clásico; el FAQ schema ayuda, pero el problema de dominio y la falta de `Organization`/`LocalBusiness` schema limitan el "knowledge panel" potencial. |
| ChatGPT (Search/grounding) | Bajo | Sin presencia en fuentes de terceros (YouTube/Reddit) que ChatGPT prioriza para temas de viaje; contenido propio aceptable pero no diferenciado vs. competidores con más señales externas. |
| Perplexity | Bajo-Medio | Perplexity valora fuertemente estructura de pasaje y datos concretos — el FAQ ya ayuda aquí, pero la falta de actualidad (`dateModified`) y de fuentes externas limita el resultado. |
| Bing Copilot | Bajo | Mismo problema de dominio; Bing además pondera señales de autoridad de dominio (que aquí son débiles: sin backlinks de calidad conocidos, sin presencia social). |

---

## 8. Checklist priorizada de GEO

### Prioridad 0 — Bloqueador (hacer antes que cualquier otra cosa)
1. **Resolver el dominio canónico roto.** Activar DNS de `natalexperience.com.br` o migrar todas las referencias canónicas/sitemap/robots al dominio Vercel real. Sin esto, ninguna otra mejora es indexable. *(Esfuerzo: bajo-medio si es solo DNS; depende de quién gestiona el registro del dominio.)*

### Prioridad 1 — Alto impacto, esfuerzo bajo-medio
2. **Unificar la cifra de "años de experiencia"** en una sola verdad y propagarla de forma idéntica en las 42 páginas (footer + home + quem-somos). *(Esfuerzo: bajo si el footer es un componente compartido; medio si hay que editar cada archivo HTML individualmente.)*
3. **Eliminar todos los precios "Sob Consulta"** y sustituir por un rango de referencia concreto, empezando por `voo-helicoptero.html` y revisando el resto de `/experiencias-exclusivas/`. *(Esfuerzo: bajo — requiere solo que el cliente provea cifras.)*
4. **Agregar bloque de "respuesta rápida" (40-60 palabras)** inmediatamente bajo el H1 en las 26 páginas de `/passeios/` y `/experiencias-exclusivas/`. *(Esfuerzo: medio — redacción + implementación HTML repetitiva.)*
5. **Vincular los iconos de redes sociales reales** (Instagram, Facebook, YouTube) en el footer compartido, sustituyendo los `href="#"`. Si aún no existen perfiles, crearlos es prerrequisito. *(Esfuerzo: bajo técnico, medio si hay que crear las cuentas desde cero.)*
6. **Publicar `llms.txt`** con el contenido propuesto en la Sección 4. *(Esfuerzo: bajo.)*
7. **Publicar el `robots.txt` mejorado** de la Sección 3.3. *(Esfuerzo: bajo.)*

### Prioridad 2 — Impacto medio-alto, esfuerzo medio
8. **Reescribir los 8 posts de blog** para incluir datos concretos (precio, distancia, duración) en cada sección, alineados con las cifras de `faq.html`, evitando contradicciones cruzadas. *(Esfuerzo: medio-alto — reescritura editorial.)*
9. **Añadir mini-FAQ con `FAQPage` JSON-LD específico** a cada página de tour (3-5 preguntas por tour). *(Esfuerzo: medio — redacción + schema repetido 26 veces.)*
10. **Añadir JSON-LD `Article`/`BlogPosting`** con `datePublished`/`dateModified` a los 8 posts de blog. *(Esfuerzo: bajo-medio.)*
11. **Envolver testimonios existentes en JSON-LD `Review`** anidado en `LocalBusiness`. *(Esfuerzo: bajo-medio, depende de la auditoría de schema general que ya está en curso por otro agente.)*
12. **Crear tabla comparativa de tours** (precio/duración/dificultad/perfil) en `experiencias.html` o página dedicada. *(Esfuerzo: medio.)*
13. **Convertir listas con `<br>` a `<ul><li>` reales** en `faq.html` y blog. *(Esfuerzo: bajo.)*

### Prioridad 3 — Impacto medio, esfuerzo medio-alto (construcción de autoridad externa, mediano plazo)
14. **Crear y activar canal de YouTube** con videos cortos de los tours (mayor señal de correlación con citación en IA, ~0.737). *(Esfuerzo: alto — producción de contenido.)*
15. **Reclamar/optimizar Google Business Profile** y enlazar la dirección del footer a un perfil de Google Maps verificable. *(Esfuerzo: bajo-medio.)*
16. **Solicitar reseñas en TripAdvisor/Google** de clientes reales (São Paulo, Lisboa, Buenos Aires ya mencionados como testimonios — convertirlos en reseñas verificables en plataformas externas). *(Esfuerzo: medio — proceso operativo continuo.)*
17. **Migrar el e-mail de contacto** de Gmail genérico a un dominio propio (`@natalexperience.com.br`) una vez resuelto el dominio. *(Esfuerzo: bajo.)*
18. **Añadir autoría nombrada (`Person` schema)** a los posts de blog, vinculando a Junior o a redactores identificados, con enlace a perfil profesional verificable (LinkedIn). *(Esfuerzo: bajo-medio.)*

### Prioridad 4 — Impacto bajo-medio, esfuerzo variable (mantenimiento continuo)
19. Monitorear menciones de marca en Reddit (foros de viajeros a Brasil/Nordeste) y participar de forma orgánica donde sea relevante.
20. Revisar y actualizar `llms.txt` y precios cada vez que cambien tarifas o se agreguen tours nuevos.
21. Considerar incorporar RSL 1.0 (licensing) si el cliente desea condicionar el uso de su contenido por crawlers de entrenamiento en el futuro — actualmente no es prioritario dado que el objetivo es maximizar visibilidad, no restringir uso.

---

## Archivos de referencia citados en este informe

- `E:\ANTIGRAVITY\NATALEXPERIENCE\robots.txt` (estado actual)
- `E:\ANTIGRAVITY\NATALEXPERIENCE\sitemap.xml` (42 URLs, dominio roto)
- `E:\ANTIGRAVITY\NATALEXPERIENCE\faq.html` (FAQPage JSON-LD, líneas 12-75)
- `E:\ANTIGRAVITY\NATALEXPERIENCE\index.html` (contradicción "30 anos", líneas 7 y 74)
- `E:\ANTIGRAVITY\NATALEXPERIENCE\quem-somos.html` (contradicción "30 anos", líneas 7, 25, 40)
- `E:\ANTIGRAVITY\NATALEXPERIENCE\blog\buggy-vale-a-pena.html`
- `E:\ANTIGRAVITY\NATALEXPERIENCE\blog\norte-ou-sul.html`
- `E:\ANTIGRAVITY\NATALEXPERIENCE\blog\guia-natal.html`
- `E:\ANTIGRAVITY\NATALEXPERIENCE\blog\roteiro-5-dias-natal.html`
- `E:\ANTIGRAVITY\NATALEXPERIENCE\passeios\buggy-litoral-norte.html`
- `E:\ANTIGRAVITY\NATALEXPERIENCE\experiencias-exclusivas\voo-helicoptero.html`
- Footer compartido con "Há mais de 18 anos" — confirmado presente de forma idéntica en 42/42 páginas HTML del proyecto.
