#!/usr/bin/env python3
"""Publie plusieurs realisations cuisine + une galerie, sans date affichee."""
import os, re, html, shutil, subprocess

S = '/private/tmp/claude-501/-Users-dreyfus-C-LINE/bfcdd7d9-09a2-40f4-9b9a-bbf5c1a345ee/scratchpad/nouv'
SITE = 'site'
DEST = os.path.join(SITE, 'wp-content/uploads/2026/09')
GABARIT = os.path.join(SITE, 'silence-mineral', 'index.html')

REALISATIONS = [
    dict(slug='cuisine-vert-olive-poutres', titre="Cuisine vert olive sous poutres apparentes",
         photos=['n01', 'n13', 'n45'],
         texte="Un vert olive profond, mat, qui dialogue avec les poutres anciennes et la pierre du "
               "plan de travail. Les façades pleine hauteur cachent les rangements, tandis que l’îlot "
               "central ouvre la cuisine sur la pièce de vie. Une teinte naturelle qui réchauffe "
               "l’ensemble sans jamais l’assombrir."),
    dict(slug='cuisine-anthracite-ilot-marbre', titre="Cuisine anthracite et plan marbré",
         photos=['n22', 'n28'],
         texte="Une cuisine tout en retenue&nbsp;: façades anthracite mates, grand îlot central et plan "
               "de travail marbré aux veines claires. Les suspensions noires alignées au-dessus de l’îlot "
               "prolongent la ligne des colonnes, pour un ensemble graphique et très calme."),
    dict(slug='cuisine-sous-arche-pierre', titre="Cuisine blanche et chêne sous arche en pierre",
         photos=['n46', 'n44', 'n38'],
         texte="Dans cette maison ancienne, l’arche en pierre et le plafond à la française ont été "
               "conservés. La cuisine y répond avec des façades blanches sans poignées et un habillage "
               "en chêne clair, qui adoucit la pierre et fait entrer la lumière jusqu’au fond de la pièce."),
]

GALERIE = ['n04','n05','n08','n09','n16','n18','n19','n24','n25','n26','n29','n33',
           'n34','n37','n39','n41','n43','n50','n51','n53','n54','n56']

def installer(cle, nom):
    src = os.path.join(S, cle + '.jpeg')
    dst = os.path.join(DEST, nom)
    subprocess.run(['sips', '-Z', '1500', '-s', 'formatOptions', '82', src, '--out', dst],
                   capture_output=True)
    return '/wp-content/uploads/2026/09/' + nom

CSS_GAL = ('<style id="cline-galerie-css">'
           '.cline-galerie{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:30px 0 10px;}'
           '.cline-galerie a{display:block;overflow:hidden;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.10);aspect-ratio:4/5;}'
           '.cline-galerie img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease;}'
           '.cline-galerie a:hover img{transform:scale(1.05);}'
           '</style>')

gab = open(GABARIT, encoding='utf-8').read()
cartes = []

for r in REALISATIONS:
    chemins = [installer(c, '%s-%d.jpg' % (r['slug'], i + 1)) for i, c in enumerate(r['photos'])]
    t = gab
    t = t.replace('Silence minéral.', r['titre']).replace('Silence minéral', r['titre'])
    brut = re.sub('&nbsp;|<[^>]+>', ' ', r['texte'])
    t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(brut)[:155]+m.group(2), t, count=1)
    t = re.sub(r'(og:description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(brut)[:200]+m.group(2), t, count=1)
    t = t.replace('/silence-mineral/', '/%s/' % r['slug'])
    t = re.sub(r'(og:image" content=")[^"]*(")', r'\g<1>'+chemins[0]+r'\g<2>', t, count=1)
    gal = ('<div class="cline-galerie">' + ''.join(
        '<a href="%s"><img src="%s" alt="%s" loading="lazy"></a>' % (p, p, r['titre']) for p in chemins) + '</div>')
    m = re.search(r'(<div class="postie-post">)(.*?)(</div>)', t, re.S)
    t = t[:m.start()] + CSS_GAL + m.group(1) + '\n<p>' + r['texte'] + '</p>\n' + gal + '\n' + m.group(3) + t[m.end():]
    os.makedirs(os.path.join(SITE, r['slug']), exist_ok=True)
    open(os.path.join(SITE, r['slug'], 'index.html'), 'w', encoding='utf-8').write(t)
    cartes.append((r['slug'], r['titre'], brut.strip()[:150], chemins))
    print('realisation :', r['slug'], '(%d photos)' % len(chemins))

# galerie de la page Cuisines
gal_chemins = [installer(c, 'galerie-cuisine-%02d.jpg' % (i + 1)) for i, c in enumerate(GALERIE)]
print('galerie :', len(gal_chemins), 'photos')

import json
json.dump({'cartes': cartes, 'galerie': gal_chemins}, open('/tmp/cline_lot.json', 'w'))
