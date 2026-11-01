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
  2. remplit, dans chaque page, le bloc « référencement » de l'en-tête (adresse canonique, liens
     vers les autres langues, aperçu de partage, icônes, données structurées, interdiction
     d'indexer tant que le site n'est pas en ligne) et le bloc « langues » du menu ;
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
# Bandeau proposant la page dans la langue du navigateur du visiteur (affiché par site.js).
# Il est rédigé dans la langue proposée, quelle que soit la langue de la page : (phrase, lien, fermer).
SUGGESTIONS = {
    'fr': ('Cette page existe aussi en français.', 'Voir la page en français', 'Fermer'),
    'en': ('This page is also available in English.', 'View in English', 'Close'),
    'de': ('Diese Seite gibt es auch auf Deutsch.', 'Auf Deutsch ansehen', 'Schließen'),
    'nl': ('Deze pagina bestaat ook in het Nederlands.', 'Bekijken in het Nederlands', 'Sluiten'),
    'es': ('Esta página también está disponible en español.', 'Ver en español', 'Cerrar'),
}

RE_CONTENU = re.compile(r'(<([a-zA-Z0-9]+)\b[^>]*\sdata-i18n="([^"]+)"[^>]*>)(.*?)(</\2>)', re.S)
RE_ATTRIBUT = re.compile(r'(\s([a-z-]+)=")([^"]*)(" data-i18n-\2="([^"]+)")')
RE_TEXTES = re.compile(r'(<script id="textes" type="application/json">\n)(.*?)(\n</script>)', re.S)
RE_REFERENCEMENT = re.compile(r'(<!-- référencement :[^\n]*-->\n)(.*?)(<!-- /référencement -->)', re.S)
RE_LANGUES = re.compile(r'(<!-- langues :[^\n]*-->\n)(.*?)(<!-- /langues -->)', re.S)
RE_SUGGESTION = re.compile(r'(<!-- suggestion :[^\n]*-->\n)(.*?)(<!-- /suggestion -->)', re.S)

# Informations de l'établissement, reprises dans les données structurées (schema.org).
NOM_SITE = 'Résidence Le Théâtre Antique'
TELEPHONE = '+33 6 32 51 56 29'
EMAIL = 'domaine.letheatreantique@gmail.com'
ADRESSE_POSTALE = {'@type': 'PostalAddress', 'streetAddress': '100 chemin du Brusquet', 'postalCode': '84110',
                   'addressLocality': 'Vaison-la-Romaine', 'addressRegion': "Provence-Alpes-Côte d'Azur", 'addressCountry': 'FR'}
GPS = {'@type': 'GeoCoordinates', 'latitude': 44.2445258, 'longitude': 5.0774152}
LOCALES = {'fr': 'fr_FR', 'en': 'en_GB', 'de': 'de_DE', 'nl': 'nl_NL', 'es': 'es_ES'}
# Par page : suffixe des clés de titre et de description, image de partage (fichier, largeur, hauteur, clé du texte alternatif).
FICHES = {
    'index.html': ('', ('accueil-piscine.jpg', 1400, 933, 'alt_accueil_piscine')),
    'villacotepiscine.html': ('_ol', ('olivier-lavande.jpg', 1200, 829, 'alt_ol')),
    'villa2terrasses.html': ('_ci', ('cigales.jpg', 1200, 800, 'alt_ci')),
}
# Maisons décrites sur chaque page : (ancre, nom, surface en m²).
MAISONS = {
    'villacotepiscine.html': [('olivier', 'Olivier', 55), ('lavande', 'Lavande', 55)],
    'villa2terrasses.html': [('cigales', 'Les Cigales', 65)],
}
EQUIPEMENTS = ['eq_piscine', 'eq_jardin', 'eq_boulodrome', 'eq_barbecue', 'eq_parking', 'eq_wifi']


def adresse(langue, nom):
    """Adresse publique d'une page, sans l'extension .html (les hébergeurs la servent ainsi)."""
    chemin = '' if nom == 'index.html' else nom[:-len('.html')]
    return ADRESSE_SITE + ('' if langue == 'fr' else f'{langue}/') + chemin


def brut(texte):
    """Texte sans balises ni entités, pour les attributs et les données structurées."""
    return html.unescape(re.sub(r'<[^>]+>', '', texte)).strip()


