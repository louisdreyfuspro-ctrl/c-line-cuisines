#!/usr/bin/env python3
"""1) Bandeau « Nos partenaires » (Forma + Nolte) sous le titre CUISINES
   2) Page Salles de bain : visuel de section renouvele + galerie d'ambiances Ideagroup"""
import re

# ---------- 1) Bandeau partenaires ----------
PARTENAIRES = [
    ('Forma', '/wp-content/uploads/2026/09/logo-forma-cucine.jpg', 'https://formalacucina.fr/',
     'Cuisines italiennes &mdash; groupe Veneta Cucine'),
    ('Nolte', '/wp-content/uploads/2015/09/logo-nolte-hd2.jpg', 'https://www.nolte-kuechen.com/',
     'Mobilier de cuisine allemand'),
]

BANDEAU = ('<div class="cline-partenaires">'
  '<style>'
  '.cline-partenaires{padding:52px 30px 58px;background:#fbfaf8;border-bottom:1px solid #efece8;}'
  '.cline-pt-inner{max-width:980px;margin:0 auto;text-align:center;}'
  '.cline-pt-sur{display:block;font-size:11.5px;letter-spacing:3.2px;text-transform:uppercase;color:#a8a29c;margin-bottom:6px;}'
  '.cline-pt-inner h2{margin:0 0 30px;font-size:clamp(21px,2.3vw,30px);color:#2b2b2b;letter-spacing:.3px;}'
  '.cline-pt-grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px;}'
  '.cline-pt-carte{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;'
  'padding:30px 24px;background:#fff;border:1px solid #eeebe7;border-radius:11px;text-decoration:none;'
  'transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;}'
  '.cline-pt-carte:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(0,0,0,.10);border-color:#e0d8cd;}'
  '.cline-pt-carte img{max-height:64px;width:auto;object-fit:contain;border-radius:5px;}'
  '.cline-pt-carte span{font-size:13px;color:#8a847e;line-height:1.5;letter-spacing:.2px;}'
  '</style>'
  '<div class="cline-pt-inner"><span class="cline-pt-sur">Nos partenaires</span>'
  '<h2>Les marques que nous avons sélectionnées</h2>'
  '<div class="cline-pt-grille">' +
  ''.join('<a class="cline-pt-carte" href="%s" target="_blank" rel="noopener noreferrer" title="%s">'
          '<img src="%s" alt="%s" loading="lazy"><span>%s</span></a>' % (lien, nom, logo, nom, desc)
          for nom, logo, lien, desc in PARTENAIRES) +
  '</div></div></div>')

P = 'site/cuisine/cuisines/index.html'
t = open(P, encoding='utf-8').read()
if 'cline-partenaires' in t:
    print('bandeau partenaires : deja present')
else:
    # juste apres la bande de titre CUISINES (row-2)
    m = re.search(r'<div class="fusion-fullwidth fullwidth-box fusion-builder-row-3', t)
    assert m, 'section suivante introuvable'
    t = t[:m.start()] + BANDEAU + t[m.start():]
    open(P, 'w', encoding='utf-8').write(t)
    print('bandeau partenaires insere sous le titre CUISINES')

# ---------- 2) Page Salles de bain ----------
P2 = 'site/cuisine/salles-de-bain/index.html'
t2 = open(P2, encoding='utf-8').read()

# visuel de section : remplacer la photo de 2015 par une actuelle
avant = t2
t2 = t2.replace('/wp-content/uploads/2015/09/ideagroup_sense_04-1024x726-01-1024x726.jpg',
                '/wp-content/uploads/2026/09/sdb-ambiance-3.jpg')
print('visuel de section renouvele :', avant != t2)

# galerie d'ambiances
if 'cline-galerie-sdb' not in t2:
    photos = ['/wp-content/uploads/2026/09/sdb-ambiance-%d.jpg' % i for i in range(1, 7)]
    GAL = ('<div class="cline-galerie-sdb">'
      '<style>'
      '.cline-galerie-sdb{padding:60px 30px 70px;background:#fff;}'
      '.cline-gs-inner{max-width:1180px;margin:0 auto;}'
      '.cline-gs-tete{text-align:center;margin-bottom:34px;}'
      '.cline-gs-tete p{color:#8a8580;margin:8px auto 0;font-size:15px;max-width:620px;line-height:1.7;}'
      '.cline-gs-grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;}'
      '.cline-gs-grille a{display:block;overflow:hidden;border-radius:8px;aspect-ratio:3/2;box-shadow:0 4px 16px rgba(0,0,0,.10);}'
      '.cline-gs-grille img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease;}'
      '.cline-gs-grille a:hover img{transform:scale(1.05);}'
      '.cline-gs-note{text-align:center;margin:18px 0 0;font-size:11.5px;color:#a8a29c;}'
      '</style>'
      '<div class="cline-gs-inner"><div class="cline-gs-tete">'
      '<div class="fusion-text"><h1>Ambiances salle de bain</h1></div>'
      '<p>Meubles suspendus, vasques, miroirs r&eacute;troéclair&eacute;s et espaces buanderie&nbsp;: '
      'un aper&ccedil;u des possibilit&eacute;s, &agrave; composer avec vous en showroom.</p></div>'
      '<div class="cline-gs-grille">' +
      ''.join('<a href="%s"><img src="%s" alt="Ambiance salle de bain Ideagroup" '
              'width="900" height="600" loading="lazy"></a>' % (p, p) for p in photos) +
      '</div><p class="cline-gs-note">Visuels Ideagroup.</p></div></div>')
    i = t2.find('</main>')
    assert i > 0, 'fin de contenu introuvable'
    i += len('</main>')
    t2 = t2[:i] + GAL + t2[i:]
    print('galerie ambiances inseree : 6 photos')
open(P2, 'w', encoding='utf-8').write(t2)
