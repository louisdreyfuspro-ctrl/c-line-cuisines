#!/usr/bin/env python3
"""Page contact : ton plus chaleureux (fin des majuscules criardes, phrases humaines)."""
import re

P = 'site/cuisine/contact/index.html'
t = open(P, encoding='utf-8').read()

# ---------- 1) Titre d'accroche plus humain ----------
t = t.replace('<h1>Nous contacter</h1>', '<h1>Parlons de votre projet</h1>', 1)
t = t.replace('<p class="cline-hero-sur">C-LINE &middot; Tassin-La-Demi-Lune</p>',
              '<p class="cline-hero-sur">Bienvenue chez C-LINE</p>', 1)
t = t.replace('209 Av Charles de Gaulle &nbsp;&middot;&nbsp; Showroom de 200&nbsp;m&sup2; &nbsp;&middot;&nbsp; du lundi au samedi',
              'Passez nous voir au 209 Av Charles de Gaulle &agrave; Tassin&nbsp;: 200&nbsp;m&sup2; de showroom vous attendent, du lundi au samedi.', 1)

# ---------- 2) Baseline des coordonnees ----------
t = t.replace('<p class="cline-coord-bl">Cuisines, salles de bain &amp; rangements</p>',
              '<p class="cline-coord-bl">Cuisines, salles de bain et rangements sur mesure</p>', 1)

# ---------- 3) Mot d'accueil au-dessus du formulaire ----------
ACCUEIL = ('<div class="cline-form-intro">'
           '<h3>&Eacute;crivez-nous</h3>'
           '<p>Une question, une envie, un projet encore flou&nbsp;? Racontez-nous en quelques mots, '
           'nous vous r&eacute;pondons rapidement &mdash; sans engagement, et toujours avec plaisir.</p>'
           '</div>')
m = re.search(r'<form[^>]*id="cline-contact-form"', t)
assert m, 'formulaire introuvable'
debut_bloc = t.rfind('<div class="wpcf7', 0, m.start())
if debut_bloc < 0:
    debut_bloc = m.start()
t = t[:debut_bloc] + ACCUEIL + t[debut_bloc:]

# ---------- 4) Libelles du formulaire, en douceur ----------
for vieux, neuf in [
    ('Votre nom (obligatoire)', 'Votre nom'),
    ('Votre email (obligatoire)', 'Votre e-mail'),
    ('Sujet', 'Le sujet'),
    ('Votre message', 'Votre message'),
]:
    t = t.replace('<p>%s\n</p>' % vieux, '<p>%s</p>' % neuf, 1)

# bouton d'envoi
t = t.replace('value="Envoyer"', 'value="Envoyer mon message"', 1)

# ---------- 5) Fin des majuscules criardes ----------
CSS_DOUX = '''
/* --- Ton plus chaleureux --- */
#cline-contact-form p{text-transform:none!important;letter-spacing:.2px!important;
  font-size:13.5px!important;color:#7d7873!important;font-weight:500;}
.cline-coord-bl{text-transform:none!important;letter-spacing:.3px!important;
  font-size:14.5px!important;color:#8d8781!important;font-style:italic;}
.cline-hero-sur{text-transform:none!important;letter-spacing:1.2px!important;font-size:14px!important;}
.cline-itineraire{text-transform:none!important;letter-spacing:.6px!important;font-size:14px!important;}
#cline-contact-form input[type=submit]{text-transform:none!important;letter-spacing:.5px!important;
  font-size:15px!important;}
.cline-hero-adr{max-width:620px;margin-left:auto;margin-right:auto;line-height:1.65;}
.cline-form-intro{margin:0 0 26px;}
.cline-form-intro h3{margin:0 0 10px;font-size:23px;color:#2b2b2b;letter-spacing:.2px;}
.cline-form-intro p{margin:0;font-size:15.5px;line-height:1.75;color:#6f6a65;}
.cline-find-us-sub{text-transform:none;}
'''
t = t.replace('<style id="cline-contact-css">', '<style id="cline-contact-css">' + CSS_DOUX, 1)

open(P, 'w', encoding='utf-8').write(t)
print('page contact rechauffee')