def attribut(texte):
    return html.escape(texte, quote=True)


def donnees_structurees(langue, nom, textes):
    suffixe, (image, *_) = FICHES[nom]
    equipements = [{'@type': 'LocationFeatureSpecification', 'name': brut(textes[cle]), 'value': True} for cle in EQUIPEMENTS]
    residence = {'@type': 'LodgingBusiness', '@id': ADRESSE_SITE + '#residence', 'name': NOM_SITE,
                 'url': adresse(langue, 'index.html'), 'telephone': TELEPHONE, 'email': EMAIL,
                 'address': ADRESSE_POSTALE, 'geo': GPS}
    if nom == 'index.html':
        maisons = [f'{adresse(langue, page)}#{ancre}' for page, liste in MAISONS.items() for ancre, _, _ in liste]
        residence.update({'description': brut(textes['meta_description']), 'image': ADRESSE_SITE + 'photos/' + image,
                          'priceRange': '700 € – 950 €', 'checkinTime': '16:00', 'checkoutTime': '10:00',
                          'petsAllowed': True, 'amenityFeature': equipements,
                          'containsPlace': [{'@id': m} for m in maisons]})
        return {'@context': 'https://schema.org', '@graph': [residence]}
    graphe = [residence]
    for ancre, nom_maison, surface in MAISONS[nom]:
        graphe.append({'@type': 'House', '@id': f'{adresse(langue, nom)}#{ancre}', 'name': f'{nom_maison}, {NOM_SITE}',
                       'description': brut(textes['meta_description' + suffixe]), 'url': adresse(langue, nom),
                       'image': ADRESSE_SITE + 'photos/' + image,
                       'floorSize': {'@type': 'QuantitativeValue', 'value': surface, 'unitCode': 'MTK'},
                       'numberOfBedrooms': 2, 'numberOfBathroomsTotal': 1,
                       'occupancy': {'@type': 'QuantitativeValue', 'maxValue': 4},
                       'petsAllowed': True, 'amenityFeature': equipements,
                       'containedInPlace': {'@id': ADRESSE_SITE + '#residence'}})
    nom_page = brut(textes['ol_titre']) if nom == 'villacotepiscine.html' else 'Les Cigales'
    graphe.append({'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': brut(textes['fil_accueil']), 'item': adresse(langue, 'index.html')},
        {'@type': 'ListItem', 'position': 2, 'name': nom_page, 'item': adresse(langue, nom)}]})
    return {'@context': 'https://schema.org', '@graph': graphe}


def bloc_referencement(langue, nom, textes):
    suffixe, (image, largeur, hauteur, cle_alt) = FICHES[nom]
    prefixe = '' if langue == 'fr' else '../'
    titre, description = brut(textes['meta_titre' + suffixe]), brut(textes['meta_description' + suffixe])
    lignes = [f'<link rel="canonical" href="{adresse(langue, nom)}">']
    lignes += [f'<link rel="alternate" hreflang="{code}" href="{adresse(code, nom)}">' for code in LANGUES]
    lignes.append(f'<link rel="alternate" hreflang="x-default" href="{adresse("fr", nom)}">')
    if not INDEXABLE:
        lignes.append('<meta name="robots" content="noindex, nofollow">')
    lignes += [
        f'<link rel="icon" href="{prefixe}favicon.svg" type="image/svg+xml">',
        f'<link rel="icon" href="{prefixe}favicon-32.png" sizes="32x32" type="image/png">',
        f'<link rel="apple-touch-icon" href="{prefixe}apple-touch-icon.png">',
        '<meta name="theme-color" content="#2f5d62">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{attribut(NOM_SITE)}">',
        f'<meta property="og:title" content="{attribut(titre)}">',
        f'<meta property="og:description" content="{attribut(description)}">',
        f'<meta property="og:url" content="{adresse(langue, nom)}">',
        f'<meta property="og:image" content="{ADRESSE_SITE}photos/{image}">',
        f'<meta property="og:image:width" content="{largeur}">',
        f'<meta property="og:image:height" content="{hauteur}">',
        f'<meta property="og:image:alt" content="{attribut(brut(textes[cle_alt]))}">',
        f'<meta property="og:locale" content="{LOCALES[langue]}">',
    ]
    lignes += [f'<meta property="og:locale:alternate" content="{LOCALES[code]}">' for code in LANGUES if code != langue]
    lignes.append('<meta name="twitter:card" content="summary_large_image">')
    lignes.append('<script type="application/ld+json">\n'
                  + json.dumps(donnees_structurees(langue, nom, textes), ensure_ascii=False, indent=1) + '\n</script>')
    return '\n'.join(lignes) + '\n'


