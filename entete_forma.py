#!/usr/bin/env python3
"""Remplace les visuels de l'en-tete de la page Cuisines par des photos Forma.
On conserve les noms de fichiers et les proportions : le slider continue de
fonctionner sans toucher au balisage."""
import subprocess, os
from PIL import Image

S = '/private/tmp/claude-501/-Users-dreyfus-C-LINE/bfcdd7d9-09a2-40f4-9b9a-bbf5c1a345ee/scratchpad/forma'
D = 'site/wp-content/uploads/2015/11'

# sauvegarde des visuels d'origine
SAUV = 'site/wp-content/uploads/2026/11/anciens-entete'
os.makedirs(SAUV, exist_ok=True)

REMPL = [
    ('f1.jpg', 'BD-CUISINE-03',  (1923, 636)),
    ('f3.jpg', 'BD-CUISINE-041', (1834, 646)),
    ('f8.jpg', 'BD-CUISINE-08',  (2398, 874)),
]

for src, cible, (lw, lh) in REMPL:
    chemin_src = os.path.join(S, src)
    chemin_cible = os.path.join(D, cible + '.jpg')
    # sauvegarde
    if os.path.exists(chemin_cible):
        subprocess.run(['cp', chemin_cible, os.path.join(SAUV, cible + '.jpg')])
    im = Image.open(chemin_src).convert('RGB')
    # recadrage au bon rapport puis redimensionnement
    rapport = lw / lh
    w, h = im.size
    if w / h > rapport:
        nw = int(h * rapport)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / rapport)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((lw, lh), Image.LANCZOS)
    im.save(chemin_cible, quality=86, optimize=True)
    # vignette du slider
    vign = os.path.join(D, cible + '-100x50.jpg')
    if os.path.exists(vign):
        im.resize((100, 50), Image.LANCZOS).save(vign, quality=85)
    print('%-16s <- %s  %dx%d' % (cible, src, lw, lh))
print('anciens visuels sauvegardes dans', SAUV)
