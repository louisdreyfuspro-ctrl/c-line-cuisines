#!/usr/bin/env python3
"""Reinsere les nouvelles realisations en clonant la carte existante de chaque page,
pour que la mise en page soit strictement identique (timeline ou grille selon la page)."""
import json, re, os

d = json.load(open('/tmp/cline_lot.json'))
NOUVELLES = [(s, ti, ex, ph) for s, ti, ex, ph in d['cartes']]
NOUVELLES.append(('renovation-entree-cuisine-lumiere',
                  "Rénovation d’un espace entrée et cuisine",
                  "Une très belle rénovation menée en collaboration avec AG Concept. L’espace d’entrée "
                  "s’ouvre sur la cuisine dans une continuité parfaite, portée par un beau travail de lumière.",
                  ['/wp-content/uploads/2026/09/reno-agconcept-%d.jpg' % i for i in range(1, 6)]))

SLUGS = [s for s, _, _, _ in NOUVELLES]
CIBLES = ['site/index.html', 'site/cuisine/realisations/index.html', 'site/cuisine/cuisines/index.html']

def retirer_mes_cartes(t):
    n = 0
    for slug in SLUGS:
        while True:
            i = t.find('/%s/' % slug)
            if i < 0:
                break
            d0 = t.rfind('<article', 0, i)
            f0 = t.find('</article>', i)
            if d0 < 0 or f0 < 0:
                break
            t = t[:d0] + t[f0 + len('</article>'):]
            n += 1
    return t, n

def cloner(gabarit, slug, titre, extrait, photos):
    c = gabarit
    # 1) slug : tous les liens de la carte
    c = re.sub(r'href="/[a-z0-9\-]+/"', 'href="/%s/"' % slug, c)
    # 2) diapositives : on reconstruit la liste avec nos photos
    slides = ''.join(
        '<li><div class="fusion-image-wrapper" aria-haspopup="true">'
        '<a href="/%s/" aria-label="%s">'
        '<img src="%s" class="attachment-full size-full wp-post-image" alt="%s" '
        'decoding="async" loading="lazy" /></a></div></li>' % (slug, titre, p, titre)
        for p in photos)
    c = re.sub(r'(<ul class="slides">).*?(</ul>)', lambda m: m.group(1) + slides + m.group(2), c, flags=re.S)
    # 3) titre
    c = re.sub(r'(<h2[^>]*entry-title[^>]*>\s*<a[^>]*>).*?(</a>)', lambda m: m.group(1) + titre + m.group(2), c, flags=re.S)
    c = re.sub(r'(aria-label=")[^"]*(")', lambda m: m.group(1) + titre + m.group(2), c)
    # 4) extrait
    c = re.sub(r'(<div class="fusion-post-content-container">).*?(</div>)',
               lambda m: m.group(1) + '<p>' + extrait + '</p>' + m.group(2), c, flags=re.S)
    # 5) identifiants uniques
    c = re.sub(r'id="[^"]*post-\d+"', 'id="post-%d"' % (abs(hash(slug)) % 100000), c)
    return c

for chemin in CIBLES:
    t = open(chemin, encoding='utf-8').read()
    t, retires = retirer_mes_cartes(t)

    # gabarit = premiere carte restante de la page
    m = re.search(r'<article[^>]*class="[^"]*fusion-post-(?:timeline|grid)[^"]*"', t)
    if not m:
        print(chemin, ': aucune carte gabarit'); continue
    fin = t.find('</article>', m.start()) + len('</article>')
    gabarit = t[m.start():fin]

    bloc = ''.join(cloner(gabarit, s, ti, ex, ph) for s, ti, ex, ph in NOUVELLES)
    t = t[:m.start()] + bloc + t[m.start():]
    open(chemin, 'w', encoding='utf-8').write(t)
    layout = 'timeline' if 'fusion-post-timeline' in gabarit else 'grille'
    print('%-42s %d retirees, %d clonees (%s)' % (chemin, retires, len(NOUVELLES), layout))
