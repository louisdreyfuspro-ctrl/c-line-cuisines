#!/usr/bin/env python3
"""Ajoute width/height aux images des nouvelles cartes : la place est reservee
avant chargement, ce qui evite l'effondrement et le decalage de mise en page."""
import os, re, subprocess

SITE = 'site'
DOSSIER = os.path.join(SITE, 'wp-content/uploads/2026/09')

# dimensions reelles de chaque photo
dims = {}
for f in os.listdir(DOSSIER):
    if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', os.path.join(DOSSIER, f)],
                         capture_output=True, text=True).stdout
    w = re.search(r'pixelWidth:\s*(\d+)', out)
    h = re.search(r'pixelHeight:\s*(\d+)', out)
    if w and h:
        dims['/wp-content/uploads/2026/09/' + f] = (w.group(1), h.group(1))
print(len(dims), 'images mesurees')

n = 0
for racine, _, fichiers in os.walk(SITE):
    for fn in fichiers:
        if not fn.endswith('.html'):
            continue
        p = os.path.join(racine, fn)
        t = open(p, encoding='utf-8', errors='replace').read()
        orig = t
        def ajouter(m):
            balise = m.group(0)
            src = re.search(r'src="([^"]+)"', balise)
            if not src or src.group(1) not in dims:
                return balise
            if re.search(r'\bwidth=', balise):
                return balise
            w, h = dims[src.group(1)]
            return balise[:-1].rstrip('/ ') + ' width="%s" height="%s" />' % (w, h)
        t = re.sub(r'<img[^>]*/wp-content/uploads/2026/09/[^>]*>', ajouter, t)
        if t != orig:
            open(p, 'w', encoding='utf-8').write(t)
            n += 1
print('dimensions ajoutees sur %d page(s)' % n)
