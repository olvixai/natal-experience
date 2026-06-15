import os

def safe_replace(filepath, search_str, replace_str):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        if search_str in content:
            new_content = content.replace(search_str, replace_str)
            with open(filepath, 'wb') as f:
                f.write(new_content)
            print(f"Update: {filepath}")
    except Exception as e:
        print(f"Error {filepath}: {e}")

target_dir = r'e:\ANTIGRAVITY\NATALEXPERIENCE'

# (Search, Replace)
# We go from what we have (9986) to what we want (99986)
# AND we fix the text format too
targets = [
    (b'99868411', b'999868411'),
    (b'9986-8411', b'99986-8411'),
]

for root, dirs, files in os.walk(target_dir):
    for name in files:
        if name.endswith('.html') or name.endswith('.js'):
            filepath = os.path.join(root, name)
            for search, replace in targets:
                safe_replace(filepath, search, replace)
