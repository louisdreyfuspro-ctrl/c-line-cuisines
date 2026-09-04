#!/usr/bin/env python3
"""Cree la page « Qui sommes-nous » a partir d'une page simple existante."""
import re, os, html

SLUG = 'qui-sommes-nous'
TITRE = "Qui sommes-nous&nbsp;?"
GABARIT = 'site/mentions-legales/index.html'

PARTENAIRES = [
    ("Forma", "/wp-content/uploads/2026/09/logo-forma-cucine.jpg", "https://formalacucina.fr/", "Cuisines italiennes"),
    ("Nolte", "/wp-content/uploads/2015/09/logo-nolte-hd2.jpg", "https://www.nolte-kuechen.com/", "Mobilier de cuisine allemand"),
    ("Ideagroup", "/wp-content/uploads/2015/09/logo_ideagroup_black.png", "https://www.ideagroupbains.fr/", "Mobilier de salle de bain"),
    ("Ambiance Dressing", "/wp-content/uploads/2026/09/logo-ambiance-dressing.png", "https://www.ambiance-dressing.fr/", "Dressings et rangements sur mesure"),
]
SHOWROOM = ['/wp-content/uploads/2026/09/qsn-showroom-%d.jpg' % i for i in range(1, 10)]

CONTENU = '''
<style id="cline-qsn-css">
.cline-qsn-hero{position:relative;min-height:56vh;display:flex;align-items:center;justify-content:center;
  background:#222 url('/wp-content/uploads/2026/09/qsn-facade.jpg') center 60%/cover no-repeat;text-align:center;padding:90px 24px;}
.cline-qsn-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.42),rgba(0,0,0,.18) 45%,rgba(0,0,0,.5));}
.cline-qsn-hero > div{position:relative;z-index:2;color:#fff;}
.cline-qsn-hero h1{color:#fff!important;margin:0 0 12px;text-shadow:0 3px 20px rgba(0,0,0,.55);}
.cline-qsn-hero p{margin:0;font-size:15px;letter-spacing:1.4px;opacity:.94;text-shadow:0 1px 12px rgba(0,0,0,.6);}
.cline-qsn{padding:64px 30px 20px;background:#fff;}
.cline-qsn-inner{max-width:900px;margin:0 auto;}
.cline-qsn-inner h2{font-size:clamp(22px,2.4vw,31px);margin:0 0 18px;color:#2b2b2b;}
.cline-qsn-inner p{font-size:16.5px;line-height:1.85;color:#5a554f;margin:0 0 18px;}
.cline-qsn-signature{margin-top:26px;padding-left:20px;border-left:3px solid #c9985f;font-style:italic;color:#7a746e;}
.cline-qsn-chiffres{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:18px;margin:44px 0 6px;}
.cline-qsn-chiffre{text-align:center;padding:26px 18px;background:#fbfaf8;border:1px solid #efece8;border-radius:11px;}
.cline-qsn-chiffre strong{display:block;font-size:30px;color:#c9985f;font-weight:700;margin-bottom:6px;}
.cline-qsn-chiffre span{font-size:13.5px;color:#7a746e;line-height:1.5;}
.cline-qsn-gal{padding:20px 30px 66px;background:#fff;}
.cline-qsn-gal-inner{max-width:1180px;margin:0 auto;}
.cline-qsn-gal h2{text-align:center;margin:0 0 8px;}
.cline-qsn-gal .sous{text-align:center;color:#8a8580;font-size:15px;margin:0 0 30px;}
.cline-qsn-grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:13px;}
.cline-qsn-grille a{display:block;overflow:hidden;border-radius:8px;aspect-ratio:1/1;box-shadow:0 3px 14px rgba(0,0,0,.10);}
.cline-qsn-grille img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease;}
.cline-qsn-grille a:hover img{transform:scale(1.06);}
.cline-qsn-part{padding:58px 30px 66px;background:#fbfaf8;border-top:1px solid #efece8;}
.cline-qsn-part-inner{max-width:1080px;margin:0 auto;text-align:center;}
.cline-qsn-part h2{margin:0 0 8px;}
.cline-qsn-part .sous{color:#8a8580;font-size:15px;margin:0 0 32px;}
.cline-qsn-part-grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:18px;}
.cline-qsn-part-carte{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:13px;
  padding:28px 20px;background:#fff;border:1px solid #eeebe7;border-radius:11px;text-decoration:none;
  transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;}
.cline-qsn-part-carte:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(0,0,0,.10);border-color:#e0d8cd;}
.cline-qsn-part-carte img{max-height:58px;width:auto;object-fit:contain;border-radius:5px;filter:none!important;opacity:1!important;}
.cline-qsn-part-carte span{font-size:12.5px;color:#8a847e;line-height:1.5;}
.cline-qsn-infos{padding:56px 30px 70px;background:#fff;}
.cline-qsn-infos-inner{max-width:900px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:34px;}
@media(max-width:760px){.cline-qsn-infos-inner{grid-template-columns:1fr;}}
.cline-qsn-bloc h3{font-size:19px;margin:0 0 12px;color:#2b2b2b;}
.cline-qsn-bloc p{margin:0 0 6px;font-size:15.5px;line-height:1.7;color:#5a554f;}
.cline-qsn-bloc a{color:#5a554f;text-decoration:none;border-bottom:1px solid transparent;transition:color .2s,border-color .2s;}
.cline-qsn-bloc a:hover{color:#c9985f;border-color:#c9985f;}
.cline-qsn-cta{text-align:center;margin-top:38px;}
.cline-qsn-cta a{display:inline-block;padding:14px 38px;border-radius:40px;background:#c9985f;color:#fff!important;
  text-decoration:none;font-size:13px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
  transition:background-color .22s,transform .22s,box-shadow .22s;box-shadow:0 6px 18px rgba(201,152,95,.32);}
.cline-qsn-cta a:hover{background:#b4864e;transform:translateY(-2px);}
</style>

<div class="cline-qsn-hero"><div>
  <div class="fusion-text"><h1>Qui sommes-nous&nbsp;?</h1></div>
  <p>C-LINE &middot; Tassin-La-Demi-Lune</p>
</div></div>

<div class="cline-qsn"><div class="cline-qsn-inner">
  <h2>Vingt ans d&rsquo;exp&eacute;rience dans l&rsquo;am&eacute;nagement de l&rsquo;habitat</h2>
  <p>Architecte d&rsquo;int&eacute;rieur et titulaire d&rsquo;un dipl&ocirc;me d&rsquo;&Eacute;tat,
     <strong>Corinne Gabet</strong> a s&eacute;lectionn&eacute; pour vous satisfaire des gammes de meubles
     reconnues, et vous accompagne de la premi&egrave;re esquisse jusqu&rsquo;&agrave; la pose.</p>
  <p>C-LINE, c&rsquo;est aussi une s&eacute;lection d&rsquo;articles d&rsquo;am&eacute;nagement pour votre
     int&eacute;rieur&nbsp;: plans de travail pour cuisines et salles de bains en granite, corian, inox,
     marbre, quartz mais aussi en verre.</p>
  <p>En plein c&oelig;ur de Tassin-La-Demi-Lune, notre show-room de 200&nbsp;m&sup2; vous accueille
     du mardi au samedi, le lundi sur rendez-vous.</p>
  <p class="cline-qsn-signature">Nous partons d&rsquo;une page blanche&nbsp;: vos id&eacute;es sont mises
     en forme, puis votre projet prend vie.</p>

  <div class="cline-qsn-chiffres">
    <div class="cline-qsn-chiffre"><strong>20 ans</strong><span>d&rsquo;exp&eacute;rience dans l&rsquo;am&eacute;nagement</span></div>
    <div class="cline-qsn-chiffre"><strong>200 m&sup2;</strong><span>de show-room &agrave; Tassin</span></div>
    <div class="cline-qsn-chiffre"><strong>4 marques</strong><span>partenaires s&eacute;lectionn&eacute;es</span></div>
  </div>
</div></div>

<div class="cline-qsn-gal"><div class="cline-qsn-gal-inner">
  <div class="fusion-text"><h2>Notre show-room</h2></div>
  <p class="sous">Cuisines, salles de bain et rangements expos&eacute;s, mat&eacute;riaux &agrave; toucher, projets &agrave; imaginer.</p>
  <div class="cline-qsn-grille">__SHOWROOM__</div>
</div></div>

<div class="cline-qsn-part"><div class="cline-qsn-part-inner">
  <div class="fusion-text"><h2>Nos partenaires</h2></div>
  <p class="sous">Les marques que nous avons s&eacute;lectionn&eacute;es pour leur qualit&eacute; et leur savoir-faire.</p>
  <div class="cline-qsn-part-grille">__PARTENAIRES__</div>
</div></div>

<div class="cline-qsn-infos"><div class="cline-qsn-infos-inner">
  <div class="cline-qsn-bloc">
    <h3>Nous rendre visite</h3>
    <p>209 Av Charles de Gaulle<br>69160 Tassin-La-Demi-Lune</p>
    <p><a href="tel:+33478476951">04 78 47 69 51</a></p>
    <p><a href="mailto:corinne@c-line-cuisines.com">corinne@c-line-cuisines.com</a></p>
  </div>
  <div class="cline-qsn-bloc">
    <h3>Horaires</h3>
    <p><strong>Lundi</strong>&nbsp;: sur rendez-vous</p>
    <p><strong>Mardi &agrave; vendredi</strong>&nbsp;: 9h30&ndash;12h / 14h30&ndash;19h</p>
    <p><strong>Samedi</strong>&nbsp;: 9h30&ndash;12h / 14h30&ndash;18h</p>
  </div>
</div>
<div class="cline-qsn-cta"><a href="/cuisine/contact/">Prendre rendez-vous</a></div>
</div>
'''

