import os

replacements = {
    '999868411': '99868411',
    '?? Rua T\ufffdo Fernandes': '📍 Rua T\u00falio Fernandes', # Fixing Tlio too
    '?? +55 84 9986-8411': '📞 +55 84 9986-8411',
    '?? natalexperiencetours@gmail.com': '📧 natalexperiencetours@gmail.com',
    'Feito com ?? em Natal': 'Feito com ❤️ em Natal',
    'aria-label="Instagram">??</a>': 'aria-label="Instagram">📷</a>',
    'aria-label="Facebook">??</a>': 'aria-label="Facebook">📘</a>',
    'aria-label="YouTube">??</a>': 'aria-label="YouTube">▶️</a>',
    'Que Nossos Clientes ??Dizem??': 'O Que Nossos Clientes <span class="gold-text">Dizem</span>',
    'Quem Somos</h1>': 'Quem Somos</h1>', # Ensure it's not broken
}

# Regex-like manual replacements for more complex cases if needed
# But let's start with basic ones.

target_dir = r'e:\ANTIGRAVITY\NATALEXPERIENCE'

for root, dirs, files in os.walk(target_dir):
    for name in files:
        if name.endswith('.html'):
            filepath = os.path.join(root, name)
            try:
                # Read as bytes to handle potential nulls or weird encoding
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                # Check for null bytes (corruption)
                if b'\x00' in content:
                    print(f"Fixing nulls in {name}")
                    content = content.replace(b'\x00', b'')

                # Convert to string (handling potential decode errors)
                text = content.decode('utf-8', errors='replace')
                
                # Apply replacements
                for old, new in replacements.items():
                    text = text.replace(old, new)
                
                # Special cases for ?? in value cards if they are consistent
                # 📍 (Address), 📞 (Phone), 💬 (Chat/WhatsApp), 🧭 (Compass), etc.
                # Since I don't know the exact ones per page, I'll be careful.
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Processed {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
