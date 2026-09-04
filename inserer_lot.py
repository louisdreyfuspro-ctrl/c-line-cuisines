#!/usr/bin/env python3
"""Insere les cartes des nouvelles realisations et la galerie de la page Cuisines."""
import json, re, os

d = json.load(open('/tmp/cline_lot.json'))

def carte(slug, titre, extrait, photos):
    diapos = ''.join(
        '<li><div class="fusion-image-wrapper" aria-haspopup="true">'
        '<a href="/%s/" aria-label="%s">'
        '<img decoding="async" src="%s" class="attachment-full size-full wp-post-image" alt="%s" loading="lazy" />'
        '</a></div></li>' % (slug, titre, p, titre) for p in photos)
    return ('<article class="fusion-post-grid post type-post status-publish format-standard '
            'has-post-thumbnail hentry category-cuisines category-nos-realisations">'
            '<div class="fusion-post-wrapper" style="background-color:rgba(255,255,255,0);border:1px solid #ebeaea;border-bottom-width:3px;">'
            '<div class="fusion-flexslider flexslider fusion-flexslider-loading fusion-post-slideshow" style="border-color:#ebeaea;">'
            '<ul class="slides">%s</ul></div>'
            '<div class="fusion-post-content-wrapper"><div class="fusion-post-content post-content">'
            '<h2 class="blog-shortcode-post-title entry-title"><a href="/%s/">%s</a></h2>'
            '<div class="fusion-post-content-container"><p>%s</p></div>'
            '</div></div><div class="fusion-clearfix"></div></div></article>'
            % (diapos, slug, titre, extrait))

CIBLES = ['site/index.html', 'site/cuisine/realisations/index.html', 'site/cuisine/cuisines/index.html']
for chemin in CIBLES:
    t = open(chemin, encoding='utf-8').read()
    m = re.search(r'<article[^>]*class="[^"]*fusion-post-(?:grid|timeline)[^"]*"', t)
    if not m:
        print(chemin, ': grille introuvable'); continue
    bloc = ''
    for slug, titre, extrait, photos in d['cartes']:
        if slug in t:
            continue
        bloc += carte(slug, titre, extrait, photos)
    if bloc:
        t = t[:m.start()] + bloc + t[m.start():]
        open(chemin, 'w', encoding='utf-8').write(t)
        print(chemin, ':', len(d['cartes']), 'cartes ajoutees')
    else:
        print(chemin, ': deja a jour')

# --- galerie sur la page Cuisines ---
P = 'site/cuisine/cuisines/index.html'
t = open(P, encoding='utf-8').read()
if 'cline-galerie-cuisines' not in t:
    vignettes = ''.join('<a href="%s"><img src="%s" alt="Cuisine réalisée par C-LINE" loading="lazy"></a>' % (p, p)
                        for p in d['galerie'])
    SECTION = ('<div class="cline-galerie-cuisines">'
               '<style>'
               '.cline-galerie-cuisines{padding:60px 30px 70px;background:#fff;}'
               '.cline-gc-inner{max-width:1180px;margin:0 auto;}'
               '.cline-gc-tete{text-align:center;margin-bottom:34px;}'
               '.cline-gc-tete p{color:#8a8580;margin:8px auto 0;font-size:15px;max-width:600px;line-height:1.7;}'
               '.cline-gc-grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;}'
               '.cline-gc-grille a{display:block;overflow:hidden;border-radius:7px;aspect-ratio:1/1;box-shadow:0 3px 12px rgba(0,0,0,.09);}'
               '.cline-gc-grille img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease;}'
               '.cline-gc-grille a:hover img{transform:scale(1.06);}'
               '</style>'
               '<div class="cline-gc-inner"><div class="cline-gc-tete">'
               '<div class="fusion-text"><h1>Nos cuisines en images</h1></div>'
               '<p>Un aperçu de nos réalisations&nbsp;: matières, teintes et implantations, '
               'du plus épuré au plus chaleureux.</p></div>'
               '<div class="cline-gc-grille">' + vignettes + '</div></div></div>')
    m = re.search(r'<div[^>]*class="fusion-footer"[^>]*>', t)
    assert m, 'pied de page introuvable'
    t = t[:m.start()] + SECTION + t[m.start():]
    open(P, 'w', encoding='utf-8').write(t)
    print('galerie inseree :', len(d['galerie']), 'photos')
else:
    print('galerie deja presente')
