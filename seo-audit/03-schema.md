# Auditoría de Datos Estructurados (Schema.org / JSON-LD)
## NatalExperience Tours — natalexperience.com.br

**Fecha de auditoría:** 2026-06-26
**Alcance:** 42 archivos `.html` (raíz + `/passeios/` [16] + `/experiencias-exclusivas/` [10] + `/blog/` [8])
**Método:** Lectura directa de código fuente estático + `grep -r "application/ld+json"` y `grep -r "schema.org"` sobre el proyecto completo.

---

## 1. DETECCIÓN — Resultado del Grep global

```
grep -rl "application/ld+json" --include="*.html" .   →  1 resultado: ./faq.html
grep -rl "schema.org" --include="*.html" .             →  1 resultado: ./faq.html
```

**Confirmado: de 42 páginas HTML, solo 1 (`faq.html`) contiene structured data.** Las 41 páginas restantes —incluyendo `index.html`, las 16 fichas de `/passeios/`, las 10 de `/experiencias-exclusivas/`, las 8 del `/blog/`, `quem-somos.html`, `contato.html`, `experiencias.html`, `politica-cookies.html` y `politica-privacidade.html`— tienen **cero bloques JSON-LD, cero Microdata y cero RDFa**.

Esto significa que actualmente el sitio:
- No es elegible para ningún Rich Result de Google (ni siquiera el FAQ existente cumple del todo, ver §2).
- No tiene ninguna señal explícita de entidad (`Organization`/`LocalBusiness`) para el Knowledge Panel ni para Google Business Profile linking.
- No expone breadcrumbs estructurados a pesar de que el HTML visual SÍ tiene una jerarquía de breadcrumbs (`<div class="breadcrumbs">`) en todas las fichas de `/passeios/` y `/experiencias-exclusivas/` — es decir, existe la jerarquía visual pero no la versión machine-readable.
- No tiene marcado de Producto/Servicio en ninguna de las 16 fichas de tours ni en las 10 fichas VIP, a pesar de tener precio, duración e inclusiones claramente estructuradas en el HTML.
- No tiene marcado `Article`/`BlogPosting` en ninguno de los 8 posts del blog, a pesar de tener fecha de publicación visible (`<span>📅 25 de Abril, 2026</span>`), categoría y tiempo de lectura.
- No tiene `Review`/`AggregateRating` a pesar de mostrar 3 testimonios con nombre, origen y 5 estrellas en `index.html`.

### 1.1 Hallazgo parcial en `faq.html`

`faq.html` SÍ contiene un bloque `FAQPage` JSON-LD (líneas 12-75), pero con dos problemas de validación serios:

1. **Cobertura incompleta**: el HTML visible tiene **14 preguntas** (`grep -c "faq-item__question" faq.html` → 14, repartidas en 2 categorías: "📍 Planejando sua Viagem a Natal" con 7 preguntas y "💳 Reservas, Pagamentos e Serviços" con 7 preguntas). El JSON-LD solo incluye `mainEntity` para **7 preguntas** — exactamente la primera categoría. Las 7 preguntas de la segunda categoría (seguro incluido, cómo reservar, cancelamento, idiomas, qué incluye el precio, formas de pago, qué pasa si llueve) están ausentes del schema.
2. **Discrepancia textual**: el texto de las respuestas en el JSON-LD no es idéntico palabra por palabra al texto visible en el HTML (p. ej. la respuesta sobre buggy en Genipabu dice "comportam até 4 passageiros" + "valores variam... a partir de R$ 600" en el JSON-LD, mientras el HTML visible dice "Os valores médios variam de R$ 600 a R$ 800... mais taxas ambientais de cerca de R$ 15 a R$ 20"). Google exige que el contenido del schema sea **visible y coincidente** con el contenido de la página; un desajuste de este tipo puede invalidar el rich result o ser tratado como structured data engañoso.

**Nota de prioridad (regla crítica del playbook):** Google restringió los rich results de `FAQPage` a sitios gubernamentales y de salud desde agosto de 2023. Como NatalExperience Tours es un sitio comercial (agencia de turismo), el `FAQPage` existente **no generará rich result en Google** aunque se corrija. Se marca como **prioridad Info**, no Crítica — el valor real de corregirlo es la **citabilidad en motores de IA generativa** (Google AI Overviews, ChatGPT, Perplexity), que sí utilizan FAQPage como señal de extracción de pares pregunta-respuesta verificados.

---

## 2. Tabla resumen de hallazgos

| Página / sección | Schema presente | Schema correcto | Schema faltante recomendado |
|---|---|---|---|
| `index.html` | Ninguno | — | `Organization`/`TravelAgency`, `WebSite`, `AggregateRating`+`Review` |
| `faq.html` | `FAQPage` (parcial, 7/14) | Parcial — falta cobertura y hay discrepancia texto/schema | Completar `mainEntity` a 14 preguntas; sincronizar texto exacto |
| `/passeios/*.html` (16 páginas) | Ninguno | — | `Product`+`Offer` (o `Service`), `BreadcrumbList` |
| `/experiencias-exclusivas/*.html` (10 páginas) | Ninguno | — | `Product`+`Offer` (precio "Sob Consulta" → usar `priceSpecification` abierto), `BreadcrumbList` |
| `/blog/*.html` (8 páginas) | Ninguno | — | `BlogPosting`, `BreadcrumbList` |
| `quem-somos.html` | Ninguno | — | `AboutPage` (opcional), reutilizar `Organization` |
| `experiencias.html` | Ninguno | — | `CollectionPage`/`ItemList` (opcional), `BreadcrumbList` |
| `contato.html` | Ninguno | — | `ContactPage` (opcional), reutilizar `LocalBusiness` |

---

## 3. FAQPage — JSON-LD corregido y completo (14 preguntas)

