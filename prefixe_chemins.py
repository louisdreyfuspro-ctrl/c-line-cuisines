#!/usr/bin/env python3
"""Prefixe les chemins absolus du site pour un hebergement en sous-dossier
(ex. GitHub Pages : https://user.github.io/<repo>/).
Usage : python3 prefixe_chemins.py <dossier> <prefixe>
"""
import os, re, sys

RACINE = sys.argv[1]
P = '/' + sys.argv[2].strip('/')

# NB : srcset / data-srcset sont traites a part (valeurs multiples separees par des virgules)
ATTRS = ['src', 'href', 'poster', 'action', 'content',
         'data-rocket-src', 'data-thumb', 'data-lazyload', 'data-bg', 'data-src']

# attribut="/..."  ->  attribut="P/..."   (on ne touche pas aux URL externes ni aux ancres)
RE_ATTR = re.compile(r'\b(' + '|'.join(map(re.escape, ATTRS)) + r')="(/(?!/)[^"]*)"')
# srcset : entrees supplementaires apres une virgule
RE_SRCSET = re.compile(r'\b(srcset|data-srcset)="([^"]*)"')
# url(...) en CSS et dans les styles en ligne (guillemets HTML echappes compris)
RE_URL = re.compile(r'url\((\s*(?:&quot;|["\'])?)(/(?!/)[^)"\'&]*)')
# chemins cites dans les scripts en ligne
RE_JS = re.compile(r"(['\"])(/wp-content/[^'\"]*)\1")

def prefixe_srcset(valeur):
    sorties = []
    for part in valeur.split(','):
        p = part.strip()
        if p.startswith('/') and not p.startswith('//'):
            p = P + p
        sorties.append(p)
    return ', '.join(sorties)

def traite(texte, est_css):
    if est_css:
        return RE_URL.sub(lambda m: 'url(' + m.group(1) + P + m.group(2), texte)
    texte = RE_SRCSET.sub(lambda m: '%s="%s"' % (m.group(1), prefixe_srcset(m.group(2))), texte)
    texte = RE_ATTR.sub(lambda m: '%s="%s%s"' % (m.group(1), P, m.group(2)), texte)
    texte = RE_URL.sub(lambda m: 'url(' + m.group(1) + P + m.group(2), texte)
    texte = RE_JS.sub(lambda m: '%s%s%s%s' % (m.group(1), P, m.group(2), m.group(1)), texte)
    return texte

n = 0
for racine, _, fichiers in os.walk(RACINE):
    for f in fichiers:
        ext = f.rsplit('.', 1)[-1].lower()
        if ext not in ('html', 'css'):
            continue
        chemin = os.path.join(racine, f)
        t = open(chemin, encoding='utf-8', errors='replace').read()
        t2 = traite(t, ext == 'css')
        if t2 != t:
            open(chemin, 'w', encoding='utf-8').write(t2)
            n += 1
print('%d fichiers prefixes avec %s' % (n, P))
