#!/usr/bin/env python3
"""Génère les versions traduites de la maquette.

Les pages françaises (maquette/index.html, villacotepiscine.html, villa2terrasses.html) sont
la référence : chaque texte à traduire y porte une clé (data-i18n="cle" pour le contenu,
data-i18n-alt="cle" pour un attribut, etc.). Une même clé a le même texte sur toutes les pages.
Les traductions sont dans maquette/i18n/<langue>.json.

Utilisation, depuis la racine du dépôt :
    python3 maquette/outils/traduire.py

Le script :
  1. met à jour maquette/i18n/fr.json (textes de référence, à ne pas modifier à la main) ;
  2. remplit le bloc « référencement » de l'en-tête de chaque page (adresse canonique, liens
     vers les autres langues, interdiction d'indexer tant que le site n'est pas en ligne) ;
  3. écrit maquette/<langue>/<page>.html pour chaque page et chaque fichier de langue ;
  4. écrit maquette/robots.txt et maquette/sitemap.xml ;
  5. signale les clés manquantes (le texte français est alors conservé).
"""
import html
import json
import re
import sys
from pathlib import Path

# ====== Réglages de mise en ligne ======
# Adresse du site, avec la barre oblique finale. Le jour de la mise en ligne, remplacer par
# l'adresse définitive (par exemple 'https://www.residenceletheatre.com/'), puis relancer le script.
ADRESSE_SITE = 'https://jimbo-77.github.io/Domaine-vaison/maquette/'
# False tant que le site est une maquette : les moteurs de recherche ne doivent pas l'indexer.
# Passer à True le jour de la mise en ligne définitive.
INDEXABLE = False

RACINE = Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'villacotepiscine.html', 'villa2terrasses.html']
DOSSIER_I18N = RACINE / 'i18n'
LANGUES = {'fr': 'Français', 'en': 'English', 'de': 'Deutsch', 'nl': 'Nederlands', 'es': 'Español'}

RE_CONTENU = re.compile(r'(<([a-zA-Z0-9]+)\b[^>]*\sdata-i18n="([^"]+)"[^>]*>)(.*?)(</\2>)', re.S)
RE_ATTRIBUT = re.compile(r'(\s([a-z-]+)=")([^"]*)(" data-i18n-\2="([^"]+)")')
RE_TEXTES = re.compile(r'(<script id="textes" type="application/json">\n)(.*?)(\n</script>)', re.S)
RE_REFERENCEMENT = re.compile(r'(<!-- référencement :[^\n]*-->\n)(.*?)(<!-- /référencement -->)', re.S)


def adresse(langue, nom):
    """Adresse publique d'une page, sans l'extension .html (les hébergeurs la servent ainsi)."""
    chemin = '' if nom == 'index.html' else nom[:-len('.html')]
    return ADRESSE_SITE + ('' if langue == 'fr' else f'{langue}/') + chemin


def bloc_referencement(langue, nom):
    lignes = [f'<link rel="canonical" href="{adresse(langue, nom)}">']
    lignes += [f'<link rel="alternate" hreflang="{code}" href="{adresse(code, nom)}">' for code in LANGUES]
    lignes.append(f'<link rel="alternate" hreflang="x-default" href="{adresse("fr", nom)}">')
    if not INDEXABLE:
        lignes.append('<meta name="robots" content="noindex, nofollow">')
    return '\n'.join(lignes) + '\n'


def referencer(page, langue, nom):
    if not RE_REFERENCEMENT.search(page):
        raise SystemExit(f'{nom} : bloc « référencement » introuvable dans l\'en-tête')
    return RE_REFERENCEMENT.sub(lambda m: m.group(1) + bloc_referencement(langue, nom) + m.group(3), page, count=1)


