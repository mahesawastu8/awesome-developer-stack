#!/usr/bin/env python3
"""
Autonomous Multi-Page Static Site & SEO Generator
Converts all markdown benchmarks into standalone, schema-enriched HTML pages,
builds XML sitemap, robots.txt, and IndexNow key verification.
"""
import os
import re
import json

ROOT_DIR = "/tmp/affiliate-engine/github-hub"
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
BASE_URL = "https://mahesawastu8.github.io/awesome-developer-stack"
INDEXNOW_KEY = "8f3b2a9e1d7c4b5a6f8e0d2c4b6a8e0f"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} (2026 Benchmark)</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph / Social -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical_url}">
    
    <!-- Schema.org TechArticle JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "TechArticle",
      "headline": "{title}",
      "description": "{description}",
      "author": {{
        "@type": "Person",
        "name": "Dimas Wastu"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Awesome Developer Stack"
      }},
      "datePublished": "2026-11-08",
      "dateModified": "2026-11-08"
    }}
    </script>

    <style>
        :root {{
            --bg: #0b0f19;
            --surface: #141d2f;
            --border: #233152;
            --text: #f1f5f9;
            --muted: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --code-bg: #1e293b;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text); line-height: 1.7; padding: 2rem 1rem; }}
        .container {{ max-width: 820px; margin: 0 auto; }}
        nav {{ margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
        nav a {{ color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.95rem; }}
        article h1 {{ font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 1rem; line-height: 1.25; }}
        article h2 {{ font-size: 1.5rem; font-weight: 700; color: #fff; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }}
        article h3 {{ font-size: 1.2rem; font-weight: 600; color: #e2e8f0; margin: 1.5rem 0 0.75rem; }}
        article p {{ margin-bottom: 1.25rem; color: #cbd5e1; font-size: 1.05rem; }}
        article ul, article ol {{ margin-bottom: 1.25rem; padding-left: 1.5rem; color: #cbd5e1; }}
        article li {{ margin-bottom: 0.5rem; }}
        article table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.95rem; }}
        article th, article td {{ border: 1px solid var(--border); padding: 0.75rem 1rem; text-align: left; }}
        article th {{ background: var(--surface); color: #fff; font-weight: 600; }}
        article tr:nth-child(even) {{ background: rgba(30, 41, 59, 0.4); }}
        article a {{ color: var(--accent); font-weight: 600; text-decoration: underline; }}
        article a:hover {{ color: #7dd3fc; }}
        .cta-box {{ background: var(--surface); border: 1px solid var(--accent); border-radius: 12px; padding: 1.5rem; margin: 2.5rem 0; text-align: center; }}
        .cta-box h3 {{ font-size: 1.3rem; margin-bottom: 0.5rem; color: #fff; }}
        .cta-box p {{ font-size: 0.95rem; color: var(--muted); margin-bottom: 1rem; }}
        .btn {{ display: inline-block; background: var(--accent); color: #0f172a; font-weight: 700; padding: 0.85rem 1.75rem; border-radius: 8px; text-decoration: none; transition: background 0.2s; }}
        .btn:hover {{ background: var(--accent-hover); color: #fff; }}
        footer {{ margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--border); text-align: center; color: var(--muted); font-size: 0.85rem; }}
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="{base_url}/">&larr; Back to Master Directory</a>
            <span>2026 Verified Benchmark</span>
        </nav>
        <article>
            {content}
        </article>
        <footer>
            <p>&copy; 2026 Awesome Developer Stack. Independent, empirical software research.</p>
        </footer>
    </div>
</body>
</html>
"""

def md_to_simple_html(md_text):
    html = md_text
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.M)
    # Bold / Italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', html)
    
    # Process tables
    lines = html.split('\n')
    in_table = False
    table_lines = []
    output_lines = []
    
    for line in lines:
        if line.strip().startswith('|') and line.strip().endswith('|'):
            in_table = True
            table_lines.append(line.strip())
        else:
            if in_table:
                # render table
                table_html = "<table>"
                for idx, tline in enumerate(table_lines):
                    cols = [c.strip() for c in tline.split('|')[1:-1]]
                    if idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cols):
                        continue # separator
                    tag = "th" if idx == 0 else "td"
                    table_html += "<tr>" + "".join(f"<{tag}>{col}</{tag}>" for col in cols) + "</tr>"
                table_html += "</table>"
                output_lines.append(table_html)
                table_lines = []
                in_table = False
            
            # Paragraphs
            sline = line.strip()
            if sline and not sline.startswith('<h') and not sline.startswith('<table') and not sline.startswith('---'):
                if sline.startswith('* ') or sline.startswith('- '):
                    output_lines.append(f"<li>{sline[2:]}</li>")
                elif re.match(r'^\d+\.\s', sline):
                    output_lines.append(f"<li>{sline.split('. ', 1)[1]}</li>")
                else:
                    output_lines.append(f"<p>{sline}</p>")
            elif sline == '---':
                output_lines.append("<hr style='border: 0; border-top: 1px solid var(--border); margin: 2rem 0;'>")
            else:
                output_lines.append(line)
                
    if in_table:
        table_html = "<table>"
        for idx, tline in enumerate(table_lines):
            cols = [c.strip() for c in tline.split('|')[1:-1]]
            if idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cols):
                continue
            tag = "th" if idx == 0 else "td"
            table_html += "<tr>" + "".join(f"<{tag}>{col}</{tag}>" for col in cols) + "</tr>"
        table_html += "</table>"
        output_lines.append(table_html)
        
    return "\n".join(output_lines)

def build_site():
    urls = [f"{BASE_URL}/"]
    
    md_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    print(f"Generating HTML pages for {len(md_files)} benchmark documents...")
    
    for f in md_files:
        path = os.path.join(DOCS_DIR, f)
        with open(path, "r", encoding="utf-8") as file:
            md_content = file.read()
            
        first_line = md_content.split('\n')[0].replace('# ', '').strip()
        title = first_line if first_line else f.replace('.md', '').replace('-', ' ').title()
        description = f"In-depth 2026 empirical benchmark and technical review of {title}. Evaluated on speed, architecture, and utility."
        
        html_filename = f.replace('.md', '.html')
        out_path = os.path.join(DOCS_DIR, html_filename)
        canonical = f"{BASE_URL}/docs/{html_filename}"
        urls.append(canonical)
        
        parsed_html = md_to_simple_html(md_content)
        final_page = TEMPLATE.format(
            title=title,
            description=description,
            canonical_url=canonical,
            base_url=BASE_URL,
            content=parsed_html
        )
        
        with open(out_path, "w", encoding="utf-8") as out_file:
            out_file.write(final_page)
        print(f"Generated: {out_path}")

    # Build sitemap.xml
    sitemap_items = "\n".join([f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-11-08</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""" for u in urls])
    
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}
</urlset>"""

    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print(f"Generated: {sitemap_path} with {len(urls)} indexed pages.")

    # Build robots.txt
    robots_txt = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    robots_path = os.path.join(ROOT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_txt)
    print(f"Generated: {robots_path}")

    # Build IndexNow verification key file
    key_file_path = os.path.join(ROOT_DIR, f"{INDEXNOW_KEY}.txt")
    with open(key_file_path, "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)
    print(f"Generated IndexNow key: {key_file_path}")

if __name__ == "__main__":
    build_site()
