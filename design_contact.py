#!/usr/bin/env python3
"""Refonte moderne du bloc contact : un seul panneau en deux volets."""
import re

P = 'site/cuisine/contact/index.html'
t = open(P, encoding='utf-8').read()

ICO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">')

BLOC = f'''<div class="cline-contact2">
<div class="cline-contact2-carte">

  <aside class="cline-c2-info">
    <div class="cline-c2-info-haut">
      <span class="cline-c2-sur">Parlons-en</span>
      <h2>Un projet en t&ecirc;te&nbsp;?</h2>
      <p class="cline-c2-intro">&Eacute;crivez-nous, passez au show-room ou appelez-nous&nbsp;:
         nous prenons le temps qu&rsquo;il faut pour comprendre ce que vous imaginez.</p>
    </div>
    <ul class="cline-c2-liste">
      <li>{ICO}<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
        <span><strong>209 Av Charles de Gaulle</strong>69160 Tassin-La-Demi-Lune</span></li>
      <li>{ICO}<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.7a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>
        <span><a href="tel:+33478476951"><strong>04 78 47 69 51</strong></a>Du mardi au samedi</span></li>
      <li>{ICO}<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>
        <span><a href="mailto:corinne@c-line-cuisines.com"><strong>corinne@c-line-cuisines.com</strong></a>R&eacute;ponse sous 48&nbsp;h ouvr&eacute;es</span></li>
      <li>{ICO}<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
        <span><strong>Horaires</strong>Lundi&nbsp;: sur rendez-vous<br>Mardi &agrave; vendredi&nbsp;: 9h30&ndash;12h / 14h30&ndash;19h<br>Samedi&nbsp;: 9h30&ndash;12h / 14h30&ndash;18h</span></li>
    </ul>
    <a class="cline-c2-itineraire" href="https://www.google.com/maps/dir/?api=1&amp;destination=209+Avenue+Charles+de+Gaulle,+69160+Tassin-la-Demi-Lune" target="_blank" rel="noopener noreferrer">
      {ICO}<path d="M3 11l19-9-9 19-2-8-8-2Z"/></svg> Ouvrir l&rsquo;itin&eacute;raire</a>
  </aside>

  <div class="cline-c2-form">__FORMULAIRE__</div>

</div></div>'''

CSS = '''
/* --- Bloc contact en deux volets --- */
.cline-contact2{padding:70px 30px 76px;background:#f7f6f4;}
.cline-contact2-carte{max-width:1120px;margin:0 auto;display:grid;grid-template-columns:0.85fr 1.15fr;
  background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 22px 60px rgba(0,0,0,.10);}
@media(max-width:900px){.cline-contact2-carte{grid-template-columns:1fr;}}
/* volet sombre */
.cline-c2-info{background:#22211f;color:#fff;padding:46px 40px;display:flex;flex-direction:column;gap:30px;position:relative;}
.cline-c2-info::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 80% at 100% 0%,rgba(201,152,95,.20),transparent 60%);}
.cline-c2-info > *{position:relative;z-index:1;}
@media(max-width:600px){.cline-c2-info{padding:36px 26px;}}
.cline-c2-sur{display:block;font-size:11.5px;letter-spacing:3.2px;text-transform:uppercase;color:#c9985f;margin-bottom:10px;}
.cline-c2-info h2{color:#fff!important;margin:0 0 12px;font-size:clamp(24px,2.6vw,33px);line-height:1.2;}
.cline-c2-intro{margin:0;font-size:15px;line-height:1.75;color:#b8b2ab;}
.cline-c2-liste{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:20px;}
.cline-c2-liste li{display:flex;gap:14px;align-items:flex-start;}
.cline-c2-liste svg{width:19px;height:19px;flex:0 0 19px;margin-top:3px;color:#c9985f;}
.cline-c2-liste span{font-size:14.5px;line-height:1.6;color:#a8a29b;}
.cline-c2-liste strong{display:block;color:#fff;font-weight:600;font-size:15.5px;margin-bottom:2px;}
.cline-c2-liste a{text-decoration:none;}
.cline-c2-liste a strong{transition:color .2s;}
.cline-c2-liste a:hover strong{color:#c9985f;}
.cline-c2-itineraire{display:inline-flex;align-items:center;gap:9px;align-self:flex-start;
  padding:12px 24px;border:1px solid rgba(255,255,255,.28);border-radius:40px;color:#fff!important;
  text-decoration:none;font-size:13.5px;font-weight:600;letter-spacing:.6px;
  transition:background-color .22s,border-color .22s,transform .22s;}
.cline-c2-itineraire svg{width:16px;height:16px;}
.cline-c2-itineraire:hover{background:#c9985f;border-color:#c9985f;transform:translateY(-2px);}
/* volet clair */
.cline-c2-form{padding:46px 42px;}
@media(max-width:600px){.cline-c2-form{padding:34px 24px;}}
.cline-c2-form #cline-contact-form{background:transparent;border:none;border-radius:0;padding:0;box-shadow:none;}
'''

# on recupere le formulaire actuel pour le replacer dans le nouveau volet
mf = re.search(r'<form[^>]*id="cline-contact-form".*?</form>', t, re.S)
assert mf, 'formulaire introuvable'
formulaire = mf.group(0)
BLOC = BLOC.replace('__FORMULAIRE__', formulaire)

# on remplace toute la section (coordonnees + formulaire)
i = t.find('<div class="cline-coord">')
debut = t.rfind('<div class="fusion-fullwidth', 0, i)
fin = t.find('<div class="cline-find-us">')
assert debut > 0 and fin > debut, 'bornes introuvables'
ancien = t[debut:fin]
assert 'cline-coord' in ancien and 'cline-contact-form' in ancien, 'section mal delimitee'
print('ancien bloc :', len(ancien), 'caracteres')

t = t[:debut] + BLOC + t[fin:]
t = t.replace('<style id="cline-contact-css">', '<style id="cline-contact-css">' + CSS, 1)
open(P, 'w', encoding='utf-8').write(t)
print('bloc contact remplace par le design en deux volets')
