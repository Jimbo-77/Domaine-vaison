# Traductions

Le site a trois pages, en cinq langues :

| Page | Français (référence) | Autres langues |
|---|---|---|
| Accueil | `maquette/index.html` | `maquette/<langue>/index.html` |
| Olivier et Lavande | `maquette/villacotepiscine.html` | `maquette/<langue>/villacotepiscine.html` |
| Les Cigales | `maquette/villa2terrasses.html` | `maquette/<langue>/villa2terrasses.html` |

Langues : anglais (`en.json`), allemand (`de.json`), néerlandais (`nl.json`), espagnol (`es.json`).
Les dossiers `en/`, `de/`, `nl/` et `es/` sont **générés** : ne les modifiez pas à la main.
La mise en forme (`style.css`) et le script (`site.js`) sont communs à toutes les pages.

## Modifier un texte

1. **Texte français** : modifiez la page française concernée. Une clé présente sur plusieurs pages
   (menu, pied de page, tarifs…) doit garder le même texte partout : le script le signale sinon.
2. **Traduction** : modifiez la valeur correspondante dans `en.json`, `de.json`, `nl.json` ou `es.json`.
   - `textes` : textes de la page (la clé est celle de l'attribut `data-i18n` dans `index.html`) ;
   - `script` : textes affichés par le script (légendes des photos, boutons des galeries, messages).
   - Les `{n}`, `{total}`, `{maison}`, `{legende}` sont remplacés automatiquement : gardez-les.
3. Régénérez les pages, depuis la racine du dépôt :

   ```
   python3 maquette/outils/traduire.py
   ```

   Le script met à jour `fr.json` (textes français de référence, utile aux traducteurs) et signale
   toute traduction manquante ; le texte français est alors affiché à sa place.

## Ajouter une langue

1. Copiez `en.json` en `<code>.json` (par exemple `it.json`) et traduisez les valeurs.
2. En haut de `maquette/outils/traduire.py`, ajoutez la langue dans `LANGUES` et la phrase du bandeau
   de suggestion dans `SUGGESTIONS`, puis dans `LOCALES` (code régional, par exemple `it_IT`).
3. Régénérez : le menu des langues, les balises `hreflang`, le plan du site et le bandeau de
   suggestion de chaque page sont mis à jour automatiquement.

## Ajouter un texte

Ajoutez dans `index.html` l'attribut `data-i18n="ma_cle"` sur l'élément (ou `data-i18n-alt="ma_cle"`,
`data-i18n-aria-label="ma_cle"`… pour un attribut, placé juste après celui-ci), puis la clé
`"ma_cle"` dans chaque fichier de langue, et régénérez.

## Bandeau de suggestion de langue

Si la langue préférée du navigateur du visiteur est disponible et n'est pas celle de la page, un
bandeau lui propose la même page dans sa langue (jamais de redirection automatique). Il disparaît dès
que le visiteur ferme le bandeau ou choisit une langue, et ce choix est mémorisé dans son navigateur.
Les phrases du bandeau sont dans `SUGGESTIONS` (`maquette/outils/traduire.py`), l'affichage dans `site.js`.

## Référencement

Chaque page déclare sa langue (`<html lang>`). Le bloc « référencement » de l'en-tête (adresse
canonique, adresses des autres langues, interdiction d'indexer) est rempli par le script, comme
`robots.txt` et `sitemap.xml` : ne les modifiez pas à la main. Tout dépend de deux réglages en haut
de `maquette/outils/traduire.py` : `ADRESSE_SITE` et `INDEXABLE` (voir « Mise en ligne » dans le
`README.md` du dépôt).

Les traductions ont été rédigées pour la maquette : faites-les relire par un locuteur natif
avant la mise en ligne définitive.
