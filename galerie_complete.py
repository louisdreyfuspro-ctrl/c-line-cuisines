#!/usr/bin/env python3
"""Reconstruit la galerie « Nos cuisines en images » avec toutes les photos."""
import json, re, os, subprocess

d = json.load(open('/tmp/cline_photos.json'))
photos = d['cuisines']

# dimensions pour reserver la place avant chargement
def dims(chemin):
    p = 'site' + chemin
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', p],
                         capture_output=True, text=True).stdout
    w = re.search(r'pixelWidth:\s*(\d+)', out)
    h = re.search(r'pixelHeight:\s*(\d+)', out)
    return (w.group(1), h.group(1)) if w and h else ('1200', '1600')

vignettes = []
for p in photos:
    w, h = dims(p)
    vignettes.append('<a href="%s"><img src="%s" alt="Cuisine réalisée par C-LINE" '
                     'width="%s" height="%s" loading="lazy"></a>' % (p, p, w, h))

P = 'site/cuisine/cuisines/index.html'
t = open(P, encoding='utf-8').read()
t2, k = re.subn(r'(<div class="cline-gc-grille">).*?(</div>)',
                lambda m: m.group(1) + ''.join(vignettes) + m.group(2), t, flags=re.S)
assert k == 1, 'galerie introuvable'

# sous-titre mis a jour
t2 = re.sub(r'(<p>Un aper&ccedil;u de nos r&eacute;alisations).*?(</p>)',
            lambda m: '<p>L&rsquo;ensemble de nos r&eacute;alisations&nbsp;: mati&egrave;res, '
                      'teintes et implantations, du plus &eacute;pur&eacute; au plus chaleureux.</p>',
            t2, count=1, flags=re.S)
open(P, 'w', encoding='utf-8').write(t2)
print('galerie reconstruite :', len(vignettes), 'photos')
