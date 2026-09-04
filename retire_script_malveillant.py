#!/usr/bin/env python3
"""Retire le script tiers vpsstatistic.com injecte dans toutes les pages.
Signature de compromission : charge depuis un domaine tiers, avec des attributs
concus pour echapper aux plugins d'optimisation (data-nowprocket, data-noptimize,
data-cfasync=false, data-no-defer)."""
import os, re

RE = re.compile(r'<script[^>]*vpsstatistic[^>]*>\s*</script>|<script[^>]*vpsstatistic[^>]*/?>', re.I)

n_pages = n_balises = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        t2, k = RE.subn('', t)
        if k:
            open(p, 'w', encoding='utf-8').write(t2)
            n_pages += 1
            n_balises += k
print('%d balises retirees sur %d pages' % (n_balises, n_pages))