CONTENU = CONTENU.replace('__SHOWROOM__', ''.join(
    '<a href="%s"><img src="%s" alt="Show-room C-LINE à Tassin-La-Demi-Lune" loading="lazy"></a>' % (p, p)
    for p in SHOWROOM))
CONTENU = CONTENU.replace('__PARTENAIRES__', ''.join(
    '<a class="cline-qsn-part-carte" href="%s" target="_blank" rel="noopener noreferrer" title="%s">'
    '<img src="%s" alt="%s" loading="lazy"><span>%s</span></a>' % (lien, nom, logo, nom, desc)
    for nom, logo, lien, desc in PARTENAIRES))

t = open(GABARIT, encoding='utf-8').read()
DESC = ("Architecte d'intérieur, Corinne Gabet et C-LINE vous accompagnent depuis 20 ans : "
        "cuisines, salles de bain et rangements sur mesure. Show-room de 200 m² à Tassin-La-Demi-Lune.")
t = t.replace('Mentions légales', 'Qui sommes-nous')
t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(DESC)+m.group(2), t, count=1)
t = re.sub(r'(og:description" content=")[^"]*(")', lambda m: m.group(1)+html.escape(DESC)+m.group(2), t, count=1)
t = t.replace('/mentions-legales/', '/%s/' % SLUG)
t = re.sub(r'(og:image" content=")[^"]*(")', r'\g<1>/wp-content/uploads/2026/09/qsn-facade.jpg\g<2>', t, count=1)

m = re.search(r'(<div class="post-content[^"]*">)(.*?)(\s*</div>\s*</div>\s*</article>)', t, re.S)
if not m:
    m = re.search(r'(<div class="post-content[^"]*">)(.*?)(</div>)', t, re.S)
t = t[:m.start()] + m.group(1) + CONTENU + m.group(3) + t[m.end():]

os.makedirs('site/' + SLUG, exist_ok=True)
open('site/%s/index.html' % SLUG, 'w', encoding='utf-8').write(t)
print('page creee : site/%s/index.html' % SLUG)
