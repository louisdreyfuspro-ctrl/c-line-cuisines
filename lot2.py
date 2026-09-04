#!/usr/bin/env python3
"""Trois nouvelles cuisines identifiees + photos isolees versees a la galerie."""
import os, re, html, json, subprocess

S = '/private/tmp/claude-501/-Users-dreyfus-C-LINE/bfcdd7d9-09a2-40f4-9b9a-bbf5c1a345ee/scratchpad/serie'
SITE = 'site'
DEST = os.path.join(SITE, 'wp-content/uploads/2026/09')
GABARIT = os.path.join(SITE, 'silence-mineral', 'index.html')

REALISATIONS = [
    dict(slug='cuisine-ilot-poutres-parquet-chevrons',
         titre="Cuisine sous charpente et parquet à chevrons",
         photos=['s14', 's8'],
         texte="Sous une charpente apparente et un plafond cathédrale, l’îlot central s’allonge face "
               "à la pièce de vie. Les façades claires et les niches ouvertes allègent le volume, "
               "tandis que le parquet à chevrons et les suspensions dorées réchauffent l’ensemble. "
               "Une cuisine ouverte qui respire, sans jamais écraser l’espace."),
    dict(slug='cuisine-verriere-cintree-mur-vert',
         titre="Cuisine ouverte sur verrière cintrée",
         photos=['s10', 's9', 's16', 's15'],
         texte="Un long îlot en pierre claire fait face à une verrière cintrée qui ouvre la pièce sur "
               "le jardin. Le mur vert profond répond aux menuiseries sombres, les suspensions "
               "en fils métalliques ponctuent la hauteur sous plafond. Cuisine, table et cave à vin "
               "s’enchaînent dans un même geste, pour une pièce à vivre entière."),
    dict(slug='cuisine-ilot-bleu-canard',
         titre="Cuisine bois et îlot bleu canard",
         photos=['s6', 's4'],
         texte="Le bleu canard mat de l’îlot tranche avec le chêne du plan de travail et de la table "
               "haute, dans une pièce largement ouverte sur l’extérieur. Les suspensions noires "
               "alignées au-dessus du bar structurent l’espace et assument le contraste, sans rien "
               "enlever à la chaleur des matières."),
]

GALERIE_SUP = ['s3', 's5', 's7', 's11', 's12']

def installer(cle, nom):
    subprocess.run(['sips', '-Z', '1500', '-s', 'formatOptions', '82',
                    os.path.join(S, cle + '.jpeg'), '--out', os.path.join(DEST, nom)],
                   capture_output=True)
    return '/wp-content/uploads/2026/09/' + nom

CSS_GAL = ('<style id="cline-galerie-css">'
  '.cline-galerie{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:30px 0 10px;}'
  '.cline-galerie a{display:block;overflow:hidden;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.10);aspect-ratio:4/5;}'
  '.cline-galerie img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease;}'
  '.cline-galerie a:hover img{transform:scale(1.05);}</style>')

gab = open(GABARIT, encoding='utf-8').read()
cartes = []
for r in REALISATIONS:
    chemins = [installer(c, '%s-%d.jpg' % (r['slug'], i + 1)) for i, c in enumerate(r['photos'])]
    t = gab.replace('Silence minéral.', r['titre']).replace('Silence minéral', r['titre'])
    brut = re.sub('&nbsp;|<[^>]+>', ' ', r['texte'])
    t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(brut)[:155]+m.group(2), t, count=1)
    t = re.sub(r'(og:description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(brut)[:200]+m.group(2), t, count=1)
    t = t.replace('/silence-mineral/', '/%s/' % r['slug'])
    t = re.sub(r'(og:image" content=")[^"]*(")', r'\g<1>'+chemins[0]+r'\g<2>', t, count=1)
    gal = '<div class="cline-galerie">' + ''.join(
        '<a href="%s"><img src="%s" alt="%s" loading="lazy"></a>' % (p, p, r['titre']) for p in chemins) + '</div>'
    m = re.search(r'(<div class="postie-post">)(.*?)(</div>)', t, re.S)
    t = t[:m.start()] + CSS_GAL + m.group(1) + '\n<p>' + r['texte'] + '</p>\n' + gal + '\n' + m.group(3) + t[m.end():]
    os.makedirs(os.path.join(SITE, r['slug']), exist_ok=True)
    open(os.path.join(SITE, r['slug'], 'index.html'), 'w', encoding='utf-8').write(t)
    cartes.append((r['slug'], r['titre'], brut.strip()[:150], chemins))
    print('%-42s %d photos' % (r['slug'], len(chemins)))

sup = [installer(c, 'galerie-cuisine-%02d.jpg' % (30 + i)) for i, c in enumerate(GALERIE_SUP)]
json.dump({'cartes': cartes, 'galerie_sup': sup}, open('/tmp/cline_lot2.json', 'w'))
print('galerie : +%d photos' % len(sup))
