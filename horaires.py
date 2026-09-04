#!/usr/bin/env python3
"""Mise a jour des horaires d'ouverture sur tout le site.
Lundi sur rendez-vous | Mardi-vendredi 9h30-12h / 14h30-19h | Samedi 9h30-12h / 14h30-18h
"""
import os

# 1) Description Google (176 pages) + phrase d'accroche de la page contact
GLOBAL = [
    ("notre show-room de 200 m2 vous accueille du lundi au samedi, de 9h à 19h",
     "notre show-room de 200 m2 vous accueille du mardi au samedi, le lundi sur rendez-vous"),
    ("200&nbsp;m&sup2; de showroom vous attendent, du lundi au samedi.",
     "200&nbsp;m&sup2; de showroom vous attendent, du mardi au samedi &mdash; et le lundi sur rendez-vous."),
]

# 2) Bloc horaires detaille de la page contact
DETAIL = (
    "<span>Du lundi au samedi<br>9h &ndash; 19h</span>",
    "<span><strong>Lundi</strong>&nbsp;: sur rendez-vous<br>"
    "<strong>Mardi &agrave; vendredi</strong>&nbsp;: 9h30&ndash;12h / 14h30&ndash;19h<br>"
    "<strong>Samedi</strong>&nbsp;: 9h30&ndash;12h / 14h30&ndash;18h</span>"
)

n_pages = n_remplacements = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        orig = t
        for vieux, neuf in GLOBAL:
            if vieux in t:
                n_remplacements += t.count(vieux)
                t = t.replace(vieux, neuf)
        if DETAIL[0] in t:
            t = t.replace(DETAIL[0], DETAIL[1])
            n_remplacements += 1
        if t != orig:
            open(p, 'w', encoding='utf-8').write(t)
            n_pages += 1

print("%d remplacements sur %d pages" % (n_remplacements, n_pages))
