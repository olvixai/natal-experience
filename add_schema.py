import re
import os
import json
import html

DOMAIN = "https://www.natalexperience.com"
ROOT = os.path.dirname(os.path.abspath(__file__))

MONTHS = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12",
}

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def get_title(content):
    m = re.search(r"<title>(.*?)</title>", content, re.S)
    if not m:
        return ""
    return html.unescape(m.group(1)).split("|")[0].strip()

def get_meta_description(content):
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    return html.unescape(m.group(1)) if m else ""

def get_canonical(content):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    return m.group(1) if m else ""

def resolve_url(base_subdir, href):
    href = href.split("#")[0]
    if href.startswith("http"):
        return href
    href = href.replace("../", "")
    return f"{DOMAIN}/{href}"

def get_breadcrumbs(content, base_subdir, current_name, current_url):
    m = re.search(r'<div class="breadcrumbs">(.*?)</div>', content, re.S)
    items = []
    pos = 1
    if m:
        inner = m.group(1)
        links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', inner)
        for href, text in links:
            items.append({
                "@type": "ListItem",
                "position": pos,
                "name": html.unescape(text).strip(),
                "item": resolve_url(base_subdir, href)
            })
            pos += 1
    items.append({
        "@type": "ListItem",
        "position": pos,
        "name": current_name,
        "item": current_url
    })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

def get_h1(content):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.S)
    if not m:
        return ""
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()

def get_first_gallery_image(content):
    m = re.search(r'bento-gallery__main[^>]*>\s*<img src="([^"]+)"', content, re.S)
    if m:
        src = m.group(1).split("?")[0]
        return resolve_url("", src)
    return f"{DOMAIN}/img/hero-natal.png"

def get_main_price(content):
    matches = re.findall(
        r'<div class="card__price" style="font-size: 1\.8rem;">.*?R\$\s*([\d.,]+)',
        content
    )
    if matches:
        price = matches[0].replace(".", "").replace(",", ".")
        return price
    return None

def build_tour_schema(filepath, base_subdir):
    content = read(filepath)
    title = get_title(content)
    description = get_meta_description(content)
    canonical = get_canonical(content)
    h1 = get_h1(content) or title
    image = get_first_gallery_image(content)
    price = get_main_price(content)

    breadcrumb = get_breadcrumbs(content, base_subdir, h1, canonical)

    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": h1,
        "description": description,
        "image": image,
        "url": canonical,
        "brand": {
            "@type": "Brand",
            "name": "NatalExperience Tours"
        },
        "additionalType": "https://schema.org/TouristTrip"
    }

    if price:
        product["offers"] = {
            "@type": "Offer",
            "url": canonical,
            "priceCurrency": "BRL",
            "price": price,
            "availability": "https://schema.org/InStock",
            "validFrom": "2026-01-01"
        }

    return breadcrumb, product

def inject_schemas(filepath, schemas):
    content = read(filepath)
    if 'application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "Product"' in content or '"@type": "BreadcrumbList"' in content:
        return False
    blocks = ""
    for schema in schemas:
        blocks += f'  <script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n  </script>\n'
    new_content = content.replace("</head>", blocks + "</head>")
    write(filepath, new_content)
    return True

def process_tour_dir(dirname):
    dirpath = os.path.join(ROOT, dirname)
    count = 0
    for fname in os.listdir(dirpath):
        if not fname.endswith(".html"):
            continue
        filepath = os.path.join(dirpath, fname)
        breadcrumb, product = build_tour_schema(filepath, dirname)
        if inject_schemas(filepath, [breadcrumb, product]):
            count += 1
            print(f"  + {dirname}/{fname}")
    return count

def parse_pt_date(date_text):
    m = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", date_text)
    if not m:
        return "2026-01-01"
    day, month_name, year = m.groups()
    month = MONTHS.get(month_name.lower(), "01")
    return f"{year}-{month}-{day.zfill(2)}"

def process_blog():
    dirpath = os.path.join(ROOT, "blog")
    count = 0
    for fname in os.listdir(dirpath):
        if not fname.endswith(".html"):
            continue
        filepath = os.path.join(dirpath, fname)
        content = read(filepath)

        title = get_title(content)
        description = get_meta_description(content)
        canonical = get_canonical(content)

        m_title = re.search(r'<h1 class="post-title">(.*?)</h1>', content, re.S)
        post_title = html.unescape(re.sub(r"<[^>]+>", "", m_title.group(1))).strip() if m_title else title

        m_cat = re.search(r'<span class="post-category">(.*?)</span>', content)
        category = html.unescape(m_cat.group(1)).strip() if m_cat else "Dicas de Viagem"

        m_date = re.search(r'<span>📅\s*(.*?)</span>', content)
        date_text = m_date.group(1).strip() if m_date else ""
        iso_date = parse_pt_date(date_text)

        m_img = re.search(r'post-header[^>]*style="background-image:\s*url\(\'([^\']+)\'\)', content)
        image = resolve_url("blog", m_img.group(1)) if m_img else f"{DOMAIN}/img/hero-natal.png"

        blog_schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post_title,
            "description": description,
            "image": image,
            "url": canonical,
            "datePublished": iso_date,
            "dateModified": iso_date,
            "articleSection": category,
            "inLanguage": "pt-BR",
            "author": {
                "@type": "Organization",
                "name": "NatalExperience Tours",
                "url": DOMAIN
            },
            "publisher": {
                "@type": "Organization",
                "name": "NatalExperience Tours",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{DOMAIN}/img/logo-minimal.png"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical
            }
        }

        breadcrumb = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{DOMAIN}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{DOMAIN}/blog.html"},
                {"@type": "ListItem", "position": 3, "name": post_title, "item": canonical},
            ]
        }

        if inject_schemas(filepath, [breadcrumb, blog_schema]):
            count += 1
            print(f"  + blog/{fname}")
    return count

def main():
    print("Processing passeios/...")
    n1 = process_tour_dir("passeios")
    print("Processing experiencias-exclusivas/...")
    n2 = process_tour_dir("experiencias-exclusivas")
    print("Processing blog/...")
    n3 = process_blog()
    print(f"\nTotal updated: {n1 + n2 + n3} pages")

if __name__ == "__main__":
    main()
