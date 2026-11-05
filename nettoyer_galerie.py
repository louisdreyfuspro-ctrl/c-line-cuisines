#!/usr/bin/env python3
"""Retire de la galerie les photos qui ne sont pas des cuisines a montrer :
photos de famille encadrees, portraits de personnes, photo mal cadree,
cuisine encombree d'effets personnels."""
import os, re, subprocess

A_RETIRER = ['006', '012', '073', '090']
DOSSIER = 'site/wp-content/uploads/2026/11'
POUBELLE = os.path.join(DOSSIER, 'ecartees')
os.makedirs(POUBELLE, exist_ok=True)

for n in A_RETIRER:
    f = os.path.join(DOSSIER, 'cuisine-%s.jpg' % n)
    if os.path.exists(f):
        subprocess.run(['mv', f, os.path.join(POUBELLE, 'cuisine-%s.jpg' % n)])
        print('retiree : cuisine-%s.jpg' % n)

# galerie reconstruite a partir des fichiers restants
restantes = sorted(f for f in os.listdir(DOSSIER) if re.match(r'cuisine-\d+\.jpg$', f))
print('photos conservees :', len(restantes))

def dims(p):
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', p],
                         capture_output=True, text=True).stdout
    w = re.search(r'pixelWidth:\s*(\d+)', out); h = re.search(r'pixelHeight:\s*(\d+)', out)
    return (w.group(1), h.group(1)) if w and h else ('1200', '1600')

vign = []
for f in restantes:
    chemin = '/wp-content/uploads/2026/11/' + f
    w, h = dims(os.path.join(DOSSIER, f))
    vign.append('<a href="%s"><img src="%s" alt="Cuisine réalisée par C-LINE" '
                'width="%s" height="%s" loading="lazy"></a>' % (chemin, chemin, w, h))

P = 'site/cuisine/cuisines/index.html'
t = open(P, encoding='utf-8').read()
t2, k = re.subn(r'(<div class="cline-gc-grille">).*?(</div>)',
                lambda m: m.group(1) + ''.join(vign) + m.group(2), t, flags=re.S)
assert k == 1
open(P, 'w', encoding='utf-8').write(t2)
print('galerie mise a jour')
