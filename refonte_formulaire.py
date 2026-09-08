#!/usr/bin/env python3
"""Refonte du formulaire de contact : structure propre, carte, deux colonnes, libelles relies."""
import re

P = 'site/cuisine/contact/index.html'
t = open(P, encoding='utf-8').read()

FORM = '''<form action="https://formsubmit.co/corinne@c-line-cuisines.com" method="post" id="cline-contact-form" aria-label="Formulaire de contact">
<input type="hidden" name="_subject" value="Message depuis le site C-LINE Cuisines">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="" id="cline-form-next">
<input type="text" name="_honey" class="cline-piege" tabindex="-1" autocomplete="off" aria-hidden="true">

<div class="cline-champs">
  <div class="cline-champ">
    <label for="cf-nom">Votre nom <span aria-hidden="true">*</span></label>
    <input id="cf-nom" type="text" name="your-name" required autocomplete="name"
           maxlength="120" placeholder="Marie Dupont">
  </div>
  <div class="cline-champ">
    <label for="cf-mail">Votre e-mail <span aria-hidden="true">*</span></label>
    <input id="cf-mail" type="email" name="your-email" required autocomplete="email"
           inputmode="email" maxlength="180" placeholder="marie@exemple.fr">
  </div>
</div>

<div class="cline-champ">
  <label for="cf-tel">Votre t&eacute;l&eacute;phone <span class="cline-facultatif">facultatif</span></label>
  <input id="cf-tel" type="tel" name="your-phone" autocomplete="tel" inputmode="tel"
         maxlength="30" placeholder="06 12 34 56 78">
</div>

<div class="cline-champ">
  <label for="cf-sujet">Votre projet</label>
  <select id="cf-sujet" name="your-subject">
    <option value="Cuisine">Une cuisine</option>
    <option value="Salle de bain">Une salle de bain</option>
    <option value="Dressing / rangements">Un dressing ou des rangements</option>
    <option value="Rénovation complète">Une rénovation compl&egrave;te</option>
    <option value="Visite du showroom">Visiter le show-room</option>
    <option value="Autre">Autre demande</option>
  </select>
</div>

<div class="cline-champ">
  <label for="cf-msg">Votre message <span aria-hidden="true">*</span></label>
  <textarea id="cf-msg" name="your-message" required rows="7" maxlength="2000"
            placeholder="Dites-nous en quelques mots ce que vous imaginez&nbsp;: la pi&egrave;ce, vos envies, vos contraintes&hellip;"></textarea>
</div>

<button type="submit" class="cline-envoyer">Envoyer mon message</button>
<p class="cline-mention">Vos informations servent uniquement &agrave; vous r&eacute;pondre. Elles ne sont ni revendues, ni utilis&eacute;es &agrave; d&rsquo;autres fins.</p>
</form>'''

m = re.search(r'<form[^>]*id="cline-contact-form".*?</form>', t, re.S)
assert m, 'formulaire introuvable'
t = t[:m.start()] + FORM + t[m.end():]

CSS = '''
/* --- Formulaire : carte et champs --- */
#cline-contact-form{background:#fff;border:1px solid #ece8e3;border-radius:14px;
  padding:34px 32px 30px;box-shadow:0 8px 30px rgba(0,0,0,.06);max-width:none;}
@media(max-width:600px){#cline-contact-form{padding:24px 20px;}}
.cline-piege{position:absolute!important;left:-9999px!important;}
.cline-champs{display:grid;grid-template-columns:1fr 1fr;gap:0 18px;}
@media(max-width:620px){.cline-champs{grid-template-columns:1fr;}}
.cline-champ{margin:0 0 20px;}
.cline-champ label{display:block;margin:0 0 8px;font-size:13.5px;font-weight:600;
  letter-spacing:.2px;color:#4a4744;}
.cline-champ label span[aria-hidden]{color:#c9985f;}
.cline-facultatif{font-weight:400;font-size:12px;color:#a8a29c;letter-spacing:.3px;}
#cline-contact-form input[type=text],#cline-contact-form input[type=email],
#cline-contact-form input[type=tel],#cline-contact-form select,#cline-contact-form textarea{
  width:100%;height:auto;min-height:52px;padding:14px 16px;border:1px solid #ded9d3;
  border-radius:9px;background:#fdfcfb;font-size:15.5px;color:#2b2b2b;line-height:1.45;
  font-family:inherit;box-shadow:none;transition:border-color .2s,box-shadow .2s,background-color .2s;
  -webkit-appearance:none;appearance:none;}
#cline-contact-form select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238a847e' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 15px center;background-size:18px;padding-right:44px;cursor:pointer;}
#cline-contact-form textarea{min-height:150px;resize:vertical;line-height:1.65;}
#cline-contact-form input:focus,#cline-contact-form select:focus,#cline-contact-form textarea:focus{
  outline:none;background:#fff;border-color:#c9985f;box-shadow:0 0 0 3px rgba(201,152,95,.16);}
#cline-contact-form input::placeholder,#cline-contact-form textarea::placeholder{color:#b8b2ac;opacity:1;}
.cline-envoyer{width:100%;margin-top:6px;padding:16px 32px;border:none;border-radius:40px;cursor:pointer;
  background:#c9985f;color:#fff;font-size:15px;font-weight:600;letter-spacing:.5px;font-family:inherit;
  transition:background-color .22s,transform .22s,box-shadow .22s;box-shadow:0 6px 18px rgba(201,152,95,.30);}
.cline-envoyer:hover{background:#b4864e;transform:translateY(-2px);box-shadow:0 10px 26px rgba(201,152,95,.40);}
.cline-envoyer:active{transform:translateY(0);}
.cline-mention{margin:16px 0 0;font-size:12px;line-height:1.6;color:#a8a29c;text-align:center;}
'''
t = t.replace('<style id="cline-contact-css">', '<style id="cline-contact-css">' + CSS, 1)
open(P, 'w', encoding='utf-8').write(t)
print('formulaire refait')
