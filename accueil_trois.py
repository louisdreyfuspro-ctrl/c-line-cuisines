#!/usr/bin/env python3
"""Accueil : ne garder que 3 realisations en vitrine + un lien vers la page complete."""
import re

P = 'site/index.html'
t = open(P, encoding='utf-8').read()

# reperer tous les articles de la grille
bornes = []
for m in re.finditer(r'<article[^>]*class="[^"]*fusion-post-grid[^"]*"', t):
    debut = m.start()
    fin = t.find('</article>', debut) + len('</article>')
    bornes.append((debut, fin))
print('articles trouves :', len(bornes))
assert len(bornes) > 3, 'rien a retirer'

# retirer du dernier vers le premier pour ne pas decaler les index
retires = 0
for debut, fin in reversed(bornes[3:]):
    t = t[:debut] + t[fin:]
    retires += 1
print('articles retires :', retires)

# bouton vers toutes les realisations, apres la grille
if 'cline-voir-tout' not in t:
    BOUTON = ('<div class="cline-voir-tout">'
      '<style>'
      '.cline-voir-tout{text-align:center;padding:6px 30px 54px;background:transparent;}'
      '.cline-voir-tout a{display:inline-block;padding:14px 38px;border-radius:40px;'
      'background:#22211f;color:#fff!important;text-decoration:none;font-size:13px;font-weight:600;'
      'letter-spacing:1.5px;text-transform:uppercase;transition:background-color .22s,transform .22s,box-shadow .22s;}'
      '.cline-voir-tout a:hover{background:#c9985f;transform:translateY(-2px);box-shadow:0 9px 22px rgba(201,152,95,.35);}'
      '</style>'
      '<a href="/cuisine/realisations/">Voir toutes nos r&eacute;alisations</a></div>')
    # juste apres la fin de la grille (fin du 3e article conserve)
    dernier = bornes[2][1]
    # l'index reste valable : on n'a supprime que ce qui suit
    ferme = t.find('</div>', dernier)
    point = t.find('</section>', dernier)
    insertion = point if point > 0 else dernier
    t = t[:insertion] + BOUTON + t[insertion:]
    print('bouton « voir toutes nos realisations » ajoute')

open(P, 'w', encoding='utf-8').write(t)