**Advertencia de implementación:** el bloque siguiente reemplaza por completo el `<script type="application/ld+json">` actual en `faq.html` (líneas 12-75). El texto de cada `acceptedAnswer.text` se ha igualado al texto **visible** en el HTML de la página (sin etiquetas HTML, tal como exige Google), para eliminar la discrepancia detectada. Recordatorio de política: aunque agregamos las 14 preguntas para fines de citabilidad por LLM, **no se debe esperar rich result en Google** por tratarse de un sitio comercial (restricción de agosto 2023). Prioridad: **Info**, no Crítica.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Qual é a melhor época do ano para visitar Natal RN e fazer os passeios?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Natal possui sol brilhando em média 300 dias por ano. A melhor época para visitar e fazer passeios é entre setembro e março. Durante esses meses, o vento diminui, as lagoas da região de Nísia Floresta e Extremoz estão cheias e com tons verde-azulados, e os parrachos de Maracajaú e Perobas atingem seu nível máximo de visibilidade e transparência. O período chuvoso se concentra de abril a julho, mas as chuvas costumam ocorrer em pancadas rápidas que abrem espaço para o sol logo em seguida."
      }
    },
    {
      "@type": "Question",
      "name": "Como funciona e quanto custa o passeio de buggy em Genipabu (Litoral Norte)?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O tradicional passeio de buggy pelo Litoral Norte de Natal passa pelas dunas móveis de Genipabu, balsa do Rio Ceará-Mirim, Lagoa de Pitangui e Lagoa de Jacumã. O passeio é totalmente privativo e os buggys credenciados pela SETUR/RN comportam até 4 passageiros. O motorista perguntará antes de iniciar se você prefere o roteiro \"com ou sem emoção\" (subindo e descendo as dunas mais íngremes). Os valores médios variam de R$ 600 a R$ 800 por buggy (valor total dividido entre os passageiros), mais taxas ambientais de cerca de R$ 15 a R$ 20 por pessoa."
      }
    },
    {
      "@type": "Question",
      "name": "Qual a distância e qual a melhor forma de ir de Natal para a Praia de Pipa?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A charmosa Praia de Pipa fica localizada no município de Tibau do Sul, a aproximadamente 85 km ao sul de Ponta Negra, em Natal. De carro ou transfer receptivo, o tempo médio de viagem é de 1 hora e 20 minutos utilizando a rodovia BR-101. A melhor forma de conhecer o local é por meio de passeios de um dia (bate e volta) organizados ou transfers privativos, que garantem paradas estratégicas no mirante das falésias da Praia do Amor, Baía dos Golfinhos e tempo livre para desfrutar da badalada Vila de Pipa com total segurança."
      }
    },
    {
      "@type": "Question",
      "name": "Vale mais a pena fazer o mergulho em Maracajaú ou em Perobas?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ambos os destinos são incríveis, mas atendem a perfis diferentes: Maracajaú (60 km ao norte) é conhecido como o \"Caribe do RN\" e possui parrachos de recifes de corais mais profundos (2 a 3 metros), excelente para quem deseja mergulhar com snorkel ou cilindro e ver corais imponentes com rica fauna marinha. Perobas (75 km ao norte) possui piscinas naturais mais rasas (0,5m a 1m de profundidade) e com fundo de areia limpa, ideal para famílias com crianças, idosos, pessoas que não sabem nadar e para tirar fotos com água cristalina na altura da cintura. Importante: ambos os passeios dependem diretamente da maré baixa (ideal abaixo de 0.5 metros). Consulte nossa equipe para verificar a tabela de marés da sua data."
      }
    },
    {
      "@type": "Question",
      "name": "Qual a distância do Aeroporto de Natal (NAT) até Ponta Negra e como ir?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O Aeroporto Internacional Aluízio Alves (NAT) fica em São Gonçalo do Amarante, a cerca de 40 km da Praia de Ponta Negra (principal polo hoteleiro). O trajeto dura entre 45 e 50 minutos de carro. A forma mais segura, cômoda e eficiente de realizar esse trajeto é contratando um serviço de transfer receptivo credenciado com antecedência. Isso evita filas, golpes de transportes clandestinos e garante veículos modernos com ar-condicionado e motorista aguardando no desembarque."
      }
    },
    {
      "@type": "Question",
      "name": "O que fazer em Natal em um roteiro de 3 a 5 dias?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Roteiro de 3 dias: Dia 1: Ambientação na Praia de Ponta Negra e fotos no Morro do Careca. Dia 2: Passeio de Buggy no Litoral Norte (Dunas de Genipabu e Lagoas). Dia 3: Passeio bate e volta para a Praia de Pipa. Roteiro de 5 dias: Adicione o Dia 4 para Mergulho nos Parrachos de Maracajaú ou Perobas, e o Dia 5 para um City Tour histórico no Forte dos Reis Magos integrado a uma visita ao Maior Cajueiro do Mundo na praia de Pirangi."
      }
    },
    {
      "@type": "Question",
      "name": "Os passeios de buggy em Natal são seguros para crianças e idosos?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim, os passeios são muito seguros, desde que feitos com profissionais credenciados pela SETUR/RN (Secretaria de Turismo). Para grávidas, idosos ou famílias com crianças de colo, a regra básica é solicitar o passeio \"sem emoção\". Nessa modalidade, o bugueiro trafega em velocidade reduzida e evita manobras radicais nas dunas móveis, garantindo um passeio tranquilo e contemplativo. Nossos veículos contam com arcos de proteção metálica adicionais homologados."
      }
    },
    {
      "@type": "Question",
      "name": "Os passeios incluem seguro para os participantes?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim! Todos os nossos passeios incluem seguro de acidentes pessoais para todos os participantes. Trabalhamos com veículos revisados, equipamentos de segurança certificados e guias treinados em primeiros socorros. A sua segurança e a da sua família é a nossa prioridade número um."
      }
    },
    {
      "@type": "Question",
      "name": "Como faço para reservar um passeio?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O processo é simples e rápido! Basta nos contatar pelo WhatsApp clicando em qualquer botão \"Reservar\" no site. Nossa equipe irá tirar todas as suas dúvidas, verificar a disponibilidade na sua data desejada e confirmar a reserva. Aceitamos pagamento via PIX, cartão de crédito e dinheiro."
      }
    },
    {
      "@type": "Question",
      "name": "Posso cancelar ou reagendar minha reserva?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim. Cancelamentos e reagendamentos podem ser feitos com até 24 horas de antecedência sem custo adicional. Para cancelamentos em prazo menor, consulte nossa equipe — sempre fazemos o possível para encontrar a melhor solução para o cliente."
      }
    },
    {
      "@type": "Question",
      "name": "Vocês oferecem atendimento em outros idiomas?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim! Contamos com profissionais bilíngues na equipe. Oferecemos atendimento em português, espanhol e inglês. Se precisar de guia ou atendimento em outro idioma específico, informe-nos no momento da reserva."
      }
    },
    {
      "@type": "Question",
      "name": "O que está incluído no preço dos passeios?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Cada passeio tem suas inclusões específicas detalhadas. De modo geral, todos incluem o transporte de ida e volta a partir dos hotéis de Ponta Negra, Via Costeira e praias centrais de Natal, guia credenciado e seguro de viagem. Taxas locais (balsas, entradas e alimentação) são especificadas em cada roteiro ou informadas no atendimento pelo WhatsApp."
      }
    },
    {
      "@type": "Question",
      "name": "Como funciona o pagamento?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Aceitamos PIX, cartão de crédito, transferência bancária e pagamento em espécie. A forma de pagamento e os detalhes de parcelamento são combinados diretamente com a nossa equipe no ato da reserva pelo WhatsApp, garantindo facilidade e clareza."
      }
    },
    {
      "@type": "Question",
      "name": "E se chover no dia do meu passeio?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Caso as condições climáticas impossibilitem a realização do passeio com segurança (como ventos extremos ou tempestades), o passeio será reagendado sem custo ou haverá reembolso integral. Para chuvas leves e passageiras comuns da nossa região tropical, os passeios costumam ocorrer normalmente. Nossa equipe monitora a previsão do tempo constantemente."
      }
    }
  ]
}
```

---

## 4. Schema para fichas de Tours (`/passeios/` y `/experiencias-exclusivas/`)

### 4.1 Justificación del tipo elegido

Se evaluaron 4 candidatos para las fichas individuales de tours:

| Tipo | Veredicto | Razón |
|---|---|---|
| **HowTo** | ❌ Descartado | Rich results retirados por Google en septiembre 2023 (regla crítica del playbook). No usar bajo ninguna circunstancia. |
| **Event** | ❌ No aplica | `Event` exige una fecha/hora de inicio concreta (`startDate`) por instancia. Los tours de NatalExperience son ofertas recurrentes y continuas ("saídas diárias sob consulta da maré", "08:00–09:00"), no eventos puntuales con fecha fija. Forzar `Event` generaría errores de validación en Search Console (fechas faltantes o repetidas indebidamente) y es semánticamente incorrecto. |
| **TouristAttraction** | ⚠️ Parcial, no recomendado como tipo principal | `TouristAttraction` describe el **lugar/destino** (p. ej. "Praia de Pipa", "Dunas de Genipabu" como entidad geográfica), no el **servicio comercial vendible** que ofrece la agencia para visitarlo. No tiene rich result propio en Google y no admite `Offer`/precio de forma nativa. Es más adecuado para una eventual página informativa sobre el destino en sí (no existe en este sitio), no para la ficha de venta del passeio. |
| **TouristTrip** | ⚠️ Tipo semánticamente correcto, sin Rich Result en Google | `TouristTrip` es el tipo más preciso de schema.org para describir un itinerario turístico vendible (tiene `itinerary`, `touristType`, `provider`). Sin embargo, **Google no documenta ningún Rich Result para `TouristTrip`** en Search Central — no aparece en la lista de tipos soportados. |
| **Product + Offer** | ✅ **Recomendado como tipo principal** | Es el único de los candidatos con **Rich Result documentado y soportado por Google** (snippet de producto: precio, disponibilidad, rango de precios). Cada "passeio" se vende como un producto/servicio con un precio fijo o "a partir de", exactamente el patrón que Google espera en `Product`/`Offer`. Search Central permite usar `Product` para servicios reservables como tours. |

**Decisión final:** se usa `Product` como `@type` principal (para activar el Rich Result de Google) y se añade `"additionalType": "https://schema.org/TouristTrip"` para reforzar la semántica exacta ante motores de IA generativa (Google AI Overviews, ChatGPT, Perplexity), que sí entienden tipos compuestos y usan esa información adicional para clasificar mejor la entidad sin que esto rompa la validación de Google para `Product`. Esta combinación maximiza tanto el Rich Result clásico como la citabilidad GEO (Generative Engine Optimization).

Para las fichas de `/experiencias-exclusivas/` con precio "Sob Consulta" (sin valor fijo, ej. helicóptero, transfer VIP), se usa el mismo patrón `Product`+`Offer`, pero con `priceSpecification` o, donde no hay ningún precio ni siquiera orientativo, se omite el bloque de precio y se indica explícitamente como **dato faltante** (ver notas en cada bloque). **No se debe inventar un precio** — Google penaliza structured data con datos ficticios o no verificables en la página.

### 4.2 JSON-LD — `passeios/maracajau.html` (Mergulho em Maracajaú, Lancha Rápida)

Datos extraídos directamente del HTML: precio adulto R$ 280, precio criança R$ 200, duración ~8 horas, incluye transporte+equipo+guía+taxa ambiental, imágenes reales del bento-gallery.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "additionalType": "https://schema.org/TouristTrip",
  "name": "Mergulho em Maracajaú (Lancha Rápida)",
  "description": "Explore o Caribe Brasileiro em Maracajaú com a rapidez e emoção da Lancha Rápida. Mergulhe em águas cristalinas nos parrachos a 7km da costa, com snorkel entre corais e rica vida marinha. Passeio de aproximadamente 8 horas com saída de Ponta Negra, Via Costeira e Praia do Meio.",
  "image": [
    "https://www.natalexperience.com.br/img/maracajau_lancha_new_1.jpg",
    "https://www.natalexperience.com.br/img/maracajau_lancha_new_2.jpg",
    "https://www.natalexperience.com.br/img/maracajau_lancha_new_3.jpg",
    "https://www.natalexperience.com.br/img/maracajau_lancha_l3_centered.jpg"
  ],
  "brand": {
    "@type": "Organization",
    "name": "NatalExperience Tours"
  },
  "url": "https://www.natalexperience.com.br/passeios/maracajau.html",
  "offers": {
    "@type": "Offer",
    "url": "https://www.natalexperience.com.br/passeios/maracajau.html",
    "priceCurrency": "BRL",
    "price": "280.00",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "NatalExperience Tours"
    }
  }
}
```

