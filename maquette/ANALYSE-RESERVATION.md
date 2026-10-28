# Analyse de la réservation sur residenceletheatre.com

> Analyse faite le 28 octobre 2026 sur le site en ligne (pages `/reservation`, `/en/book`, accueil,
> pages villas, script `app.js`). Le formulaire a été rempli dans un navigateur de test **sans être
> envoyé** : aucune demande n'est partie chez le propriétaire.

## 1. Comment ça marche aujourd'hui

- **Ce n'est pas un moteur de réservation** : c'est un formulaire qui envoie un e-mail au
  propriétaire (`POST /reservation`, module « resamail » du CMS My Groom Service). Il n'y a ni
  disponibilités, ni prix, ni paiement, ni confirmation immédiate.
- **Accès** : le bouton « Réserver » de l'en-tête mène à `/reservation` (onglet « Réservation » de la
  page Contact & Accès). Le même formulaire figure sur la page d'accueil. Les pages des villas n'ont
  qu'un lien vers `/reservation` : le choix de la villa est perdu en route.
- **Deux étapes** :
  1. arrivée, départ, nombre d'adultes (1 à 6), nombre d'enfants (0 à 5), villa
     (« Villa Olivier et Villa Lavande » ou « Villa Les Cigales »), bouton « Réserver » ;
  2. nom, téléphone, e-mail, bouton « Demande de réservation », case RGPD obligatoire.
- **Calendrier** : sélecteur de dates flatpickr, au format jj/mm/aaaa, à partir d'aujourd'hui ;
  la date de départ doit suivre l'arrivée. Aucune autre règle.
- **Version anglaise** (`/en/book`) : même formulaire traduit, boutons « Book now » puis
  « Booking request ».

## 2. Problèmes constatés

### Les règles de location ne sont pas appliquées

| Règle (page Tarifs) | Ce que le formulaire accepte | Vérifié |
|---|---|---|
| 3 jours minimum (basse et moyenne saison), 1 semaine en haute saison | une seule nuit, même en juillet | oui |
| 4 personnes par maison | jusqu'à 6 adultes et 5 enfants, soit 11 personnes | oui |
| Dates déjà louées | toutes les dates futures sont sélectionnables : aucune disponibilité affichée | oui |
| Olivier et Lavande sont deux maisons | un seul choix « Villa Olivier et Villa Lavande » | oui |

### Des demandes incomplètes ou fausses

- **Arrivée pré-remplie avec la date du jour** (le 28/10/2026 lors du test) : si le visiteur ne la
  modifie pas, la demande porte sur aujourd'hui.
- **Pas de champ message** : impossible de signaler un animal (25 €), un lit bébé ou une chaise haute
  (15 €), le linge en option ou une arrivée tardive, alors que ces options figurent dans les tarifs.
- **L'âge des enfants n'est pas demandé** : on ne sait pas s'il faut un lit bébé.
- **Aucun prix** : ni tarif de la période, ni ménage obligatoire (50 €), ni taxe de séjour.
  Le visiteur envoie une demande sans connaître le montant.

### Une expérience confuse

- **« Réserver » / « Book now » promettent une réservation**, alors que le visiteur n'envoie
  qu'une demande, sans savoir ce qui suit (délai de réponse, devis, acompte).
- **Les intitulés sont dans les champs** (« Nom* », « Arrivée* ») et disparaissent à la saisie ;
  le choix de la villa s'intitule « Selectionnez...* ».
- **La case RGPD obligatoire est placée sous le bouton d'envoi**, en petit texte gris clair sur fond
  gris : peu lisible, facile à manquer, d'où un refus à l'envoi.
- **Le bandeau cookies recouvre le bouton et la case**, sur ordinateur comme sur mobile, tant qu'il
  n'est pas fermé.
- **Aucun message de confirmation décrit** après l'envoi (non testé, pour ne pas envoyer de demande).

### Technique et conformité

- **Pas de protection anti-spam sur le formulaire de réservation** : le reCAPTCHA invisible ne
  protège que le formulaire de contact.
- **Pas de synchronisation de calendrier** (iCal ou gestionnaire de canaux) avec Airbnb,
  Booking.com, etc. : les doubles réservations doivent être évitées à la main.
- **Consentement RGPD imposé** : la case est obligatoire pour envoyer la demande, alors qu'une
  demande de réservation relève plutôt des mesures précontractuelles ; le texte ne précise ni la
  finalité ni la durée de conservation. À faire valider.
- **Dépendance au prestataire** du site (CMS My Groom Service) : formulaire et données non
  exportables simplement.

## 3. Recommandations

### Cible : un vrai moteur de réservation (Smoobu, déjà prévu dans la maquette)

Le Booking Engine de Smoobu règle la plupart des problèmes, à condition de le paramétrer :

- **trois logements distincts** : Olivier, Lavande, Les Cigales ;
- **capacité maximale de 4 personnes**, lit bébé en plus ;
- **séjour minimum par saison** : 3 nuits en basse et moyenne saison, 7 en haute saison ;
  jour d'arrivée imposé l'été si souhaité ;
- **tarifs par saison**, ménage obligatoire de 50 €, taxe de séjour de 1,70 € par adulte et par
  nuit ;
- **options payantes** : animal 25 €, lit bébé et chaise haute 15 €, linge ;
- **acompte ou paiement en ligne**, confirmation immédiate par e-mail ;
- **synchronisation des calendriers** avec les autres plateformes (Smoobu est un gestionnaire de
  canaux) ;
- **langues** du moteur alignées sur celles du site (FR, EN, DE, NL, ES).

### En attendant Smoobu : une demande de réservation fiable

Si le formulaire de demande reste en service quelque temps (sur l'ancien site ou dans la maquette) :

1. Intitulés visibles au-dessus des champs ; aucune date pré-remplie.
2. Contrôles avant l'envoi : séjour minimum selon la saison, 4 personnes maximum.
3. Choix séparés : Olivier, Lavande, Les Cigales, ou « peu importe ».
4. Champ message et cases pour les options (animal, lit bébé, linge, arrivée tardive) ;
   enfants de moins de 2 ans comptés à part.
5. Récapitulatif avant l'envoi avec un prix estimé : semaine(s) de la saison, ménage, options,
   taxe de séjour.
6. Bouton « Envoyer ma demande » (et non « Réserver ») et texte « Réponse sous 24 h, aucun
   paiement à cette étape ».
7. Mention d'information RGPD courte au-dessus du bouton, sans case obligatoire.
8. Protection anti-spam (champ piège invisible ou reCAPTCHA).

### Dans la maquette

- La section « Réserver » est prête pour Smoobu (`SMOOBU.md`).
- **Le formulaire « Nous écrire » de la maquette n'envoie rien pour l'instant** : il faut le
  brancher (Smoobu, ou un service d'envoi de formulaire) avant toute mise en ligne.
- Le site actuel demande le téléphone : à ajouter au formulaire de la maquette si le propriétaire
  rappelle ses clients.
