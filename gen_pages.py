import os
import re
import random

classicos = [
    {
        "filename": "passeios/litoral-sul-4x4.html",
        "title": "4x4 Litoral Sul VIP",
        "price_string": '<p class="detail-sidebar__price">R$ 170 <span>/ pessoa</span></p>',
        "sticky_price": "R$ 170",
        "duration": "Dia inteiro",
        "description": "Explore as praias mais famosas do Litoral Sul com o conforto e a exclusividade de um veículo 4x4. Visite o Maior Cajueiro do Mundo, o Mirante dos Golfinhos e as piscinas naturais incríveis.",
        "whatsapp_name": "4x4 Litoral Sul VIP",
        "inclusions": ["Veículo 4x4 exclusivo com motorista credenciado", "Transporte ida e volta do seu hotel em Natal", "Seguro passageiro", "Roteiro personalizado pelo litoral sul"],
        "exclusions": ["Alimentação e bebidas", "Ingresso do Maior Cajueiro do Mundo", "Passeio de lancha/barco (opcional)"],
        "what_to_bring": ["Roupas leves e de banho", "Protetor solar e óculos de sol", "Toalha e dinheiro para extras"]
    },
    {
        "filename": "passeios/pipa.html",
        "title": "Passeio para Pipa",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 75 <span>/ pessoa</span></p>',
        "sticky_price": "A partir de R$ 75",
        "duration": "Dia inteiro",
        "description": "Pipa é um dos destinos mais cobiçados do Brasil, famosa por suas imensas falésias coloridas, mar de águas mornas e a charmosa vila repleta de lojas e gastronomia internacional.",
        "whatsapp_name": "Passeio para Pipa",
        "inclusions": ["Transporte rodoviário de ida e volta", "Guia de turismo credenciado", "Seguro passageiro", "Visita à Praia do Madeiro, Baía dos Golfinhos e Centro de Pipa"],
        "exclusions": ["Alimentação e bebidas", "Passeios de barco ou buggy locais (opcionais)", "Gastos pessoais na vila"],
        "what_to_bring": ["Roupas leves e de banho", "Protetor solar e óculos de sol", "Câmera fotográfica ou celular"]
    },
    {
        "filename": "passeios/perobas.html",
        "title": "Perobas (Parrachos do Rio do Fogo)",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 185 <span>/ pessoa</span></p>',
        "sticky_price": "A partir de R$ 185",
        "duration": "8 horas aprox",
        "description": "Mergulhe nas águas cristalinas dos Parrachos de Perobas. Um verdadeiro paraíso intacto, perfeito para snorkeling e contato direto com a vida marinha em piscinas naturais rasas e tranquilas.",
        "whatsapp_name": "Parrachos de Perobas",
        "inclusions": ["Transporte ida e volta do seu hotel", "Passeio de lancha até os parrachos", "Taxa de preservação ambiental", "Máscara e snorkel"],
        "exclusions": ["Alimentação e bebidas", "Fotos subaquáticas (opcional)", "Guarda-sol na praia base"],
        "what_to_bring": ["Roupas de banho", "Protetor solar biodegradável", "Dinheiro em espécie"]
    },
    {
        "filename": "passeios/buggy-litoral-sul-pipa.html",
        "title": "Buggy Litoral Sul (Pipa)",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 800 <span>/ Buggy (até 4 pax)</span></p>',
        "sticky_price": "A partir de R$ 800",
        "duration": "~7 horas",
        "description": "Aventure-se pelas praias do litoral sul de Natal em um passeio de buggy inesquecível até a famosa Vila de Pipa. Praias desertas, balsa e muita aventura.",
        "whatsapp_name": "Buggy Litoral Sul (Pipa)",
        "inclusions": ["Buggy exclusivo com motorista credenciado", "Transporte ida e volta do seu hotel em Natal", "Seguro passageiro", "Roteiro pelas praias do sul e Chapadão de Pipa"],
        "exclusions": ["Alimentação e bebidas", "Travessia de balsa (R$ 100/buggy ida e volta)", "Ingresso do Maior Cajueiro do Mundo"],
        "what_to_bring": ["Roupas leves e de banho", "Protetor solar e óculos de sol", "Toalha e dinheiro para taxas"]
    },
    {
        "filename": "passeios/maracajau.html",
        "title": "Maracajaú + Mergulho",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 295 <span>/ pessoa</span></p>',
        "sticky_price": "A partir de R$ 295",
        "duration": "Dia inteiro",
        "description": "Conhecida como o Caribe Brasileiro, Maracajaú oferece os maiores bancos de corais da região. O passeio inclui o mergulho (com cilindro ou snorkel) em meio aos recifes cheios de peixes coloridos.",
        "whatsapp_name": "Maracajaú com Mergulho",
        "inclusions": ["Transporte ida e volta do seu hotel", "Catamarã até os parrachos de Maracajaú", "Máscara e snorkel", "Suporte no ponto de apoio na praia"],
        "exclusions": ["Alimentação e bebidas", "Mergulho de cilindro (opcional)", "Taxa de preservação ambiental"],
        "what_to_bring": ["Roupas de banho", "Protetor solar", "Dinheiro em espécie ou cartão"]
    },
    {
        "filename": "passeios/galinhos.html",
        "title": "Galinhos (Com Barco)",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 175 <span>/ pessoa</span></p>',
        "sticky_price": "A partir de R$ 175",
        "duration": "Dia inteiro",
        "description": "Visite a península de Galinhos, um refúgio de paz acessível apenas por barco. Navegue pelos manguezais, veja as salinas e encante-se com este pedaço intocado do litoral norte.",
        "whatsapp_name": "Galinhos",
        "inclusions": ["Transporte rodoviário ida e volta", "Passeio de barco na travessia", "Guia turístico", "Seguro viagem"],
        "exclusions": ["Alimentação e bebidas", "Passeio de buggy nas dunas de Galinhos (opcional)", "Passeio de charrete"],
        "what_to_bring": ["Roupas de banho e chinelos", "Protetor solar", "Câmera fotográfica"]
    },

    {
        "filename": "passeios/sao-miguel-do-gostoso.html",
        "title": "São Miguel do Gostoso + Tourinhos",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 125 <span>/ pessoa</span></p>',
        "sticky_price": "A partir de R$ 125",
        "duration": "Dia inteiro",
        "description": "Conheça a vila pitoresca de São Miguel do Gostoso e a paradisíaca Praia de Tourinhos, famosa por suas formações rochosas (suspiros) e pelo pôr do sol inesquecível.",
        "whatsapp_name": "São Miguel do Gostoso",
        "inclusions": ["Transporte ida e volta do seu hotel", "Visita à Praia de Tourinhos", "Tempo livre na vila de São Miguel do Gostoso", "Guia especializado"],
        "exclusions": ["Alimentação e bebidas", "Passeios extras de jardineira ou buggy (opcionais)", "Serviços de praia"],
        "what_to_bring": ["Roupa de banho e roupas leves", "Protetor solar e óculos de sol", "Câmera fotográfica para o pôr do sol"]
    },
    {
        "filename": "passeios/por-do-sol-potengi.html",
        "title": "Pôr do Sol no Potengi",
        "price_string": '<p class="detail-sidebar__price">A partir de R$ 125 <span>/ pessoa</span></p>',
        "sticky_price": "A partir de R$ 125",
        "duration": "2-3 horas",
        "description": "Navegue pelas águas calmas do Rio Potengi ao fim do dia e desfrute do mais belo pôr do sol de Natal, com vista privilegiada para o Forte dos Reis Magos e a ponte Newton Navarro.",
        "whatsapp_name": "Pôr do Sol no Potengi",
        "inclusions": ["Passeio de barco no Rio Potengi", "Música ambiente a bordo", "Serviço de bordo (guia)"],
        "exclusions": ["Transporte até o local de embarque (Iate Clube de Natal)", "Comidas e bebidas consumidas no barco"],
        "what_to_bring": ["Câmera ou smartphone para fotos", "Protetor solar (para o início do passeio)", "Agasalho leve para o fim de tarde"]
    }
]