def robots_et_sitemap():
    if INDEXABLE:
        robots = f'User-agent: *\nAllow: /\n\nSitemap: {ADRESSE_SITE}sitemap.xml\n'
    else:
        robots = '# Maquette : rien ne doit être indexé. Voir INDEXABLE dans outils/traduire.py.\nUser-agent: *\nDisallow: /\n'
    (RACINE / 'robots.txt').write_text(robots, encoding='utf-8')
    urls = []
    for nom in PAGES:
        liens = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{code}" href="{adresse(code, nom)}"/>' for code in LANGUES)
        liens += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{adresse("fr", nom)}"/>'
        urls += [f'  <url>\n    <loc>{adresse(code, nom)}</loc>{liens}\n  </url>' for code in LANGUES]
    (RACINE / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(urls) + '\n</urlset>\n', encoding='utf-8')


def extraire(pages):
    """Rassemble les textes français de toutes les pages et signale les clés incohérentes."""
    textes, script = {}, None
    for nom, page in pages.items():
        trouves = [(m.group(3), m.group(4)) for m in RE_CONTENU.finditer(page)]
        trouves += [(m.group(5), html.unescape(m.group(3))) for m in RE_ATTRIBUT.finditer(page)]
        for cle, texte in trouves:
            if cle in textes and textes[cle] != texte:
                print(f'attention : la clé {cle} n\'a pas le même texte dans {nom}')
            textes.setdefault(cle, texte)
        bloc = json.loads(RE_TEXTES.search(page).group(2))
        if script is not None and bloc != script:
            print(f'attention : le bloc de textes du script de {nom} diffère de celui de index.html')
        script = script or bloc
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


def selecteur_langues(page, langue, nom):
    """Chaque option mène à la même page dans l'autre langue (adresse relative au dossier <langue>/)."""
    fichier = '' if nom == 'index.html' else nom
    def option(code):
        if code == langue:
            valeur = fichier or './'
        else:
            valeur = '../' + ('' if code == 'fr' else f'{code}/') + fichier
        choisi = ' selected' if code == langue else ''
        return f'<option value="{valeur}" lang="{code}"{choisi}>{LANGUES[code]}</option>'
    options = ''.join(option(c) for c in LANGUES)
    return re.sub(r'(<select [^>]*onchange="location\.href = this\.value">).*?(</select>)',
                  lambda m: m.group(1) + options + m.group(2), page, count=1, flags=re.S)


def generer(page, langue, nom, textes, script):
    page = RE_CONTENU.sub(lambda m: m.group(1) + textes.get(m.group(3), m.group(4)) + m.group(5), page)
    page = RE_ATTRIBUT.sub(
        lambda m: m.group(1) + html.escape(textes.get(m.group(5), html.unescape(m.group(3))), quote=True) + m.group(4), page)
    page = RE_TEXTES.sub(lambda m: m.group(1) + json.dumps(script, ensure_ascii=False, indent=2) + m.group(3), page)
    page = page.replace('<html lang="fr">', f'<html lang="{langue}">', 1)
    page = referencer(page, langue, nom)
    page = selecteur_langues(page, langue, nom)
    # La page traduite est un dossier plus bas : on remonte pour les fichiers communs.
    page = re.sub(r'(\s(?:src|href)=")(photos/|style\.css|site\.js)', r'\1../\2', page)
    page = page.replace('data-racine=""', 'data-racine="../"', 1)
    return page


def main():
    pages = {}
    for nom in PAGES:
        source = RACINE / nom
        page = source.read_text(encoding='utf-8')
        mise_a_jour = referencer(page, 'fr', nom)
        if mise_a_jour != page:
            source.write_text(mise_a_jour, encoding='utf-8')
        pages[nom] = mise_a_jour
    robots_et_sitemap()
    print(f'adresse du site : {ADRESSE_SITE} ; indexable : {"oui" if INDEXABLE else "non (maquette)"}')
    textes_fr, script_fr = extraire(pages)
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
        (RACINE / code).mkdir(exist_ok=True)
        for nom, page in pages.items():
            (RACINE / code / nom).write_text(generer(page, code, nom, textes, script), encoding='utf-8')
        print(f'{code} : {len(pages)} pages générées dans {(RACINE / code).relative_to(RACINE.parent)}/'
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
