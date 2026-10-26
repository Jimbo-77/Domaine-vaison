# Traductions

Le site existe en cinq langues, chacune à sa propre adresse :

| Langue | Page | Traductions |
|---|---|---|
| Français (référence) | `maquette/index.html` | dans la page elle-même |
| Anglais | `maquette/en/index.html` | `en.json` |
| Allemand | `maquette/de/index.html` | `de.json` |
| Néerlandais | `maquette/nl/index.html` | `nl.json` |
| Espagnol | `maquette/es/index.html` | `es.json` |

Les pages `en/`, `de/`, `nl/` et `es/` sont **générées** : ne les modifiez pas à la main.

## Modifier un texte

1. **Texte français** : modifiez `maquette/index.html`.
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
2. Ajoutez la langue dans `LANGUES`, en haut de `maquette/outils/traduire.py`.
3. Dans l'en-tête de `index.html`, ajoutez la balise `hreflang` et l'option du sélecteur de langue.
4. Régénérez.

## Ajouter un texte

Ajoutez dans `index.html` l'attribut `data-i18n="ma_cle"` sur l'élément (ou `data-i18n-alt="ma_cle"`,
`data-i18n-aria-label="ma_cle"`… pour un attribut, placé juste après celui-ci), puis la clé
`"ma_cle"` dans chaque fichier de langue, et régénérez.

## Référencement

Chaque page déclare sa langue (`<html lang>`), son adresse canonique et les adresses des autres
langues (`hreflang`). Si l'adresse du site change (nom de domaine), remplacez
`https://jimbo-77.github.io/Domaine-vaison/maquette/` dans l'en-tête de `index.html`, puis régénérez.

Les traductions ont été rédigées pour la maquette : faites-les relire par un locuteur natif
avant la mise en ligne définitive.
