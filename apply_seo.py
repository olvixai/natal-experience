import os
import re
from datetime import datetime

DOMAIN = "https://www.natalexperience.com"
DEFAULT_IMAGE = f"{DOMAIN}/img/hero-natal.png"

def update_seo_tags(filepath):
    # Determine the relative URL
    rel_path = os.path.relpath(filepath, ".").replace("\\", "/")
    
    # Skip temporary or hidden files
    if rel_path.startswith(".") or rel_path == "template.html":
        return None

    # Construct absolute URL
    url = f"{DOMAIN}/{rel_path}"
    # Special case for index
    if rel_path == "index.html":
        url = f"{DOMAIN}/"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find </head>
    head_end_match = re.search(r'</head>', content, re.IGNORECASE)
    if not head_end_match:
        print(f"Warning: No </head> found in {filepath}")
        return None

    head_content = content[:head_end_match.start()]
    body_content = content[head_end_match.start():]

    # Clean existing canonical, og:url, og:image to avoid duplicates
    head_content = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>\s*', '', head_content, flags=re.IGNORECASE)
    head_content = re.sub(r'<meta\s+property="og:url"\s+content="[^"]*"\s*/?>\s*', '', head_content, flags=re.IGNORECASE)
    head_content = re.sub(r'<meta\s+property="og:image"\s+content="[^"]*"\s*/?>\s*', '', head_content, flags=re.IGNORECASE)

    # Prepare tags to inject
    tags_to_inject = f"""
  <link rel="canonical" href="{url}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DEFAULT_IMAGE}">
"""
    # Insert right before </head>
    new_content = head_content + tags_to_inject + body_content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return url

def main():
    sitemap_urls = []
    
    for root, dirs, files in os.walk("."):
        # Ignore common non-public dirs
        if "css" in root or "js" in root or "img" in root or ".git" in root or "apps-script" in root:
            continue
            
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                url = update_seo_tags(filepath)
                if url:
                    # Give different priorities
                    priority = "0.8"
                    if "index.html" in url:
                        priority = "1.0"
                    elif "passeios/" in url or "experiencias-exclusivas/" in url:
                        priority = "0.9"
                    elif "blog/" in url:
                        priority = "0.7"
                        
                    sitemap_urls.append((url, priority))
                    print(f"Updated SEO tags for: {filepath}")

    # Generate sitemap.xml
    today = datetime.now().strftime("%Y-%m-%d")
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority in sitemap_urls:
        sitemap_content += "  <url>\n"
        sitemap_content += f"    <loc>{url}</loc>\n"
        sitemap_content += f"    <lastmod>{today}</lastmod>\n"
        sitemap_content += f"    <changefreq>weekly</changefreq>\n"
        sitemap_content += f"    <priority>{priority}</priority>\n"
        sitemap_content += "  </url>\n"
    sitemap_content += "</urlset>\n"

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml")

    # Generate robots.txt
    robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("Generated robots.txt")

if __name__ == "__main__":
    main()
