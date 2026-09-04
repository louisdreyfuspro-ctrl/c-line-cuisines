# C-LINE Cuisines — site statique

Refonte du site **c-line-cuisines.com** (C-LINE Cuisines, Corinne Gabet — Tassin-La-Demi-Lune).

Le site d'origine tournait sous WordPress (thème Avada). Les identifiants d'administration
ayant été perdus, le site a été reconstruit en **statique** : plus de WordPress, plus de base
de données, plus de risque de perdre l'accès. Il se déploie tel quel sur n'importe quel
hébergement.

## Lancer le site en local

```bash
python3 serve.py
```

Puis ouvrir <http://localhost:8741>.

Le serveur est volontairement multi-thread et sans cache (`Cache-Control: no-store`) :
un `python -m http.server` classique tronque les pages de ce site, très riches en ressources.

## Organisation

| Chemin | Contenu |
|---|---|
| `site/` | Le site complet, prêt à déployer (177 pages) |
| `site/wp-content/uploads/` | Photos d'origine + médias ajoutés (`2026/09/`) |
| `serve.py` | Serveur local de développement |
| `site/sitemap.xml`, `site/robots.txt` | Référencement |

## Ce qui a été ajouté au site d'origine

- **Film narratif au scroll** sur l'accueil (40 s) : page blanche → croquis → maquette 3D → cuisine
- **Films « expérience »** (16 s) sur les pages Salles de bain et Rangements
- **Section « Ambiance Dressing »** avec sélecteur d'ambiances
- **Comparateurs avant/après** sur les rénovations de salles de bains
- **Lightbox** plein écran, apparitions au scroll, en-tête compact, barre de progression
- **Page contact** refaite : nouvelle adresse, actions rapides (appeler / écrire / itinéraire), carte

Les blocs ajoutés sont identifiables dans le HTML par le préfixe `cline-`
(`cline-mods`, `cline-visite`, `cline-exp-*`, `cline-dressing`, `cline-immersive`, `cline-modern`).

## Points en attente de validation client

- Certains visuels (films, ambiances dressing) sont **générés**, pas photographiés :
  à remplacer par de vraies photos si le client le souhaite.
- Page Cuisines : le texte mentionne NOLTE — préciser si Veneta Cucine s'ajoute ou remplace.
- Page « Votre showroom dédié près de Lyon » : vide (elle l'était déjà sur le site d'origine).
- Horaires affichés sur la page contact : à confirmer après le déménagement.
- Formulaire de contact : passe par FormSubmit vers `corinne@c-line-cuisines.com`.
  **Le premier envoi déclenche un e-mail d'activation à valider une fois.**

## Note

Les masters vidéo 4K ne sont pas versionnés (trop volumineux) ; ils sont conservés
localement à la racine du projet.