def lien_relatif(langue, nom, code):
    """Adresse relative, depuis la page `nom` en `langue`, de la même page en `code`."""
    fichier = '' if nom == 'index.html' else nom
    if code == langue:
        return fichier or './'
    if langue == 'fr':
        return f'{code}/{fichier}'
    return '../' + ('' if code == 'fr' else f'{code}/') + fichier


def bloc_suggestion(langue, nom):
    donnees = {code: {'href': lien_relatif(langue, nom, code), 'texte': texte, 'lien': lien, 'fermer': fermer}
               for code, (texte, lien, fermer) in SUGGESTIONS.items() if code != langue}
    return ('<script id="suggestion-langue" type="application/json">'
            + json.dumps(donnees, ensure_ascii=False) + '</script>\n')


def bloc_langues(langue, nom):
    """Menu des langues en vrais liens : chacun mène à la même page dans l'autre langue."""
    def lien(code):
        href = lien_relatif(langue, nom, code)
        courant = ' aria-current="page"' if code == langue else ''
        return f'      <li><a href="{href}" hreflang="{code}" lang="{code}"{courant}>{LANGUES[code]}</a></li>'
    # Le libellé « Langue » (traduit) est dans la page, juste avant ce bloc : id="titre-langues".
    return ('    <details class="langues">\n'
            f'      <summary aria-describedby="titre-langues">{LANGUES[langue]}</summary>\n'
            '      <ul>\n' + '\n'.join(lien(c) for c in LANGUES) + '\n      </ul>\n'
            '    </details>\n')


def remplir_blocs(page, langue, nom, textes):
    for motif, nom_bloc, contenu in ((RE_REFERENCEMENT, 'référencement', bloc_referencement(langue, nom, textes)),
                                     (RE_LANGUES, 'langues', bloc_langues(langue, nom)),
                                     (RE_SUGGESTION, 'suggestion', bloc_suggestion(langue, nom))):
        if not motif.search(page):
            raise SystemExit(f'{nom} : bloc « {nom_bloc} » introuvable')
        page = motif.sub(lambda m: m.group(1) + contenu + m.group(3), page, count=1)
    return page


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


def generer(page, langue, nom, textes, script):
    page = RE_CONTENU.sub(lambda m: m.group(1) + textes.get(m.group(3), m.group(4)) + m.group(5), page)
    page = RE_ATTRIBUT.sub(
        lambda m: m.group(1) + html.escape(textes.get(m.group(5), html.unescape(m.group(3))), quote=True) + m.group(4), page)
    page = RE_TEXTES.sub(lambda m: m.group(1) + json.dumps(script, ensure_ascii=False, indent=2) + m.group(3), page)
    page = page.replace('<html lang="fr">', f'<html lang="{langue}">', 1)
    page = remplir_blocs(page, langue, nom, textes)
    # La page traduite est un dossier plus bas : on remonte pour les fichiers communs.
    page = re.sub(r'(\s(?:src|href)=")(photos/|polices/|style\.css|site\.js)', r'\1../\2', page)
    page = re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + re.sub(r'(^|, )photos/', r'\1../photos/', m.group(1)) + '"', page)
    page = page.replace('data-racine=""', 'data-racine="../"', 1)
    return page


def main():
    pages = {nom: (RACINE / nom).read_text(encoding='utf-8') for nom in PAGES}
    textes_fr, script_fr = extraire(pages)
    for nom, page in pages.items():
        mise_a_jour = remplir_blocs(page, 'fr', nom, textes_fr)
        if mise_a_jour != page:
            (RACINE / nom).write_text(mise_a_jour, encoding='utf-8')
        pages[nom] = mise_a_jour
    robots_et_sitemap()
    print(f'adresse du site : {ADRESSE_SITE} ; indexable : {"oui" if INDEXABLE else "non (maquette)"}')
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