**Notas de validación:**
- `priceValidUntil` se fijó como dato razonable de fin de año fiscal; el cliente debe confirmar o actualizar esta fecha periódicamente (Google la exige en `Offer` para evitar precios obsoletos).
- El precio "criança R$ 200" y la opción "Lancha VIP — Consulte valores" no se incluyeron como `Offer` adicional en este bloque base por simplicidad; si se desea representarlos, se puede usar un array en `offers` con un segundo objeto `Offer` (ver ficha siguiente con `AggregateOffer` como alternativa si el cliente lo solicita).

### 4.3 JSON-LD — `passeios/buggy-litoral-norte.html` (Litoral Norte Completo)

Datos extraídos: precio R$ 780 (valor por buggy, no por persona — importante para el `Offer`), duración ~7 horas, salida 08:00-09:00 desde el hotel.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "additionalType": "https://schema.org/TouristTrip",
  "name": "Litoral Norte Completo (Passeio de Buggy)",
  "description": "Passeio de buggy pelo litoral norte de Natal: dunas de Genipabu, Lagoa de Pitangui, Lagoa de Jacumã e Praia de Muriú. Buggy exclusivo com motorista/guia credenciado, transporte ida e volta do hotel em Natal e seguro de passageiro incluídos. Duração aproximada de 7 horas.",
  "image": [
    "https://www.natalexperience.com.br/img/buggy-norte-2.jpg",
    "https://www.natalexperience.com.br/img/buggy-norte-3.jpg",
    "https://www.natalexperience.com.br/img/buggy-norte-ponte-newcomer.jpg",
    "https://www.natalexperience.com.br/img/buggy-norte-4.jpg",
    "https://www.natalexperience.com.br/img/buggy-norte-grupo-t1.jpg"
  ],
  "brand": {
    "@type": "Organization",
    "name": "NatalExperience Tours"
  },
  "url": "https://www.natalexperience.com.br/passeios/buggy-litoral-norte.html",
  "offers": {
    "@type": "Offer",
    "url": "https://www.natalexperience.com.br/passeios/buggy-litoral-norte.html",
    "priceCurrency": "BRL",
    "price": "780.00",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "description": "Preço total por buggy (até 4 passageiros), não incluindo taxa de balsa/ambiental (aprox. R$ 120 por buggy).",
    "seller": {
      "@type": "Organization",
      "name": "NatalExperience Tours"
    }
  }
}
```

**Nota de validación:** se añadió `offers.description` para aclarar que el precio es "por buggy" y no "por persona" — esto es crítico porque Google puede mostrar el precio en el snippet y un usuario podría interpretarlo erróneamente como precio por persona si no se aclara. Es un patrón de buena práctica, no un campo inventado.

### 4.4 JSON-LD — `experiencias-exclusivas/voo-helicoptero.html` (Voo Panorâmico de Helicóptero)

Este caso **no tiene precio fijo** en el HTML ("Sob Consulta / Voo — Preço a partir de. Consulte valores para grupos."). No se debe inventar un número.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "additionalType": "https://schema.org/TouristTrip",
  "name": "Voo Panorâmico de Helicóptero",
  "description": "Veja Natal de uma perspectiva única e inesquecível. Sobrevoo das dunas, do litoral e dos principais pontos turísticos da cidade com piloto executivo experiente. Voo exclusivo para até 4 ou 6 passageiros, com duração de 15 a 30 minutos.",
  "image": [
    "https://www.natalexperience.com.br/img/helicoptero_card.png",
    "https://www.natalexperience.com.br/img/helicoptero_gallery_1.jpg",
    "https://www.natalexperience.com.br/img/helicoptero_gallery_2.jpg",
    "https://www.natalexperience.com.br/img/helicoptero_gallery_3.jpg",
    "https://www.natalexperience.com.br/img/helicoptero_gallery_4.jpg"
  ],
  "brand": {
    "@type": "Organization",
    "name": "NatalExperience Tours"
  },
  "url": "https://www.natalexperience.com.br/experiencias-exclusivas/voo-helicoptero.html",
  "offers": {
    "@type": "Offer",
    "url": "https://www.natalexperience.com.br/experiencias-exclusivas/voo-helicoptero.html",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "businessFunction": "https://schema.org/Sell",
    "description": "Valor sob consulta, calculado conforme número de passageiros e disponibilidade. Solicitar orçamento pelo WhatsApp."
  }
}
```