exclusivas = [
    {
        "filename": "experiencias-exclusivas/voo-helicoptero.html",
        "title": "Voo Panorâmico de Helicóptero",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Voo</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "15 a 30 mins",
        "description": "Veja Natal de uma perspectiva única e inesquecível. Sobrevoe as dunas, o litoral e os principais pontos turísticos da cidade com conforto e total segurança.",
        "whatsapp_name": "Voo Panorâmico",
        "inclusions": ["Voo exclusivo para até 4 ou 6 passageiros (dependendo da aeronave)", "Piloto executivo experiente", "Briefing de segurança inicial"],
        "exclusions": ["Transporte terrestre até o heliponto", "Alimentação e bebidas", "Fotografia ou filmagem profissional (opcional)"],
        "what_to_bring": ["Documento de identidade original", "Câmera fotográfica ou smartphone", "Óculos de sol"]
    },
    {
        "filename": "experiencias-exclusivas/passeio-aviao.html",
        "title": "Voo de Aeronave para Estados Vizinhos",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Voo</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "Personalizado",
        "description": "Acesse os destinos mais remotos e deslumbrantes do Nordeste com total exclusividade em nossa aeronave privada. Economize horas de viagem e desfrute de vistas aéreas inesquecíveis.",
        "whatsapp_name": "Voo de Aeronave",
        "inclusions": ["Fretamento de aeronave exclusiva", "Flexibilidade de horários e rotas", "Serviço de bordo VIP", "Atendimento coordenado"],
        "exclusions": ["Transfer terrestre na origem/destino", "Taxas de pouso em aeroportos não conveniados", "Acomodação no destino"],
        "what_to_bring": ["Documentos pessoais originais com foto", "Bagagem dentro dos limites estabelecidos", "Roupas confortáveis"]
    },
    {
        "filename": "experiencias-exclusivas/veleiro-noronha.html",
        "title": "Charter de Veleiro para Noronha",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Charter</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "Vários dias",
        "description": "Uma travessia oceânica luxuosa rumo ao arquipélago de Fernando de Noronha. Sinta a liberdade do mar a bordo de um veleiro equipado com todo o conforto e tripulação à sua disposição.",
        "whatsapp_name": "Charter para Noronha",
        "inclusions": ["Fretamento de veleiro com cabines de luxo", "Skipper (capitão) e tripulação experiente", "Alimentação completa a bordo", "Equipamentos de snorkel e stand-up paddle"],
        "exclusions": ["Taxa de Preservação Ambiental (TPA) de Noronha", "Ingressos do Parque Nacional Marinho", "Bebidas alcoólicas premium (personalizável)"],
        "what_to_bring": ["Roupas leves, de banho e corta-vento", "Protetor solar biodegradável", "Medicamentos de uso pessoal (inclusive para enjoo)"]
    },
    {
        "filename": "experiencias-exclusivas/buggy-vip.html",
        "title": "Passeio Diferenciado VIP",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Experiência</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "Tarde e Noite",
        "description": "O clássico passeio de buggy elevado ao máximo luxo: roteiro personalizado, serviço de fotógrafo profissional, espumante gelado e um jantar romântico exclusivo montado apenas para você na praia.",
        "whatsapp_name": "Passeio de Buggy VIP",
        "inclusions": ["Buggy premium e motorista/guia exclusivo", "Sessão de fotos com fotógrafo profissional", "Espumante ou vinho para brindar o pôr do sol", "Jantar romântico montado na praia com menu personalizado"],
        "exclusions": ["Taxas de atividades nas lagoas (aerobunda, etc.)", "Bebidas adicionais não acordadas previamente", "Transporte aéreo"],
        "what_to_bring": ["Roupas de banho elegantes para fotos", "Protetor solar", "Repelente para o fim de tarde"]
    },
    {
        "filename": "experiencias-exclusivas/mergulho-maracajau.html",
        "title": "Mergulho Privado em Maracajaú",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Lancha Privada</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "Dia inteiro",
        "description": "Esqueça os barcos lotados. Preparamos uma lancha privada exclusivamente para você e seus convidados conhecerem os parrachos de Maracajaú, com instrutores dedicados só para o seu grupo.",
        "whatsapp_name": "Mergulho Privado em Maracajaú",
        "inclusions": ["Transfer VIP em veículo executivo", "Lancha exclusiva e marinheiro", "Equipamentos de mergulho premium", "Instrutor de mergulho dedicado ao grupo", "Bebidas a bordo"],
        "exclusions": ["Refeições no restaurante base", "Fotos e vídeos subaquáticos (pode ser contratado à parte)"],
        "what_to_bring": ["Roupas de banho", "Protetor solar (aplicar antes da travessia)", "Toalha pessoal"]
    },
    {
        "filename": "experiencias-exclusivas/rota-secreta-praias.html",
        "title": "Rota Secreta de Praias Selvagens",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Veículo 4x4</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "Dia inteiro",
        "description": "Aventure-se por trilhas exclusivas que revelam praias intocadas e lugares que a maioria dos turistas nunca ouvirá falar. Uma jornada premium guiada por experts locais da região.",
        "whatsapp_name": "Rota Secreta de Praias",
        "inclusions": ["Veículo 4x4 Land Rover ou similar", "Guia expert em expedições off-road", "Cooler com bebidas geladas e snacks premium", "Roteiro fora do circuito tradicional"],
        "exclusions": ["Almoço em restaurante local", "Equipamentos esportivos extras (kitesurf, surf)"],
        "what_to_bring": ["Roupas de aventura e banho", "Protetor solar", "Calçado apropriado para caminhada curta"]
    },
    {
        "filename": "experiencias-exclusivas/rota-norte-helicoptero.html",
        "title": "Rota Norte + Sobrevoo",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Experiência</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "Meio dia",
        "description": "Combine a adrenalina das dunas de Genipabu com as vistas incomparáveis de um sobrevoo de helicóptero sobre as lagoas e a costa norte. A experiência definitiva para quem busca o máximo da emoção potiguar.",
        "whatsapp_name": "Rota Norte com Sobrevoo",
        "inclusions": ["Transporte VIP até as dunas", "Passeio de buggy com motorista credenciado", "Voo panorâmico de helicóptero (15 a 30 mins)"],
        "exclusions": ["Taxas ambientais e de balsa do passei de buggy", "Atrações nas lagoas (esquibunda, etc.)", "Alimentação"],
        "what_to_bring": ["Roupas leves", "Câmera fotográfica ou smartphone", "Óculos de sol"]
    },
    {
        "filename": "experiencias-exclusivas/vip-sao-miguel.html",
        "title": "Escapada VIP São Miguel do Gostoso",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Experiência</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "1 ou 2 dias",
        "description": "Chegue à charmosa São Miguel do Gostoso com transporte de luxo, acesso privilegiado aos melhores beach clubs da cidade e reservas garantidas nos restaurantes mais concorridos.",
        "whatsapp_name": "Escapada VIP para São Miguel",
        "inclusions": ["Transfer executivo ou em 4x4 de luxo de Natal a São Miguel das Gostoso", "Reserva VIP em beach club com day use", "Guia host à disposição", "Água e espumante no veículo"],
        "exclusions": ["Consumação no beach club/restaurante", "Pernoite ou hospedagem (se não acordado)", "Aulas de Kitesurf/Windsurf"],
        "what_to_bring": ["Looks para praia e beach club", "Protetor solar e óculos de sol", "Câmera fotográfica"]
    },
    {
        "filename": "experiencias-exclusivas/rota-natal-fortaleza.html",
        "title": "Expedição Natal a Fortaleza",
        "price_string": '<p class="detail-sidebar__price">Sob Consulta <span>/ Expedição</span></p>',
        "sticky_price": "Sob Consulta",
        "duration": "5 dias / 4 noites",
        "description": "A jornada off-road definitiva cruzando praias paradisíacas entre os dois estados. Uma expedição de luxo com pernoites em pousadas selecionadas a dedo e gastronomia regional de alta qualidade.",
        "whatsapp_name": "Rota Natal-Fortaleza",
        "inclusions": ["Veículos 4x4 de alto padrão com guia/motorista expedicionário", "Hospedagem em pousadas de charme com café da manhã", "Travessias de balsa e taxas rodoviárias/ambientais", "Suporte 24h durante todo o trajeto"],
        "exclusions": ["Almoços e jantares (para maior liberdade gastronômica)", "Passeios extras nos destinos (barcos, buggys locais)"],
        "what_to_bring": ["Mala flexível (duffel bag) de até 15kg", "Roupas com proteção UV e roupas de banho", "Protetor solar, repelente e chapéu"]
    }
]

