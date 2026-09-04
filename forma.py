#!/usr/bin/env python3
"""Remplace Veneta Cucine par Forma (groupe Veneta Cucine) sur les pages concernees."""
import re

LOGO = '/wp-content/uploads/2026/09/logo-forma-cucine.jpg'
LIEN = 'https://formalacucina.fr/'

for P in ['site/index.html', 'site/cuisine/cuisines/index.html']:
    t = open(P, encoding='utf-8').read()
    avant = t

    # 1) l'image
    t = re.sub(r'<img[^>]*logo-veneta-cucine[^>]*>',
               '<img decoding="async" class="alignnone aligncenter" src="%s" '
               'alt="Forma" width="200" height="179" />' % LOGO, t)
    # 2) le lien qui l'entoure
    t = t.replace('href="https://www.venetacucine.com/"', 'href="%s"' % LIEN)
    t = t.replace('title="Veneta Cucine"', 'title="Forma"')
    t = t.replace('aria-label="Veneta Cucine"', 'aria-label="Forma"')
    t = t.replace('alt="Veneta Cucine"', 'alt="Forma"')

    if t != avant:
        open(P, 'w', encoding='utf-8').write(t)
        print(P, ': Veneta -> Forma')
    else:
        print(P, ': rien a changer')

# 3) le logo Forma est un aplat orange : le passer en gris le denaturerait
import os
ANCIEN = '.post-content img[src*="logo-"]:not([src*="c_line"]),'
NOUVEAU = ('.post-content img[src*="logo-forma"]{filter:none!important;opacity:1!important;'
           'border-radius:6px;}\n'
           '.post-content img[src*="logo-"]:not([src*="c_line"]),')
n = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        if ANCIEN in t and 'logo-forma"]{filter' not in t:
            open(p, 'w', encoding='utf-8').write(t.replace(ANCIEN, NOUVEAU, 1))
            n += 1
print('logo Forma exclu du filtre gris sur %d pages' % n)
