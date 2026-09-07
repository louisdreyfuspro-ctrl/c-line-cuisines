#!/usr/bin/env python3
"""Supprime le script malveillant injecte en base64 (balise id="_ea_s").
Charge du code obfusque qui affiche une fausse reCAPTCHA et empoisonne le presse-papier."""
import os, re

MOTIFS = [
    re.compile(r'<script[^>]*id="_ea_s"[^>]*>\s*</script>', re.I),
    re.compile(r'<script[^>]*id="_ea_s"[^>]*/?>', re.I),
    re.compile(r'<script[^>]*src="data:text/javascript;base64,[A-Za-z0-9+/=]+"[^>]*>\s*</script>', re.I),
    re.compile(r'<script[^>]*src="data:text/javascript;base64,[A-Za-z0-9+/=]+"[^>]*/?>', re.I),
]

n_pages = n_balises = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        orig = t
        for motif in MOTIFS:
            t, k = motif.subn('', t)
            n_balises += k
        if t != orig:
            open(p, 'w', encoding='utf-8').write(t)
            n_pages += 1
print('%d balises supprimees sur %d pages' % (n_balises, n_pages))