def generate_pages(item_list, template_file, is_exclusive=False):
    with open(template_file, "r", encoding="utf-8") as f:
        html = f.read()

    for item in item_list:
        content = html
        
        if is_exclusive:
            content = re.sub(r'<a href="\.\./experiencias\.html#classicos">Passeios Clássicos</a>', '<a href="../experiencias.html#exclusivas">Experiências Exclusivas</a>', content)
            content = re.sub(r'<span class="section-label">Passeio Clássico</span>', '<span class="section-label">Experiência Exclusiva</span>', content)

        # Replace titles
        content = re.sub(r"<title>.*?</title>", f"<title>{item['title']} | NatalExperience Tours</title>", content)
        content = re.sub(r'<h1 style=".*?">(.*?)</h1>', f'<h1 style="font-size: clamp(1.8rem, 4vw, 2.8rem); margin-bottom: var(--space-sm);">{item["title"]}</h1>', content)
        
        # Specific updates for breadcrumb
        content = re.sub(r'</a> <span>›</span>\s*Buggy pelo Litoral Norte\s*</div>', f'</a> <span>›</span>\n        {item["title"]}\n      </div>', content)
        
        # Meta description
        content = re.sub(r'name="description" content=".*?"', f'name="description" content="{item["description"]} Reserve pelo WhatsApp!"', content)
        
        # Duration, Group, Departure
        content = re.sub(r'<strong>Duração:</strong>.*?</span>', f'<strong>Duração:</strong> {item.get("duration", "Consulte-nos")}</span>', content, flags=re.DOTALL)
        content = re.sub(r'<strong>Grupo:</strong>.*?</span>', f'<strong>Grupo:</strong> {item.get("group_size", "Personalizado")}</span>', content, flags=re.DOTALL)
        content = re.sub(r'<strong>Saída:</strong>.*?</span>', f'<strong>Saída:</strong> {item.get("departure", "A combinar")}</span>', content, flags=re.DOTALL)

        # Description text
        content = re.sub(r'<h3 style="margin-bottom: var\(--space-sm\);">Sobre o Passeio</h3>\s*<p.*?>.*?</p>\s*<p.*?>.*?</p>', f'<h3 style="margin-bottom: var(--space-sm);">Sobre a Experiência</h3>\n          <p style="color:var(--color-text-light); line-height:1.8; margin-bottom: var(--space-md);">\n            {item["description"]}\n          </p>', content, flags=re.DOTALL)

        # Prices
        content = re.sub(r'<p class="detail-sidebar__price">R\$ 180 <span>/ por pessoa</span></p>', item["price_string"], content)
        content = re.sub(r'<div class="sticky-cta__price"><span>A partir de</span>R\$ 180</div>', f'<div class="sticky-cta__price"><span></span>{item["sticky_price"]}</div>', content)

        # WhatsApp buttons
        content = re.sub(r'data-whatsapp-message="Olá! Quero reservar o passeio .*?!"', f'data-whatsapp-message="Olá! Quero reservar a experiência {item["whatsapp_name"]}!"', content)
        content = re.sub(r'data-whatsapp-message="Olá! Gostaria de reservar o passeio .*? para a data', f'data-whatsapp-message="Olá! Gostaria de reservar a experiência {item["whatsapp_name"]} para a data', content)
        content = re.sub(r'data-whatsapp-message="Olá! Gostaria de reservar o passeio .*?\.', f'data-whatsapp-message="Olá! Gostaria de reservar a experiência {item["whatsapp_name"]}.', content)
        content = re.sub(r'data-whatsapp-message="Olá! Tenho uma dúvida sobre .*?\.', f'data-whatsapp-message="Olá! Tenho uma dúvida sobre a experiência {item["whatsapp_name"]}.', content)
        content = re.sub(r'Quero reservar o Buggy Litoral Norte!', f'Quero reservar {item["whatsapp_name"]}!', content)

        # Title word in placeholder instead of emoji
        short_title = item['title'].split()[0]
        content = re.sub(r'<span style="font-size:4rem; color:rgba\(255,255,255,0\.8\);">.*?</span>', f'<span style="font-size:4rem; color:rgba(255,255,255,0.8);">{short_title}</span>', content)

        # Itinerary
        if "itinerary" in item:
            itin_html = ""
            for step in item["itinerary"]:
                itin_html += f"            <p><strong>{step['time']}</strong> — {step['desc']}</p>\n"
            content = re.sub(r'<h3 style="margin-bottom: var\(--space-sm\); margin-top: var\(--space-lg\);">Roteiro do Dia</h3>\s*<div style="color:var\(--color-text-light\); line-height:2; margin-bottom: var\(--space-lg\);">.*?</div>',
                f'<h3 style="margin-bottom: var(--space-sm); margin-top: var(--space-lg);">Roteiro do Dia</h3>\n          <div style="color:var(--color-text-light); line-height:2; margin-bottom: var(--space-lg);">\n{itin_html}          </div>',
                content, flags=re.DOTALL)
        else:
            # Remove the itinerary section completely
            content = re.sub(r'<h3 style="margin-bottom: var\(--space-sm\); margin-top: var\(--space-lg\);">Roteiro do Dia</h3>\s*<div style="color:var\(--color-text-light\); line-height:2; margin-bottom: var\(--space-lg\);">.*?</div>', '', content, flags=re.DOTALL)

        # Inclusions
        if "inclusions" in item:
            inc_html = ""
            for inc in item["inclusions"]:
                inc_html += f"""            <li>
              <div class="tour-list__icon tour-list__icon--check"><svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none"><path d="M20 6L9 17l-5-5"/></svg></div>
              {inc}
            </li>\n"""
            # Replace the static list in the template
            content = re.sub(r'<h3 style="margin-bottom: var\(--space-sm\);">O Que Está Incluído</h3>\s*<ul class="tour-list">.*?</ul>', f'<h3 style="margin-bottom: var(--space-sm);">O Que Está Incluído</h3>\n          <ul class="tour-list">\n{inc_html}          </ul>', content, flags=re.DOTALL)

        # Exclusions
        if "exclusions" in item:
            exc_html = ""
            for exc in item["exclusions"]:
                exc_html += f"""            <li>
              <div class="tour-list__icon tour-list__icon--cross"><svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none"><path d="M18 6L6 18M6 6l12 12"/></svg></div>
              {exc}
            </li>\n"""
            content = re.sub(r'<h3 style="margin-bottom: var\(--space-sm\); margin-top: var\(--space-lg\);">O Que Não Está Incluído</h3>\s*<ul class="tour-list">.*?</ul>', f'<h3 style="margin-bottom: var(--space-sm); margin-top: var(--space-lg);">O Que Não Está Incluído</h3>\n          <ul class="tour-list">\n{exc_html}          </ul>', content, flags=re.DOTALL)
            
        # What to bring
        if "what_to_bring" in item:
            wtb_html = ""
            for wtb in item["what_to_bring"]:
                wtb_html += f"""            <li>
              <div class="tour-list__icon tour-list__icon--info"><svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg></div>
              {wtb}
            </li>\n"""
            content = re.sub(r'<h3 style="margin-bottom: var\(--space-sm\); margin-top: var\(--space-lg\);">O Que Levar</h3>\s*<ul class="tour-list">.*?</ul>', f'<h3 style="margin-bottom: var(--space-sm); margin-top: var(--space-lg);">O Que Levar</h3>\n          <ul class="tour-list">\n{wtb_html}          </ul>', content, flags=re.DOTALL)

        # Recommended (Veja Também) Section
        all_tours = classicos + exclusivas
        other_tours = [t for t in all_tours if t["filename"] != item["filename"]]
        recommended = random.sample(other_tours, min(3, len(other_tours)))
        
        rec_html = '<div class="tour-grid">\n'
        placeholders = ['ocean', 'sunset', 'nature', 'city']
        for idx, rec in enumerate(recommended):
            delay_class = f" delay-{idx}" if idx > 0 else ""
            placeholder = placeholders[idx % len(placeholders)]
            link = f"../{rec['filename']}"
            
            rec_html += f"""        <div class="tour-card animate-on-scroll{delay_class}">
          <div class="tour-card__image">
            <div class="placeholder-img placeholder-img--{placeholder}"></div>
          </div>
          <div class="tour-card__body">
            <h3 class="tour-card__title">{rec['title']}</h3>
            <div class="tour-card__info">
              <span class="tour-card__duration"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {rec.get('duration', 'Consulte')}</span>
              <strong class="tour-card__price">{rec.get('sticky_price', 'Sob Consulta')}</strong>
            </div>
            <a href="{link}" class="btn btn--outline-dark btn--sm">Ver detalhes</a>
          </div>
        </div>\n"""
        rec_html += '      </div>'
        
        rec_pattern = r'<h2 style="text-align:center; margin-bottom:var\(--space-xl\); color:var\(--color-navy\);">Veja Também</h2>\s*<div class="tour-grid">.*?</section>'
        replacement = f'<h2 style="text-align:center; margin-bottom:var(--space-xl); color:var(--color-navy);">Veja Também</h2>\n      {rec_html}\n    </div>\n  </section>'
        content = re.sub(rec_pattern, replacement, content, flags=re.DOTALL)

        out_path = os.path.join(".", item["filename"])
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(content)
        print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_pages(classicos, "passeios/buggy-litoral-norte.html", is_exclusive=False)
    generate_pages(exclusivas, "passeios/buggy-litoral-norte.html", is_exclusive=True)
