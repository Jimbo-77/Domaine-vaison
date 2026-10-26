# Brancher la réservation Smoobu

La maquette contient une section **Réservation en ligne** (`#reservation`), avec un onglet par villa.
Elle affiche le moteur de réservation Smoobu (Booking Engine) : disponibilités en temps réel
(synchronisées avec Airbnb, Booking.com, etc.), calcul du prix et paiement en ligne.

## 1. Côté Smoobu

1. Activer et configurer le **Booking Engine** : photos, descriptions, tarifs, séjour minimum,
   moyens de paiement (Stripe / PayPal), conditions d'annulation, langues.
2. Aller dans **Booking Engine > Intégrer au site web**
   (aide Smoobu : « How to integrate Smoobu booking engine into my external site »).
3. Récupérer :
   - le code du module **pour tous les logements** ;
   - le code du module **pour chaque logement** (une villa = un logement Smoobu).

## 2. Côté site

Dans `maquette/index.html`, en bas du fichier, remplir l'objet `SMOOBU` avec l'adresse
(attribut `src` ou `url` du code fourni par Smoobu) de chaque module :

```js
const SMOOBU = {
  toutes: 'https://login.smoobu.com/…',   // module tous logements
  olivier: 'https://login.smoobu.com/…',  // Villa Olivier
  lavande: 'https://login.smoobu.com/…',  // Villa Lavande
  cigales: 'https://login.smoobu.com/…',  // Villa Les Cigales
};
```

- Une villa laissée vide affiche le module « toutes les villas ».
- Si tout est vide, un encart « Module Smoobu à connecter » renvoie vers le formulaire de contact.
- Les boutons « Réserver » et « Dates libres » des fiches ouvrent directement l'onglet de la bonne villa.

Si Smoobu fournit un code JavaScript (et non une simple adresse d'iframe), envoyez-le-moi :
je l'intégrerai tel quel dans la section, à la place de l'iframe.

## 3. Pour aller plus loin (optionnel)

- **Calendrier de disponibilité seul** (sans réservation) sur une future page détail de villa :
  Smoobu > Avancé > *Calendar iFrame*.
- **API Smoobu** (disponibilités/prix affichés dans le design du site, ex. « dès 450 € » mis à jour
  automatiquement) : nécessite un petit serveur pour protéger la clé d'API — GitHub Pages
  seul ne suffit pas.
