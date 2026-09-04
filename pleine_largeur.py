#!/usr/bin/env python3
"""Etend les sections d'animation scroll sur toute la largeur de la page.
On mesure le decalage reel a l'execution plutot que d'utiliser 100vw
(qui deborderait de la largeur de la barre de defilement) et sans overflow:hidden
(qui casserait le position:sticky)."""
import os, re

BLOC = '''
<script id="cline-pleine-largeur">
(function(){
  var SEL='.cline-visite,.cline-exp';
  function etendre(){
    document.querySelectorAll(SEL).forEach(function(s){
      s.style.marginLeft='0px';s.style.marginRight='0px';
      var r=s.getBoundingClientRect(), dispo=document.documentElement.clientWidth;
      var g=Math.round(r.left), d=Math.round(dispo-r.right);
      if(g>0)s.style.marginLeft=(-g)+'px';
      if(d>0)s.style.marginRight=(-d)+'px';
    });
  }
  window.addEventListener('load',etendre);
  window.addEventListener('resize',etendre,{passive:true});
  if(document.readyState!=='loading')etendre();
  else document.addEventListener('DOMContentLoaded',etendre);
})();
</script>
'''

n = 0
for racine, _, fichiers in os.walk('site'):
    for f in fichiers:
        if not f.endswith('.html'):
            continue
        p = os.path.join(racine, f)
        t = open(p, encoding='utf-8', errors='replace').read()
        if 'cline-pleine-largeur' in t:
            continue
        if 'cline-visite' not in t and 'cline-exp-' not in t:
            continue
        if '</body>' not in t:
            continue
        t = t.replace('</body>', BLOC + '</body>', 1)
        open(p, 'w', encoding='utf-8').write(t)
        n += 1
print('sections etendues sur %d page(s)' % n)
