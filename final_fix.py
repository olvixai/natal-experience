import os
import re

rep_map = {
    'InÍcio': 'Início',
    'Inesquecìveis': 'Inesquecíveis',
    'Experiencia': 'Experiência',
    'Experiencias': 'Experiências',
    'Conheça': 'Conheça',
    'há': 'há',
    'até': 'até',
    'missão': 'missão',
    'turístico': 'turístico',
    'férias': 'férias',
    'última': 'última',
    'Região': 'Região',
    'bilíngue': 'bilíngue',
    'Português': 'Português',
    'Inglês': 'Inglês',
    'segurança': 'segurança',
    'veículos': 'veículos',
    'únicos': 'únicos',
    'referência': 'referência',
    'página': 'página',
    'Legislação': 'Legislação',
    'Clássicos': 'Clássicos',
    'Olá': 'Olá',
    'está': 'está',
    'São': 'São',
    'você': 'você',
    'Nossos Clientes Dice': 'Nossos Clientes Dizem',
}

# The problem is that I don't know the exact broken character if it's already ? or something else.
# But I can fix the icons specifically.

def fix_content(text):
    # Fix phone number (the main task)
    text = text.replace('999868411', '99868411')
    
    # Restoring icons which are currently '??'
    text = text.replace('?? Rua Túlio', '📍 Rua Túlio')
    text = text.replace('?? +55', '📞 +55')
    text = text.replace('?? natalexperiencetours', '📧 natalexperiencetours')
    text = text.replace('Feito com ??', 'Feito com ❤️')
    text = text.replace('aria-label="Instagram">??</a>', 'aria-label="Instagram">📷</a>')
    text = text.replace('aria-label="Facebook">??</a>', 'aria-label="Facebook">📘</a>')
    text = text.replace('aria-label="YouTube">??</a>', 'aria-label="YouTube">▶️</a>')
    
    # Portuguese fixes (common broken ones from view_file)
    text = text.replace('Incio', 'Início')
    text = text.replace('Experincias', 'Experiências')
    text = text.replace('Experincia', 'Experiência')
    text = text.replace('Inesquecveis', 'Inesquecíveis')
    text = text.replace('h', 'há')
    text = text.replace('at', 'até')
    text = text.replace('paixo', 'paixão')
    text = text.replace('turstico', 'turístico')
    text = text.replace('frias', 'férias')
    text = text.replace('misso', 'missão')
    text = text.replace('Conhea', 'Conheça')
    text = text.replace('Regio', 'Região')
    text = text.replace('bilngue', 'bilíngue')
    text = text.replace('Portugus', 'Português')
    text = text.replace('Ingls', 'Inglês')
    text = text.replace('segurana', 'segurança')
    text = text.replace('veculos', 'veículos')
    text = text.replace('nicos', 'únicos')
    text = text.replace('referncia', 'referência')
    text = text.replace('pgina', 'página')
    text = text.replace('Legislao', 'Legislação')
    text = text.replace('Clssicos', 'Clássicos')
    text = text.replace('Ol', 'Olá')
    text = text.replace('est', 'está')
    text = text.replace('So', 'São')
    text = text.replace('voc', 'você')
    text = text.replace('aniversrios', 'aniversários')
    text = text.replace('celebrao', 'celebração')
    
    return text

target_dir = r'e:\ANTIGRAVITY\NATALEXPERIENCE'

for root, dirs, files in os.walk(target_dir):
    for name in files:
        if name.endswith('.html') or name.endswith('.js'):
            filepath = os.path.join(root, name)
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            
            new_text = fix_content(text)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_text)
            print(f"Fixed {filepath}")
