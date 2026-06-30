import os
import re
import json

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "image_mapping.json"), "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Synthetic entry: hero-natal.png never existed as a real file (sitewide broken
# reference), now backed by a copy of f0.webp (1920x1080 Forte dos Reis Magos aerial)
mapping["hero-natal.png"] = {"new_file": "hero-natal.webp", "width": 1920, "height": 1080}

# Sort by filename length descending to avoid partial-match collisions
old_names = sorted(mapping.keys(), key=len, reverse=True)

HTML_DIRS = [ROOT, os.path.join(ROOT, "passeios"), os.path.join(ROOT, "experiencias-exclusivas"),
             os.path.join(ROOT, "blog")]

def find_html_files():
    files = []
    for d in HTML_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if fname.endswith(".html"):
                files.append(os.path.join(d, fname))
    return files

def replace_filenames(content):
    for old in old_names:
        new = mapping[old]["new_file"]
        old_esc = re.escape(old)
        # match old filename optionally followed by a query string, before a
        # quote/paren/space delimiter so we don't touch unrelated substrings
        pattern = re.compile(old_esc + r'(\?[^"\'\s)]*)?(?=["\')\s])')
        content = pattern.sub(new, content)
    return content

IMG_TAG_RE = re.compile(r'<img\b[^>]*>')

def enhance_img_tags(content):
    def process(m):
        tag = m.group(0)
        src_match = re.search(r'src="([^"]+)"', tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        basename = os.path.basename(src.split("?")[0])
        dims = None
        for old, info in mapping.items():
            if info["new_file"] == basename:
                dims = info
                break
        if dims and "width" not in tag:
            tag = tag.replace(
                f'src="{src}"',
                f'src="{src}" width="{dims["width"]}" height="{dims["height"]}"'
            )
        if "loading=" not in tag:
            tag = tag[:-1] + ' loading="lazy">'
        return tag
    return IMG_TAG_RE.sub(process, content)

def main():
    files = find_html_files()
    changed = 0
    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = replace_filenames(content)
        new_content = enhance_img_tags(new_content)
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed += 1
            print(f"updated {os.path.relpath(filepath, ROOT)}")
    print(f"\n{changed}/{len(files)} HTML files updated")

if __name__ == "__main__":
    main()
