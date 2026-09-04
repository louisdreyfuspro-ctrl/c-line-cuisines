#!/usr/bin/env python3
"""Ajoute « Qui sommes-nous » au menu, juste avant Contact, sur toutes les pages."""
import os, re

ENTREE = ('<li id="menu-item-9100" class="menu-item menu-item-type-post_type menu-item-object-page '
          'menu-item-9100" data-item-id="9100"><a href="/qui-sommes-nous/" class="fusion-bar-highlight">'
          '<span class="menu-text">Qui sommes-nous</span></a></li>')

# on cible l'element de menu « Contact » et on insere juste avant
MOTIF = re.compile(r'(<li[^>]*menu-item[^>]*>\s*<a[^>]*href="/cuisine/contact/"[^>]*>.*?</li>)', re.S)

n = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        if '/qui-sommes-nous/' in t and 'menu-item-9100' in t:
            continue
        t2, k = MOTIF.subn(lambda m: ENTREE + m.group(1), t)
        if k:
            open(p, 'w', encoding='utf-8').write(t2)
            n += 1
print('entree de menu ajoutee sur %d pages (%d occurrences par page en moyenne)' % (n, k if n else 0))
