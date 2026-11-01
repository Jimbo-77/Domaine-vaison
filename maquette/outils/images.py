#!/usr/bin/env python3
"""Recrée les images WebP du site à partir des photos JPEG.

À lancer après avoir remplacé ou ajouté une photo, depuis la racine du dépôt :
    python3 maquette/outils/images.py

- Photos des pages (maquette/photos/<nom>.jpg) : trois largeurs, <nom>-480.webp, -800.webp et
  -1200.webp, que le navigateur choisit selon l'écran (attributs srcset et sizes des pages).
- Photos des galeries (liste GALERIES de site.js) : <nom>.webp dans photos/site-actuel/ et
  dans photos/vignettes/, à côté des JPEG d'origine.
Nécessite la bibliothèque Pillow (pip install Pillow).
"""
import re
from pathlib import Path
from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
PHOTOS = RACINE / 'photos'
PHOTOS_PAGES = ['accueil-piscine', 'accueil-olivier', 'accueil-terrasse', 'entree', 'olivier-lavande', 'cigales', 'pont-romain']
LARGEURS = (480, 800, 1200)


def webp(source, destination, largeur=None, qualite=78):
    image = Image.open(source).convert('RGB')
    if largeur and image.width > largeur:
        image = image.resize((largeur, round(image.height * largeur / image.width)), Image.LANCZOS)
    image.save(destination, 'WEBP', quality=qualite, method=6)


def main():
    for nom in PHOTOS_PAGES:
        for largeur in LARGEURS:
            webp(PHOTOS / f'{nom}.jpg', PHOTOS / f'{nom}-{largeur}.webp', largeur)
        print(f'{nom} : {", ".join(f"{l} px" for l in LARGEURS)}')
    script = (RACINE / 'site.js').read_text(encoding='utf-8')
    bloc = script[script.index('const GALERIES'):script.index('};', script.index('const GALERIES'))]
    noms = sorted(set(re.findall(r"'([A-Za-z0-9_-]+)'", bloc)) - {'olivier-lavande', 'cigales', 'domaine'})
    for nom in noms:
        webp(PHOTOS / 'site-actuel' / f'{nom}.jpg', PHOTOS / 'site-actuel' / f'{nom}.webp', qualite=76)
        webp(PHOTOS / 'vignettes' / f'{nom}.jpg', PHOTOS / 'vignettes' / f'{nom}.webp', qualite=72)
    print(f'galeries : {len(noms)} photos et leurs vignettes')


if __name__ == '__main__':
    main()