**DATO FALTANTE A COMPLETAR POR EL CLIENTE:** no existe ningún precio mínimo u orientativo en el HTML para esta experiencia. Google exige `price` o `priceSpecification` en `Offer` para que el Rich Result de producto se muestre con precio; sin él, el bloque es válido pero no mostrará precio en el snippet. **Recomendación:** si la agencia tiene un precio "a partir de" real (aunque sea estimado, ej. "a partir de R$ 1.500/voo"), debe agregarse como texto visible en la página y reflejarse aquí en `price` + `priceSpecification` tipo `UnitPriceSpecification` con nota "a partir de".

### 4.5 JSON-LD — `experiencias-exclusivas/transfer-vip.html` (Transfer VIP)

Mismo caso: precio "Sob Consulta", sin valor numérico en el HTML. Aquí se modela mejor como `Service` que como `Product`, porque no hay ninguna unidad de venta fija (varía 100% por origen/destino/pasajeros) y es un servicio de transporte, no una experiencia/producto empaquetado con precio de catálogo.

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Transfer privativo / transporte executivo",
  "name": "Transfer VIP NatalExperience Tours",
  "description": "Deslocamentos privativos com máximo conforto entre o Aeroporto de Natal (NAT), hotéis, Praia da Pipa (~85km) e São Miguel do Gostoso (~110km), além de João Pessoa, Recife e Fortaleza sob consulta. Veículos premium com ar-condicionado, água mineral e Wi-Fi cortesia.",
  "provider": {
    "@type": "Organization",
    "name": "NatalExperience Tours",
    "url": "https://www.natalexperience.com.br/"
  },
  "areaServed": {
    "@type": "City",
    "name": "Natal",
    "containedInPlace": {
      "@type": "State",
      "name": "Rio Grande do Norte"
    }
  },
  "url": "https://www.natalexperience.com.br/experiencias-exclusivas/transfer-vip.html",
  "image": "https://www.natalexperience.com.br/img/transfer-vip-real.png",
  "offers": {
    "@type": "Offer",
    "priceCurrency": "BRL",
    "description": "Valor varia de acordo com o destino e número de passageiros. Solicitar orçamento pelo WhatsApp."
  }
}
```

**DATO FALTANTE A COMPLETAR POR EL CLIENTE:** igual que el caso anterior, no hay precio base. `Service` no requiere `price` obligatoriamente, pero si el cliente desea Rich Result de producto con precio visible, debería publicar al menos un precio de referencia por trayecto más solicitado (ej. "Aeroporto → Ponta Negra a partir de R$ X").

### 4.6 Plantilla genérica reutilizable (para las 12 fichas de `/passeios/` y 7 de `/experiencias-exclusivas/` restantes)

Para aplicar el mismo patrón a todas las demás fichas, reemplazar los placeholders entre `{{ }}` por los datos reales de cada página (NO dejar ningún placeholder sin completar — el playbook prohíbe explícitamente texto de relleno en el JSON-LD final):

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "additionalType": "https://schema.org/TouristTrip",
  "name": "{{Título exacto del <h1> de la ficha}}",
  "description": "{{Párrafo descriptivo real de 'Sobre o Passeio' / 'Sobre a Experiência'}}",
  "image": ["{{URL absoluta imagen 1}}", "{{URL absoluta imagen 2}}", "{{URL absoluta imagen 3}}"],
  "brand": { "@type": "Organization", "name": "NatalExperience Tours" },
  "url": "{{URL canónica de la página, según <link rel='canonical'>}}",
  "offers": {
    "@type": "Offer",
    "url": "{{misma URL canónica}}",
    "priceCurrency": "BRL",
    "price": "{{valor numérico sin 'R$' ni 'a partir de', solo el número}}",
    "priceValidUntil": "2026-12-31",
    "availability": "https://schema.org/InStock",
    "seller": { "@type": "Organization", "name": "NatalExperience Tours" }
  }
}
```

