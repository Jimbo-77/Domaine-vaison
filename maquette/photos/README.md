# Photos

Photos récupérées sur residenceletheatre.com (octobre 2026), recompressées sans métadonnées.

## Utilisées par la maquette (1200 px)

| Fichier | Où | Original |
|---|---|---|
| `accueil-piscine.jpg` | Ouverture, grand arc | `residentheatre-16.jpg` |
| `accueil-olivier.jpg` | Ouverture, arc du haut | `SAM_2117_1080.jpg` |
| `accueil-terrasse.jpg` | Ouverture, arc du bas | `SAM_2122_1080.jpg` |
| `entree.jpg` | Section « Sur place » | `SAM_3534_1080.jpg` |
| `olivier-lavande.jpg` | Fiche Olivier et Lavande | `1676558f1dcadd750df69defc4e16d6b.jpg` |
| `cigales.jpg` | Fiche Les Cigales | `residentheatre-12.jpg` |
| `piscine.jpg` | Réserve | `residentheatre-18.jpg` |
| `pont-romain.jpg` | Section « Autour » | `1fa7748ea79f0770434323efd9a8b54b.jpg` |
| `jardin.jpg` | Réserve (page détail à venir) | `SAM_2128_1080.jpg` |

Les pages affichent des versions WebP plus légères, en trois largeurs (`<nom>-480.webp`, `-800.webp`,
`-1200.webp`) : le navigateur choisit la bonne selon l'écran. Les galeries utilisent `<nom>.webp` dans
`site-actuel/` et `vignettes/`. Les JPEG restent la source, et servent d'image d'aperçu quand on partage
un lien (WhatsApp, Facebook…).

Pour changer une photo : remplacez le JPEG en gardant le même nom, puis lancez
`python3 maquette/outils/images.py`, qui recrée toutes les versions WebP.

## Archive complète : `site-actuel/` (1600 px max)

Les 55 images trouvées sur le site, avec leurs noms d'origine : intérieurs et extérieurs des villas
(séries `residentheatre-*`, `SAM_*` et noms en hexadécimal) et photos des environs
(Vaison, Mont Ventoux, Avignon, Dentelles de Montmirail).

**Droits** : les photos de la résidence appartiennent au propriétaire. Les photos touristiques
(Ventoux, Avignon, pont romain…) peuvent provenir d'une banque d'images fournie par le prestataire
du site actuel : vérifiez leur licence avant de les publier ailleurs.

## Galeries des maisons

Les galeries (vignettes sous chaque fiche, visionneuse plein écran) affichent les photos de
`site-actuel/` et leurs vignettes de `vignettes/` (360 px, mêmes noms de fichier).
La liste des photos de chaque galerie est dans l'objet `GALERIES` de `maquette/site.js` ; leurs légendes
sont dans le bloc de textes des pages (section `legendes`) et dans `maquette/i18n/*.json` pour les traductions.
Pour ajouter une photo : déposez-la dans `site-actuel/`, créez sa vignette dans `vignettes/`, ajoutez
son nom (sans extension) dans la bonne galerie de `site.js`, sa légende française dans le bloc de textes
des trois pages françaises et sa traduction dans chaque fichier de langue, puis lancez
`python3 maquette/outils/images.py` et `python3 maquette/outils/traduire.py`.
