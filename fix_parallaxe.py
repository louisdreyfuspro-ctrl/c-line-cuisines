#!/usr/bin/env python3
"""Exclut les en-tetes porteurs de texte de l'effet de parallaxe :
le deplacement continu de l'image rendait le titre bancal et illisible."""
import os

ANCIEN = """    var secs=[].slice.call(document.querySelectorAll('.fusion-fullwidth')).filter(function(s){
      var st=s.getAttribute('style')||'';
      return st.indexOf('background-image')>-1 && st.indexOf('cover')>-1 && s.offsetHeight>180 && s.offsetHeight<window.innerHeight*1.6;
    });"""

NOUVEAU = """    var secs=[].slice.call(document.querySelectorAll('.fusion-fullwidth')).filter(function(s){
      var st=s.getAttribute('style')||'';
      /* on laisse tranquilles les en-tetes qui portent du texte : le deplacement
         de l'image les rendrait bancals et illisibles */
      if(s.querySelector('.cline-hero-contact,.cline-qsn-hero,h1'))return false;
      return st.indexOf('background-image')>-1 && st.indexOf('cover')>-1 && s.offsetHeight>180 && s.offsetHeight<window.innerHeight*1.6;
    });"""

n = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        if ANCIEN in t:
            open(p, 'w', encoding='utf-8').write(t.replace(ANCIEN, NOUVEAU, 1))
            n += 1
print('parallaxe ajustee sur %d pages' % n)