Lista de páginas pendientes de aplicar esta plantilla (con su precio real ya detectado en el código fuente, para referencia rápida del implementador):

**`/passeios/`:**
- `buggy-litoral-alternativo.html` — R$ 400/Buggy, ~2h
- `buggy-litoral-intermedio.html` — R$ 500/Buggy, ~3h
- `buggy-litoral-sul-pipa.html` — R$ 800/Buggy, ~7h
- `city-tour-buggy.html` — precio no confirmado en esta auditoría, leer ficha
- `galinhos.html` — R$ 175/pessoa (con barco)
- `litoral-sul-4x4.html` — R$ 170/pessoa
- `litoral-sul-aguas.html` — R$ 760/Buggy
- `litoral-sul-vip-4x4.html` — precio no confirmado, leer ficha
- `maracajau-buggy-mergulho.html` — R$ 980/Buggy, ~8h
- `maracajau-catamara.html` — R$ 170/pessoa, ~7h
- `perobas.html` — R$ 185 aprox., ~8h
- `pipa.html` — R$ 75/pessoa, dia inteiro
- `por-do-sol-potengi.html` — precio no confirmado, leer ficha
- `sao-miguel-do-gostoso.html` — R$ 125 aprox.

**`/experiencias-exclusivas/`:** la mayoría usa "Sob Consulta" (sin precio fijo) — aplicar el patrón `Service` de §4.5 en vez de `Product`, salvo que el cliente confirme precios de referencia: `buggy-vip.html`, `mergulho-maracajau.html`, `passeio-aviao.html`, `rota-natal-fortaleza.html`, `rota-norte-helicoptero.html`, `rota-secreta-praias.html`, `vip-sao-miguel.html`, `veleiro-noronha.html`.

---

## 5. LocalBusiness / TravelAgency — Schema de Organización (para Home/Footer global)

### 5.1 Justificación

Schema.org tiene el tipo específico `TravelAgency` (subtipo de `LocalBusiness`), que es el más preciso para NatalExperience Tours. Se recomienda inyectar este bloque en `index.html` (idealmente también repetido o referenciado en el footer/`<head>` de todas las páginas vía `@id` para consistencia, pero como mínimo en la home).

### 5.2 Datos confirmados en el sitio (NO inventados)
- Nombre: NatalExperience Tours
- Dirección: Rua Túlio Fernandes, 415 - Praia do Meio, Natal - RN, 59010-038, Brasil
- Teléfono: +55 84 99986-8411 (confirmado también en `tel:+5584999868411`)
- Email: natalexperiencetours@gmail.com
- URL: https://www.natalexperience.com.br/ (según `<link rel="canonical">` de `index.html`)
- Logo: img/logo-minimal.png

### 5.3 ⚠️ Inconsistencia de contenido detectada (antes de implementar `foundingDate` o antigüedad)

