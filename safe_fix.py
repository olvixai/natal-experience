import os

def safe_replace(filepath, search_str, replace_str):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check if the search string exists
        if search_str in content:
            new_content = content.replace(search_str, replace_str)
            with open(filepath, 'wb') as f:
                f.write(new_content)
            print(f"Update: {filepath}")
        else:
            # print(f"No match: {filepath}")
            pass
    except Exception as e:
        print(f"Error updating {filepath}: {e}")

target_dir = r'e:\ANTIGRAVITY\NATALEXPERIENCE'

targets = [
    (b'999868411', b'99868411'),
]

for root, dirs, files in os.walk(target_dir):
    for name in files:
        if name.endswith('.html') or name.endswith('.js'):
            filepath = os.path.join(root, name)
            for search, replace in targets:
                safe_replace(filepath, search, replace)
