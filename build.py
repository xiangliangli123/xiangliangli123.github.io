#!/usr/bin/env python3
"""Build a small academic website. Uses only the Python standard library."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
DATA = json.loads((ROOT / "content.json").read_text())
STYLE_VERSION = hashlib.sha256((ROOT / "assets" / "style.css").read_bytes()).hexdigest()[:12]
parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="", help="Public HTTPS address. Omit for an unindexed preview.")
args = parser.parse_args()
BASE = args.base_url.rstrip("/")
if BASE and (urlparse(BASE).scheme != "https" or not urlparse(BASE).hostname):
    parser.error("Use the final HTTPS website address.")
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
if (ROOT / "static").exists():
    shutil.copytree(ROOT / "static", OUT, dirs_exist_ok=True)
e = html.escape

def link(url, text, extra=""):
    return f'<a href="{e(url, quote=True)}" {extra}>{e(text)}</a>'

def paper(p, abstract=True):
    title = link(p["url"], p["title"]) if p.get("url") else e(p["title"])
    authors = ""
    if p.get("authors"):
        authors = '<p class="authors">With ' + " and ".join(link(a["url"], a["name"]) for a in p["authors"]) + '</p>'
    venue = f'<p class="venue"><i>{e(p["venue"])}</i> · {p["year"]}</p>' if p.get("venue") else ""
    detail = f'<details><summary>Abstract</summary><p>{e(p["abstract"])}</p></details>' if abstract and p.get("abstract") else ""
    return f'<article class="paper"><h3>{title}</h3>{authors}{venue}{detail}</article>'

def page(title, content, path, research=False):
    prefix = "../" if research else "./"
    canonical = f'<link rel="canonical" href="{e(BASE + path)}">' if BASE else '<meta name="robots" content="noindex, nofollow">'
    structured = {"@context":"https://schema.org", "@type":"Person", "name":DATA["name"], "alternateName":DATA["name_zh"], "jobTitle":DATA["role"], "affiliation":{"@type":"Organization","name":DATA["institution"]}, "email":DATA["email"]}
    if BASE: structured["url"] = BASE + "/"
    description = "Xiangliang Li is an economist at Nankai University. Research in game theory and international trade. Papers, CV, and contact information."
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
{canonical}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website"><meta name="theme-color" content="#163b3c">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/style.css?v={STYLE_VERSION}">
<script type="application/ld+json">{json.dumps(structured, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><a class="wordmark" href="{prefix}">Xiangliang Li<span lang="zh">李相梁</span></a>
<nav aria-label="Main navigation"><a href="{prefix}" {'aria-current="page"' if not research else ''}>About</a><a href="{prefix}research/" {'aria-current="page"' if research else ''}>Research</a>{link(DATA['cv_url'], 'CV')}<a href="mailto:{e(DATA['email'])}">Contact</a></nav></header>
<main id="main">{content}</main>
</body></html>'''

portrait = '<figure class="portrait"><img src="./assets/portrait.jpg" alt="Xiangliang Li" width="600" height="750"></figure>' if (ROOT/'assets'/'portrait.jpg').exists() else '<aside class="profile-note"><span class="chinese-name" lang="zh">李相梁</span><p>School of Finance<br>Nankai University</p><p>PhD in Economics<br>Yale University, 2021</p></aside>'
home = f'''<section class="intro"><div class="intro-copy"><h1>Xiangliang Li</h1><p class="bio">{e(DATA['bio'])}</p><div class="intro-links">{link(DATA['cv_url'], 'Curriculum vitae', 'class="primary-link"')}<a href="mailto:{e(DATA['email'])}">{e(DATA['email'])}</a></div></div>{portrait}</section>
<section class="selected"><div class="section-heading"><h2>Selected research</h2><a href="./research/">All research <span aria-hidden="true">→</span></a></div>{''.join(paper(p,False) for p in DATA['papers'][:3])}</section>'''
(OUT/'index.html').write_text(page('Xiangliang Li | Economics, Nankai University',home,'/'))
sections=[]
for section in ['Working paper','Publications','Work in progress']:
    sections.append(f'<section class="research-section"><h2>{e(section)}</h2><div>{"".join(paper(p) for p in DATA["papers"] if p["section"]==section)}</div></section>')
research='<div class="page-heading"><p class="eyebrow">PAPERS & PROJECTS</p><h1>Research</h1></div>'+''.join(sections)
(OUT/'research').mkdir(exist_ok=True)
(OUT/'research'/'index.html').write_text(page('Research | Xiangliang Li',research,'/research/',True))
# Preserve the old /home path for domain forwarding and bookmarked links.
(OUT/'home').mkdir(exist_ok=True)
(OUT/'home'/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../"><title>Xiangliang Li</title></head><body><a href="../">Go to the homepage</a></body></html>')
(OUT/'.nojekyll').write_text('')
if BASE:
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(BASE+p)}</loc></url>' for p in ['/','/research/'])+'</urlset>\n')
else:
    (OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (OUT/'sitemap.xml').unlink(missing_ok=True)
print(f'Built {OUT} ({"public: "+BASE if BASE else "local preview, noindex"})')
