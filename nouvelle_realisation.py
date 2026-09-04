#!/usr/bin/env python3
"""Cree la realisation « Renovation entree + cuisine » a partir du gabarit d'un article existant."""
import os, re, html

SITE = 'site'
SLUG = 'renovation-entree-cuisine-lumiere'
TITRE = "Rénovation d’un espace entrée et cuisine"
GABARIT = os.path.join(SITE, 'silence-mineral', 'index.html')

TEXTE = ("Une très belle rénovation menée en collaboration avec AG Concept. "
         "L’espace d’entrée s’ouvre sur la cuisine dans une continuité parfaite&nbsp;: façades blanches "
         "sans poignées, plan de travail et îlot habillés de chêne, soulignés par un fin liseré noir "
         "qui dessine les volumes sans les alourdir. "
         "Tout repose ici sur un beau travail de lumière&nbsp;— éclairages intégrés sous les meubles, "
         "ligne lumineuse au plafond et suspensions dorées au-dessus de l’îlot&nbsp;— qui réchauffe "
         "les teintes claires et donne à l’ensemble sa douceur.")

PHOTOS = ['/wp-content/uploads/2026/09/reno-agconcept-%d.jpg' % i for i in range(1, 6)]

t = open(GABARIT, encoding='utf-8').read()

# --- titres et metadonnees ---
t = t.replace('Silence minéral.', TITRE)
t = t.replace('Silence minéral', TITRE)
t = re.sub(r'(<meta name="description" content=")[^"]*(")',
           lambda m: m.group(1) + html.escape(re.sub('&nbsp;|<[^>]+>', ' ', TEXTE))[:155] + m.group(2), t, count=1)
t = re.sub(r'(og:description" content=")[^"]*(")',
           lambda m: m.group(1) + html.escape(re.sub('&nbsp;|<[^>]+>', ' ', TEXTE))[:200] + m.group(2), t, count=1)
t = t.replace('/silence-mineral/', '/%s/' % SLUG)
t = re.sub(r'(og:image" content=")[^"]*(")', r'\g<1>' + PHOTOS[0] + r'\g<2>', t, count=1)

# --- corps de l'article : texte + galerie ---
GALERIE = ('<div class="cline-galerie">' +
           ''.join('<a href="%s"><img src="%s" alt="%s" loading="lazy"></a>' % (p, p, TITRE) for p in PHOTOS) +
           '</div>')
CSS = ('<style id="cline-galerie-css">'
       '.cline-galerie{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:30px 0 10px;}'
       '.cline-galerie a{display:block;overflow:hidden;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.10);aspect-ratio:4/5;}'
       '.cline-galerie img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease;}'
       '.cline-galerie a:hover img{transform:scale(1.05);}'
       '</style>')
m = re.search(r'(<div class="postie-post">)(.*?)(</div>)', t, re.S)
assert m, 'corps introuvable'
t = t[:m.start()] + CSS + m.group(1) + '\n<p>' + TEXTE + '</p>\n' + GALERIE + '\n' + m.group(3) + t[m.end():]

dossier = os.path.join(SITE, SLUG)
os.makedirs(dossier, exist_ok=True)
open(os.path.join(dossier, 'index.html'), 'w', encoding='utf-8').write(t)
print('page creee :', dossier + '/index.html')
print('  photos   :', len(PHOTOS))
