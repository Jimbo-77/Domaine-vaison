#!/usr/bin/env python3
"""Génère les versions traduites de la maquette.

La page française (maquette/index.html) est la référence : chaque texte à traduire y porte
une clé (data-i18n="cle" pour le contenu, data-i18n-alt="cle" pour un attribut, etc.).
Les traductions sont dans maquette/i18n/<langue>.json.

Utilisation, depuis la racine du dépôt :
    python3 maquette/outils/traduire.py

Le script :
  1. met à jour maquette/i18n/fr.json (textes de référence, à ne pas modifier à la main) ;
  2. écrit maquette/<langue>/index.html pour chaque fichier de langue ;
  3. signale les clés manquantes (le texte français est alors conservé).
"""
import html
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / 'index.html'
DOSSIER_I18N = RACINE / 'i18n'
LANGUES = {'fr': 'Français', 'en': 'English', 'de': 'Deutsch', 'nl': 'Nederlands'}

RE_CONTENU = re.compile(r'(<([a-zA-Z0-9]+)\b[^>]*\sdata-i18n="([^"]+)"[^>]*>)(.*?)(</\2>)', re.S)
RE_ATTRIBUT = re.compile(r'(\s([a-z-]+)=")([^"]*)(" data-i18n-\2="([^"]+)")')
RE_TEXTES = re.compile(r'(<script id="textes" type="application/json">\n)(.*?)(\n</script>)', re.S)


def extraire(page):
    textes = {}
    for m in RE_CONTENU.finditer(page):
        textes.setdefault(m.group(3), m.group(4))
    for m in RE_ATTRIBUT.finditer(page):
        textes.setdefault(m.group(5), html.unescape(m.group(3)))
    script = json.loads(RE_TEXTES.search(page).group(2))
    return textes, script


def fusionner(reference, traduction, chemin, manquants):
    """Complète la traduction avec le français pour les clés absentes."""
    if isinstance(reference, dict):
        traduction = traduction if isinstance(traduction, dict) else {}
        return {k: fusionner(v, traduction.get(k), f'{chemin}.{k}', manquants) for k, v in reference.items()}
    if traduction in (None, ''):
        manquants.append(chemin)
        return reference
    return traduction


def selecteur_langues(page, langue):
    def option(code):
        valeur = ('./' if code == langue else
                  ('../' if code == 'fr' else f'../{code}/') if langue != 'fr' else f'{code}/')
        choisi = ' selected' if code == langue else ''
        return f'<option value="{valeur}" lang="{code}"{choisi}>{LANGUES[code]}</option>'
    options = ''.join(option(c) for c in LANGUES)
    return re.sub(r'(<select [^>]*onchange="location\.href = this\.value">).*?(</select>)',
                  lambda m: m.group(1) + options + m.group(2), page, count=1, flags=re.S)


def generer(page, langue, textes, script):
    page = RE_CONTENU.sub(lambda m: m.group(1) + textes.get(m.group(3), m.group(4)) + m.group(5), page)
    page = RE_ATTRIBUT.sub(
        lambda m: m.group(1) + html.escape(textes.get(m.group(5), html.unescape(m.group(3))), quote=True) + m.group(4), page)
    page = RE_TEXTES.sub(lambda m: m.group(1) + json.dumps(script, ensure_ascii=False, indent=2) + m.group(3), page)
    page = page.replace('<html lang="fr">', f'<html lang="{langue}">', 1)
    page = re.sub(r'(<link rel="canonical" href="[^"]*/maquette/)', rf'\g<1>{langue}/', page, count=1)
    page = selecteur_langues(page, langue)
    # La page traduite est un dossier plus bas : on remonte pour les photos.
    page = re.sub(r'(\s(?:src|href)=")photos/', r'\1../photos/', page)
    page = page.replace("const PHOTOS = 'photos/';", "const PHOTOS = '../photos/';")
    return page


def main():
    page = SOURCE.read_text(encoding='utf-8')
    textes_fr, script_fr = extraire(page)
    DOSSIER_I18N.mkdir(exist_ok=True)
    (DOSSIER_I18N / 'fr.json').write_text(
        json.dumps({'langue': 'fr', 'textes': textes_fr, 'script': script_fr}, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')

    erreurs = 0
    for code in LANGUES:
        if code == 'fr':
            continue
        fichier = DOSSIER_I18N / f'{code}.json'
        if not fichier.exists():
            print(f'{code} : {fichier.name} absent, langue ignorée')
            continue
        donnees = json.loads(fichier.read_text(encoding='utf-8'))
        manquants = []
        textes = fusionner(textes_fr, donnees.get('textes'), 'textes', manquants)
        script = fusionner(script_fr, donnees.get('script'), 'script', manquants)
        inutiles = sorted(set(donnees.get('textes', {})) - set(textes_fr))
        sortie = RACINE / code / 'index.html'
        sortie.parent.mkdir(exist_ok=True)
        sortie.write_text(generer(page, code, textes, script), encoding='utf-8')
        print(f'{code} : {sortie.relative_to(RACINE.parent)} généré'
              + (f', {len(manquants)} texte(s) manquant(s)' if manquants else '')
              + (f', {len(inutiles)} clé(s) inconnue(s)' if inutiles else ''))
        for cle in manquants:
            print(f'   manquant : {cle}')
        for cle in inutiles:
            print(f'   inconnue : textes.{cle}')
        erreurs += len(manquants)
    return 1 if erreurs else 0


if __name__ == '__main__':
    sys.exit(main())
