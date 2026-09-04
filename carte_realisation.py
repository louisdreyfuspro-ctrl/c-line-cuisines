#!/usr/bin/env python3
"""Insere la nouvelle realisation en tete des grilles « dernieres realisations »."""
import re, os

SLUG = 'renovation-entree-cuisine-lumiere'
TITRE = "Rénovation d’un espace entrée et cuisine"
EXTRAIT = ("Une très belle rénovation menée en collaboration avec AG Concept. L’espace d’entrée "
           "s’ouvre sur la cuisine dans une continuité parfaite, portée par un beau travail de lumière.")
PHOTOS = ['/wp-content/uploads/2026/09/reno-agconcept-%d.jpg' % i for i in range(1, 6)]

def carte(prefixe_id):
    diapos = ''.join(
        '<li><div class="fusion-image-wrapper" aria-haspopup="true">'
        '<a href="/%s/" aria-label="%s">'
        '<img decoding="async" src="%s" class="attachment-full size-full wp-post-image" alt="%s" loading="lazy" />'
        '</a></div></li>' % (SLUG, TITRE, p, TITRE) for p in PHOTOS)
    return (
      '<article id="%s-post-9001" class="fusion-post-grid post-9001 post type-post status-publish '
      'format-standard has-post-thumbnail hentry category-cuisines category-nos-realisations '
      'category-nos-realisations-2 tag-c-line-cuisines-a-tassin-la-demi-lune tag-cuisines-lyon">'
      '<div class="fusion-post-wrapper" style="background-color:rgba(255,255,255,0);border:1px solid #ebeaea;border-bottom-width:3px;">'
      '<div class="fusion-flexslider flexslider fusion-flexslider-loading fusion-post-slideshow" style="border-color:#ebeaea;">'
      '<ul class="slides">%s</ul></div>'
      '<div class="fusion-post-content-wrapper">'
      '<div class="fusion-post-content post-content">'
      '<h2 class="blog-shortcode-post-title entry-title"><a href="/%s/">%s</a></h2>'
      '<div class="fusion-post-content-container"><p>%s</p></div>'
      '</div></div>'
      '<div class="fusion-clearfix"></div></div></article>'
      % (prefixe_id, diapos, SLUG, TITRE, EXTRAIT))

CIBLES = [
    ('site/index.html', 'blog-1'),
    ('site/cuisine/realisations/index.html', 'blog-1'),
    ('site/cuisine/cuisines/index.html', 'blog-1'),
]

for chemin, prefixe in CIBLES:
    if not os.path.exists(chemin):
        print('absent :', chemin); continue
    t = open(chemin, encoding='utf-8').read()
    if SLUG in t:
        print(chemin, ': deja present'); continue
    m = re.search(r'<article[^>]*class="[^"]*fusion-post-(?:grid|timeline)[^"]*"', t)
    if not m:
        print(chemin, ': aucune grille trouvee'); continue
    t = t[:m.start()] + carte(prefixe) + t[m.start():]
    open(chemin, 'w', encoding='utf-8').write(t)
    print(chemin, ': carte inseree en tete')