Se encontró una **contradicción factual entre páginas** que debe resolverse ANTES de publicar cualquier schema con antigüedad de la empresa:

- El **footer de TODAS las páginas** (index, faq, passeios, experiencias-exclusivas, quem-somos, etc.) dice: *"Há mais de **18 anos** criando experiências inesquecíveis em Natal..."*
- La página `quem-somos.html` dice: *"Com mais de **30 anos de experiência**"* (sobre el fundador Junior) y el contador animado de estadísticas (`data-counter="30"`) en home y quem-somos también marca **30**.
- La meta description de `index.html` y `quem-somos.html` también dice **"Mais de 30 anos de experiência"**.

Esto es una discrepancia de negocio (18 vs 30 años) que no es un problema de schema, sino de contenido fuente. **No se debe publicar un `foundingDate` calculado a partir de ninguno de los dos números hasta que el cliente confirme cuál es correcto** — de lo contrario se introduce un structured data potencialmente falso, lo cual viola las políticas de Google contra datos engañosos. Se señala como dato faltante/a resolver en el bloque siguiente.

### 5.4 JSON-LD — TravelAgency (listo para implementar, con datos reales únicamente)

```json
{
  "@context": "https://schema.org",
  "@type": "TravelAgency",
  "@id": "https://www.natalexperience.com.br/#organization",
  "name": "NatalExperience Tours",
  "image": "https://www.natalexperience.com.br/img/logo-minimal.png",
  "logo": "https://www.natalexperience.com.br/img/logo-minimal.png",
  "url": "https://www.natalexperience.com.br/",
  "telephone": "+55-84-99986-8411",
  "email": "natalexperiencetours@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua Túlio Fernandes, 415 - Praia do Meio",
    "addressLocality": "Natal",
    "addressRegion": "RN",
    "postalCode": "59010-038",
    "addressCountry": "BR"
  },
  "areaServed": {
    "@type": "State",
    "name": "Rio Grande do Norte"
  },
  "sameAs": []
}
```

**DATOS FALTANTES A COMPLETAR POR EL CLIENTE (no inventados, omitidos intencionalmente):**

1. **`geo` (latitude/longitude):** no se encontró ningún dato de geolocalización en el código fuente (ni mapa embebido de Google Maps con coordenadas, ni meta tags `geo.position`). Sin esto, el negocio no podrá aparecer correctamente vinculado en Google Maps / Local Pack. Recomendación: obtener lat/long exacta de la dirección vía Google Maps y añadir:
   ```json
   "geo": { "@type": "GeoCoordinates", "latitude": "REEMPLAZAR", "longitude": "REEMPLAZAR" }
   ```
2. **`openingHoursSpecification`:** no se encontró ningún horario de atención visible en ninguna página del sitio (ni en `contato.html`, ni en footer). Si la agencia atiende por WhatsApp en un horario determinado, debe añadirse, por ejemplo:
   ```json
   "openingHoursSpecification": {
     "@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
     "opens": "REEMPLAZAR (ej. 08:00)",
     "closes": "REEMPLAZAR (ej. 20:00)"
   }
   ```
3. **`sameAs` (redes sociales):** el footer de todas las páginas tiene iconos de Instagram, Facebook y YouTube, pero **los 3 enlaces apuntan a `href="#"`** (sin URL real). No se debe inventar una URL de perfil social. El cliente debe proporcionar las URLs reales de sus perfiles para poblar `sameAs`:
   ```json
   "sameAs": ["REEMPLAZAR URL Instagram", "REEMPLAZAR URL Facebook", "REEMPLAZAR URL YouTube"]
   ```
4. **`foundingDate` / antigüedad:** NO incluido en el bloque por la contradicción 18 vs 30 años detallada en §5.3. Resolver primero a nivel de contenido (decidir cuál cifra es la correcta y corregirla de forma consistente en footer, quem-somos.html, meta descriptions y contador de stats), luego añadir `foundingDate` con el año real de fundación.
5. **`priceRange`:** opcional pero recomendado para `TravelAgency`/`LocalBusiness` (ej. `"$$"` o rango en BRL); no hay datos suficientes en el sitio para inferirlo de forma fiable dado que va desde R$ 75 (Pipa/pessoa) hasta "Sob Consulta" (helicóptero/veleiro). Si el cliente confirma un rango, se puede agregar `"priceRange": "R$75 - R$1000+"` o similar.

### 5.5 JSON-LD — WebSite (complementario, recomendado junto al anterior en `index.html`)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://www.natalexperience.com.br/#website",
  "url": "https://www.natalexperience.com.br/",
  "name": "NatalExperience Tours",
  "publisher": { "@id": "https://www.natalexperience.com.br/#organization" },
  "inLanguage": "pt-BR"
}
```

---

## 6. BreadcrumbList — Jerarquía de navegación

### 6.1 Justificación

Todas las fichas de `/passeios/` y `/experiencias-exclusivas/` ya muestran visualmente una jerarquía de breadcrumbs en HTML (`<div class="breadcrumbs">Início › Experiências › Passeios Clássicos › {{Tour}}</div>`), pero no existe la versión `BreadcrumbList` machine-readable. Es uno de los Rich Results mejor soportados y de implementación más segura de Google (sin restricciones de industria, a diferencia de FAQ). Prioridad: **Alta**.

### 6.2 JSON-LD — Ejemplo real para `passeios/maracajau.html`

Basado en el breadcrumb visible real: `Início › Experiências › Passeios Clássicos › Maracajaú`

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Início",
      "item": "https://www.natalexperience.com.br/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Experiências",
      "item": "https://www.natalexperience.com.br/experiencias.html"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Passeios Clássicos",
      "item": "https://www.natalexperience.com.br/experiencias.html#classicos"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "Mergulho em Maracajaú (Lancha Rápida)"
    }
  ]
}
```

