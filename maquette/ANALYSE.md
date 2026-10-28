# Analyse de residenceletheatre.com & proposition de maquette

> Analyse mise à jour en octobre 2026 à partir du site lui-même (pages, `llms-full.txt`, galerie).

## 1. Ce que propose le site actuel

| Élément | Constat |
|---|---|
| **Offre** | « Résidence Le Théâtre Antique », 100 chemin du Brusquet, 84110 Vaison-la-Romaine. À deux pas du Théâtre antique, à 300 m du centre-ville. Ouvert toute l'année. Accueil par M. Brygo. |
| **Logements** | 3 maisons pour 4 personnes. **Olivier** et **Lavande** : jumelles, 55 m², lit double 140 × 190 + deux lits jumeaux 90 × 190, baignoire, terrasse privée (vue sur la piscine pour Lavande seulement) (page « Villa côté Piscine »). **Les Cigales** : 65 m², même couchage, douche, pas de lave-vaisselle, deux terrasses sud et est, lit d'appoint possible (page « Villa les 2 Terrasses »). *Salles de bain, lave-vaisselle et vue sur la piscine corrigés par le propriétaire, le site actuel étant inexact sur ces points.* |
| **Équipements** | Piscine 10 × 5 m, jardin, parking fermé, boulodrome, Wi-Fi gratuits ; barbecue et boules prêtés sur demande ; panier d'accueil. |
| **Tarifs (semaine)** | Olivier ou Lavande : 700 € / 800 € / 900 € ; Les Cigales : 750 € / 850 € / 950 € (basse / moyenne / haute saison). Minimum 3 jours en basse et moyenne saison, 1 semaine en haute saison. |
| **Frais** | Ménage obligatoire 50 €, draps et serviettes en option, lit bébé et chaise haute 15 €/séjour, animal 25 €/séjour, taxe de séjour 1,70 €/adulte/jour. |
| **Contact** | 06 32 51 56 29, domaine.letheatreantique@gmail.com. |
| **Pages** | Accueil, Les villas (2 pages), Galerie, Tarifs, Aux alentours, Contact & Accès. FR / EN. Réservation par formulaire de demande, sans disponibilités en ligne. |
| **Avis** | Deux avis Google repris sur l'accueil. |
| **Photos** | 33 photos de la résidence (intérieurs, terrasses, piscine, jardin) et 11 des environs. |

## 2. Points faibles relevés

1. **Noms confus** : le menu annonce « Nos deux villas » (Côté Piscine, Les 2 Terrasses) alors qu'il y a trois maisons (Olivier, Lavande, Les Cigales) ; la page tarifs parle de « deux villas d'exception » et le tableau en liste trois.
2. **Informations contradictoires** : arrivée à 16 h (pages villas) ou 16 h 30 (tarifs) ; départ 9 h–10 h ou 8 h 30–10 h ; la moyenne saison inclut juin, la haute saison aussi (« Juin à Août »).
3. **Pas de disponibilités en ligne** : le visiteur envoie une demande sans savoir si ses dates sont libres.
4. **Atout principal peu visible** : la proximité du Théâtre antique et du centre n'est pas montrée dès le premier écran.
5. **Avis clients** peu exploités (deux avis, sans lien vers la fiche Google).

## 3. Proposition : `maquette/index.html`

Page d'accueil unique, responsive, autonome :

- **Ouverture** : promesse « Trois maisons à deux pas du Théâtre antique », trois repères (théâtre, centre-ville à 300 m, piscine) et trois photos en arcs romains.
- **Les maisons** : une fiche pour Olivier et Lavande, une pour Les Cigales, avec les vraies photos, surfaces, couchages et prix.
- **Sur place** : équipements compris, photo de la piscine.
- **Autour** : à pied et en voiture, d'après la page « Aux alentours ».
- **Tarifs** : grille par saison et par maison, ce qui est compris, les frais en plus.
- **Réserver** : onglets Olivier / Lavande / Les Cigales prêts pour le moteur Smoobu (voir `SMOOBU.md`).
- **Avis** : les deux avis Google.
- **Contact** : carte OpenStreetMap de l'emplacement réel, téléphone, e-mail, itinéraire, formulaire.

**Identité visuelle** (revue avec le plugin *frontend-design*) :
- élément signature : l'ouverture en trois arcs romains (piscine, maison sous l'olivier, terrasse sur le jardin), qui se lèvent au chargement ;
- palette : blanc de chaux `#F8F8F4`, pierre `#D9D0C1`, vert de volet `#2F5D62`, eau du bassin `#8EC5C9`, ombre `#1F2A2C`, soleil `#E0A43A` ;
- typographies : *Marcellus* (titres, inspirée des inscriptions romaines) et *Commissioner* (texte) ;
- photos dans des cadres en arc romain ; une seule animation (le lever des arcs), désactivée si l'utilisateur limite les animations.

## 4. À valider avec le propriétaire avant mise en ligne

- [ ] Nom de marque : « Domaine Vaison » (nom du repo) ou « Résidence Le Théâtre Antique » (nom actuel)
- [ ] Horaires d'arrivée et de départ (la maquette reprend ceux des pages villas : 16 h ; 9 h–10 h)
- [ ] Périodes exactes de moyenne et haute saison (juin apparaît dans les deux sur le site actuel)
- [ ] Prix des draps et serviettes en option
- [ ] Licence des photos touristiques (voir `photos/README.md`)
- [ ] Orthographe des avis cités (légèrement corrigée dans la maquette)

## 5. Étapes suivantes suggérées

1. Valider la maquette et les contenus.
2. Pages détail par maison avec galerie (les photos sont déjà dans `photos/site-actuel/`).
3. Brancher Smoobu.
4. Version anglaise, SEO local (données structurées `LodgingBusiness`, fiche Google Business).
