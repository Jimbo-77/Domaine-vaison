# Domaine-vaison

Site vitrine des trois maisons de vacances à deux pas du Théâtre antique de Vaison-la-Romaine.

- `maquette/index.html` — l'accueil en français (page de référence)
- `maquette/villacotepiscine.html`, `maquette/villa2terrasses.html` — pages des maisons Olivier et Lavande, et Les Cigales (mêmes adresses que sur le site actuel)
- `maquette/style.css`, `maquette/site.js` — mise en forme et script communs
- `maquette/polices/` — polices Marcellus et Commissioner hébergées sur le site (licence OFL)
- `maquette/outils/images.py` — recrée les images WebP après le remplacement d'une photo
- `maquette/en/`, `maquette/de/`, `maquette/nl/`, `maquette/es/` — versions anglaise, allemande, néerlandaise et espagnole, générées par `maquette/outils/traduire.py`
- `maquette/i18n/` — traductions et mode d'emploi (`maquette/i18n/README.md`)
- `maquette/photos/` — photos du site actuel (voir `maquette/photos/README.md`)
- `maquette/ANALYSE.md` — analyse du site actuel residenceletheatre.com et points à valider
- `maquette/ANALYSE-RESERVATION.md` — analyse de la réservation sur le site actuel et recommandations
- `maquette/SMOOBU.md` — comment brancher la réservation en ligne Smoobu
- `maquette/apercu-*.png` — captures desktop et mobile

## Mise en ligne définitive

Tant que le site est une maquette, toutes les pages demandent aux moteurs de recherche de ne pas
les indexer, pour ne pas concurrencer le site actuel. Le jour de la mise en ligne :

1. Dans `maquette/outils/traduire.py`, régler `ADRESSE_SITE` sur l'adresse définitive
   (par exemple `'https://www.residenceletheatre.com/'`) et passer `INDEXABLE` à `True`.
2. Lancer `python3 maquette/outils/traduire.py` : adresses canoniques, liens entre langues,
   `robots.txt` et `sitemap.xml` sont mis à jour, et l'interdiction d'indexer est retirée.
3. Publier le contenu du dossier `maquette/` à la racine du domaine.
4. Déclarer `sitemap.xml` dans Google Search Console.
5. Rediriger les anciennes adresses du site actuel vers les nouvelles pages.