**Nota técnica:** el último `ListItem` (la página actual) no necesita `item` (URL) según la documentación de Google —es opcional para el último elemento— pero si se incluye debe ser la URL canónica de la propia página.

### 6.3 JSON-LD — Ejemplo real para `experiencias-exclusivas/voo-helicoptero.html`

Basado en el breadcrumb visible real: `Início › Experiências › Experiências Exclusivas › Voo Panorâmico de Helicóptero`

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Início",
      "item": "https://www.natalexperience.com.br/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Experiências",
      "item": "https://www.natalexperience.com.br/experiencias.html"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Experiências Exclusivas",
      "item": "https://www.natalexperience.com.br/experiencias.html#exclusivas"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "Voo Panorâmico de Helicóptero"
    }
  ]
}
```

**Aplicación:** este mismo patrón de 4 niveles (Início › Experiências › [Passeios Clássicos | Experiências Exclusivas] › Título) debe replicarse en las 16 + 10 = 26 fichas de tours, ajustando únicamente el nombre del último nivel y la URL del tercer nivel según corresponda (`#classicos` o `#exclusivas`).

---

## 7. Review / AggregateRating — Basado en testimonios visibles

### 7.1 ⚠️ ADVERTENCIA CRÍTICA DE CUMPLIMIENTO (leer antes de implementar)

`index.html` muestra 3 testimonios reales en la sección `#depoimentos`:

| Autor | Origen | Estrellas | Texto |
|---|---|---|---|
| Carolina Martins | São Paulo, SP | ★★★★★ (5) | "Uma experiência absolutamente incrível! O passeio de buggy foi emocionante e o Junior nos fez sentir em casa. Voltaremos com certeza!" |
| Ricardo & Ana Ferreira | Lisboa, Portugal | ★★★★★ (5) | "O voo de helicóptero foi de tirar o fôlego! A equipe toda muito profissional e atenciosa. Superou todas as expectativas." |
| Família González | Buenos Aires, Argentina | ★★★★★ (5) | "Contratamos o roteiro sob medida e foi perfeito. Cada detalhe pensado com carinho. Natal é mais lindo do que imaginávamos." |

**Antes de marcar estos testimonios con `Review`/`AggregateRating` en JSON-LD, el cliente DEBE confirmar:**

1. Que estos 3 testimonios son **reales y verificables** (clientes reales que efectivamente contrataron el servicio), no copys de marketing redactados internamente. Google Search Central prohíbe explícitamente el "schema markup engañoso", incluyendo reseñas inventadas o no verificables, y puede aplicar **acciones manuales** (penalización) si detecta `Review`/`AggregateRating` sin sustento real.
2. Idealmente, que existan estas reseñas también en una plataforma de terceros verificable (Google Business Profile, TripAdvisor, Facebook) para poder enlazarlas o, al menos, conservar evidencia (capturas, mensajes de WhatsApp del cliente, etc.) en caso de auditoría de Google.
3. Que el sitio realmente recopiló reseñas de **más de una persona** de forma agregada si se va a usar `AggregateRating` con `reviewCount` — actualmente solo hay 3 testimonios visibles, lo cual es una muestra pequeña pero válida si son reales.

**Si el cliente no puede confirmar la autenticidad/verificabilidad de estos 3 testimonios, NO se debe implementar el bloque de §7.2 — usar los testimonios solo como contenido visual de la página, sin marcado de `Review`/`AggregateRating`.** Esta es una decisión del cliente sobre datos de su propio negocio, no algo que se pueda inferir solo leyendo el HTML.

### 7.2 JSON-LD — Review + AggregateRating (implementar SOLO tras confirmar §7.1)

Este bloque se anidaría dentro del objeto `TravelAgency` de §5.4 (agregar las propiedades `aggregateRating` y `review` al mismo objeto), o publicarse como bloque independiente referenciando el mismo `@id`:

```json
{
  "@context": "https://schema.org",
  "@type": "TravelAgency",
  "@id": "https://www.natalexperience.com.br/#organization",
  "name": "NatalExperience Tours",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "3",
    "bestRating": "5",
    "worstRating": "1"
  },
  "review": [
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5"
      },
      "author": {
        "@type": "Person",
        "name": "Carolina Martins"
      },
      "reviewBody": "Uma experiência absolutamente incrível! O passeio de buggy foi emocionante e o Junior nos fez sentir em casa. Voltaremos com certeza!",
      "publisher": {
        "@type": "Organization",
        "name": "NatalExperience Tours"
      }
    },
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5"
      },
      "author": {
        "@type": "Person",
        "name": "Ricardo & Ana Ferreira"
      },
      "reviewBody": "O voo de helicóptero foi de tirar o fôlego! A equipe toda muito profissional e atenciosa. Superou todas as expectativas.",
      "publisher": {
        "@type": "Organization",
        "name": "NatalExperience Tours"
      }
    },
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5"
      },
      "author": {
        "@type": "Person",
        "name": "Família González"
      },
      "reviewBody": "Contratamos o roteiro sob medida e foi perfeito. Cada detalhe pensado com carinho. Natal é mais lindo do que imaginávamos.",
      "publisher": {
        "@type": "Organization",
        "name": "NatalExperience Tours"
      }
    }
  ]
}
```

**Nota adicional:** `reviewCount: 3` es matemáticamente honesto (solo hay 3 reseñas reales visibles en el sitio), pero un `AggregateRating` con muestra tan pequeña tiene bajo impacto/credibilidad ante Google y ante los propios usuarios. Se recomienda al cliente **ampliar activamente la recolección de reseñas reales** (Google Business Profile, encuestas post-servicio) antes de depender de este schema como palanca de Rich Result, ya que Google también puede no mostrar el rich snippet de estrellas si la cantidad de reseñas es muy baja o si no detecta la página de reseñas como "principalmente sobre reseñas" en ciertos contextos de `Product`.

---

## 8. BlogPosting — Recomendación adicional para `/blog/` (no solicitada explícitamente, pero detectada como oportunidad)

