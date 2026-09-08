#!/usr/bin/env python3
"""Fiche etablissement (schema.org LocalBusiness) + confort de saisie du formulaire."""
import re, json

P = 'site/cuisine/contact/index.html'
t = open(P, encoding='utf-8').read()

# ---------- 1) Fiche etablissement pour Google ----------
fiche = {
    "@context": "https://schema.org",
    "@type": "HomeGoodsStore",
    "@id": "https://www.c-line-cuisines.com/#etablissement",
    "name": "C-LINE Cuisines",
    "description": "Cuisines, salles de bain et rangements sur mesure à Tassin-La-Demi-Lune, près de Lyon. Show-room de 140 m².",
    "url": "https://www.c-line-cuisines.com/",
    "telephone": "+33478476951",
    "email": "corinne@c-line-cuisines.com",
    "image": "https://www.c-line-cuisines.com/wp-content/uploads/2026/09/hero-contact-magasin.jpg",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "209 Avenue Charles de Gaulle",
        "postalCode": "69160",
        "addressLocality": "Tassin-la-Demi-Lune",
        "addressRegion": "Auvergne-Rhône-Alpes",
        "addressCountry": "FR",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 45.7556880, "longitude": 4.7719473},
    "hasMap": "https://www.google.com/maps/search/?api=1&query=209+Avenue+Charles+de+Gaulle,+69160+Tassin-la-Demi-Lune",
    "areaServed": [{"@type": "City", "name": "Lyon"}, {"@type": "City", "name": "Tassin-la-Demi-Lune"}],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "09:30", "closes": "12:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "14:30", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:30", "closes": "12:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "14:30", "closes": "18:00"},
    ],
    "openingHours": "Mo by appointment",
    "sameAs": ["https://www.facebook.com/clinecuisines", "https://www.instagram.com/c_line_cuisines/"],
}

BLOC = ('<script type="application/ld+json" id="cline-fiche-etablissement">'
        + json.dumps(fiche, ensure_ascii=False, separators=(',', ':')) + '</script>')

if 'cline-fiche-etablissement' not in t:
    t = t.replace('</head>', BLOC + '</head>', 1)
    print('fiche etablissement ajoutee (adresse, horaires, telephone, GPS)')

# ---------- 2) Confort de saisie ----------
REMPL = [
    ('type="text" name="your-name"',
     'type="text" name="your-name" autocomplete="name" placeholder="Marie Dupont"'),
    ('type="email" name="your-email"',
     'type="email" name="your-email" autocomplete="email" inputmode="email" placeholder="marie@exemple.fr"'),
    ('type="text" name="your-subject"',
     'type="text" name="your-subject" placeholder="Projet de cuisine, demande de rendez-vous…"'),
    ('name="your-message"',
     'name="your-message" placeholder="Dites-nous en quelques mots ce que vous imaginez : la pièce, vos envies, vos contraintes…"'),
]
n = 0
for v, nv in REMPL:
    if v in t and 'placeholder' not in t[t.find(v):t.find(v) + 200]:
        t = t.replace(v, nv, 1); n += 1
print('champs enrichis (saisie automatique + exemples) :', n)

CSS = ('#cline-contact-form input::placeholder,#cline-contact-form textarea::placeholder'
       '{color:#b8b2ac;opacity:1;}')
t = t.replace('<style id="cline-contact-css">', '<style id="cline-contact-css">' + CSS, 1)

open(P, 'w', encoding='utf-8').write(t)