Aunque no fue pedido en el alcance original de breadcrumbs/FAQ/tours/LocalBusiness/Review, se detectó que las 8 páginas de `/blog/` tienen todos los datos necesarios para `BlogPosting` (fecha visible, categoría, tiempo de lectura, imagen de cabecera) y actualmente no tienen ningún schema. Se incluye como oportunidad adicional de alta relevancia para citabilidad en AI Overviews/Perplexity (que priorizan fuertemente contenido con `datePublished` explícito y autoría clara).

### Ejemplo real — `blog/guia-natal.html`

Datos extraídos: título, fecha "25 de Abril, 2026", categoría "Dicas de Viagem", imagen de cabecera `blog-guia-natal.jpg`.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "O que fazer em Natal RN: Guia completo para planejar sua viagem perfeita",
  "description": "Descubra o que fazer em Natal RN: praias, dunas de Genipabu, mergulho em Maracajaú e muito mais. O guia definitivo para sua viagem perfeita.",
  "image": "https://www.natalexperience.com.br/img/blog-guia-natal.jpg",
  "datePublished": "2026-04-25",
  "author": {
    "@type": "Organization",
    "name": "NatalExperience Tours"
  },
  "publisher": {
    "@type": "Organization",
    "name": "NatalExperience Tours",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.natalexperience.com.br/img/logo-minimal.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.natalexperience.com.br/blog/guia-natal.html"
  }
}
```

**DATO FALTANTE A COMPLETAR POR EL CLIENTE:** no hay autor individual identificado en ninguno de los posts (no se atribuye a una persona, solo a la marca) — se usó `Organization` como `author`, lo cual es válido pero menos óptimo para E-E-A-T que un autor humano nombrado con su propia bio. Si el cliente desea reforzar autoridad (especialmente para los artículos de "guia"/"roteiro"), considerar atribuir autoría a "Junior" (el fundador, ya presentado en `quem-somos.html`) usando `"@type": "Person", "name": "Junior", "url": ".../quem-somos.html"`. Tampoco existe `dateModified` visible en el HTML — si el cliente actualiza el artículo en el futuro, debe añadir esa fecha también.

**Recordatorio de regla crítica:** ninguno de los 8 artículos de blog revisados o mencionados en la estructura del sitio (`buggy-vale-a-pena.html`, `guia-natal.html`, `melhores-lagoas-natal.html`, `melhores-passeios.html`, `mergulho-natal.html`, `norte-ou-sul.html`, `pipa-bate-e-volta.html`, `roteiro-5-dias-natal.html`) debe usar `@type: "HowTo"` aunque su contenido sea tipo "roteiro paso a paso" o "guía" — confirmar que ninguno de los títulos induzca a implementarlo como HowTo en el futuro; usar siempre `BlogPosting` o `Article`.

---

## 9. Resumen de prioridades de implementación

| Prioridad | Acción | Impacto esperado |
|---|---|---|
| **Crítica** | Implementar `BreadcrumbList` en las 26 fichas de tours/experiencias (§6) | Rich Result de Google sin restricciones de industria; mejora CTR en SERP |
| **Crítica** | Implementar `Product`+`Offer` en las 26 fichas de tours/experiencias (§4) | Rich Result de producto (precio/disponibilidad) en Google; base estructural para GEO |
| **Crítica** | Implementar `TravelAgency` + `WebSite` en `index.html` (§5) | Entidad de negocio reconocible por Google y por LLMs; base para Knowledge Panel |
| **Alta** | Resolver inconsistencia 18 vs 30 años antes de publicar `foundingDate` (§5.3) | Evita publicar dato factualmente incierto en schema (riesgo de penalización por datos engañosos) |
| **Alta** | Obtener `geo`, `openingHoursSpecification` y `sameAs` reales del cliente (§5.4) | Completa el perfil de `LocalBusiness` para Maps/Local Pack |
| **Media (Info)** | Completar y corregir `FAQPage` en `faq.html` (§3) | Sin Rich Result en Google (restricción agosto 2023, sitio comercial); sí mejora citabilidad en AI Overviews/ChatGPT/Perplexity |
| **Media** | Confirmar autenticidad de testimonios antes de `Review`/`AggregateRating` (§7) | Riesgo de acción manual de Google si no son reales/verificables; alto valor si se confirman |
| **Baja (oportunidad adicional)** | `BlogPosting` en los 8 artículos del blog (§8) | Mejora citabilidad GEO; no es Rich Result clásico de alto impacto pero refuerza E-E-A-T |

---

## 10. Checklist de validación aplicado a cada bloque entregado

Todos los bloques JSON-LD de este informe fueron verificados contra el checklist del playbook:

1. ✅ `@context` es `"https://schema.org"` (HTTPS, no HTTP) en todos los bloques.
2. ✅ Ningún `@type` usado es deprecado (no se usó `HowTo`, `SpecialAnnouncement`, `CourseInfo`, `EstimatedSalary` ni `LearningVideo`).
3. ✅ `FAQPage` se mantiene pero marcado explícitamente como prioridad Info (no Crítica) por la restricción de Google a sitios gubernamentales/salud desde agosto 2023.
4. ✅ Todas las URLs son absolutas (`https://www.natalexperience.com.br/...`), nunca relativas.
5. ✅ Las fechas usadas (`priceValidUntil`, `datePublished`) están en formato ISO 8601 (`YYYY-MM-DD`).
6. ✅ No se incluyó ningún placeholder tipo `[Business Name]` en los bloques finales de implementación directa (§3, §4.2-4.5, §5.4-5.5, §6.2-6.3, §7.2, §8) — los placeholders `{{ }}` solo aparecen en la plantilla genérica de §4.6, identificada explícitamente como plantilla a completar, no como bloque final.
7. ✅ Todo dato no verificable en el código fuente (geo-coordenadas, horario de atención, redes sociales reales, antigüedad de la empresa, precios de experiencias "Sob Consulta") fue señalado explícitamente como **dato faltante a completar por el cliente**, sin inventar valores.
