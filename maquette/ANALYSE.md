# Analyse de residenceletheatre.com & proposition de maquette

> Remarque : le site n'était pas accessible directement depuis l'environnement de travail (réseau filtré).
> Cette analyse repose sur son contenu indexé par les moteurs de recherche et sur les fiches
> des annuaires touristiques (Provence Guide / Vaucluse Tourisme, Charme & Traditions, gites.fr).

## 1. Ce que propose le site actuel

| Élément | Constat |
|---|---|
| **Offre** | Résidence de villas de vacances, 100 chemin du Brusquet, 84110 Vaison-la-Romaine, face au Théâtre antique. Ouvert toute l'année. |
| **Logements** | 2 ou 3 villas selon les pages (« deux villas d'exception » sur la page tarifs, « one of the 3 villas » en anglais). Pages connues : *Villa les 2 Terrasses*, *Côté Piscine*. Villa type : ~65 m², 2 chambres (1 lit double + 2 lits simples), 4 pers. + lit bébé, salon ouvert sur terrasse et jardin, cuisine équipée. |
| **Équipements** | Piscine, Wi-Fi, jardin, parking fermé, boulodrome (gratuits) ; espace barbecue ; animaux acceptés (supplément par séjour). |
| **Tarifs (2025, annuaires)** | ~450 €/semaine en basse saison, ~800 €/semaine en juillet-août. |
| **Pages** | Accueil, villas, Tarifs, Booking (réservation par téléphone / e-mail / formulaire, pas de réservation en ligne), Contact & Accès. Versions FR / EN. |
| **Contact** | Plusieurs numéros et e-mails différents selon les pages et les annuaires (incohérence). |

## 2. Points faibles relevés

1. **Informations incohérentes** : nombre de villas, numéros de téléphone et e-mails divergent d'une page à l'autre → perte de confiance et de demandes.
2. **Pas de réservation / disponibilité en ligne** : le visiteur doit appeler ou écrire sans savoir si les dates sont libres.
3. **Proposition de valeur peu visible** : l'atout n°1 (vue sur le Théâtre antique, centre-ville à pied, piscine dans un domaine clos) n'est pas mis en avant dès le premier écran.
4. **Structure technique datée** (URLs du type `index.php/en?lg=1`), peu favorable au référencement et au partage.
5. **Tarifs peu lisibles** : pas de grille claire par saison ni de liste « compris / en option ».
6. **Avis clients** peu exploités alors qu'ils sont un levier majeur de conversion.

## 3. Proposition : `maquette/index.html`

Une page d'accueil « one-page » responsive (mobile d'abord), autonome (HTML + CSS, sans dépendance), qui :

- **Hero plein écran** avec promesse claire : *« Vos villas face au Théâtre antique »* + 2 CTA.
- **Barre de disponibilité** (dates, voyageurs, villa) visible immédiatement — prête à être branchée sur un moteur de réservation (Lodgify, Amenitiz, Elloha, Gîtes de France Open System…) ou un simple formulaire.
- **Le domaine** : texte d'ambiance + chiffres clés.
- **Nos villas** : une carte par villa (capacité, surface, points forts, prix « dès »).
- **Équipements** : grille d'icônes (piscine, jardin, boulodrome, barbecue, parking, Wi-Fi).
- **Vaison-la-Romaine** : la destination et les distances clés.
- **Tarifs** : grille par saison + « compris / en option ».
- **Avis** : emplacements pour de vrais avis clients.
- **Contact & accès** : coordonnées uniques, plan de situation, formulaire de demande.
- **CTA collant sur mobile** « Vérifier les disponibilités ».
- Menu multilingue FR / EN / DE / NL (clientèle étrangère importante en Vaucluse).

**Identité visuelle** (revue avec le plugin *frontend-design*) :
- élément signature : un plan dessiné en ouverture (hémicycle du théâtre, chemin du Brusquet, domaine, piscine, trajet vers le centre) qui montre la promesse « en face du Théâtre antique » ;
- palette : blanc de chaux `#F8F8F4`, pierre `#D9D0C1`, vert de volet `#2F5D62`, eau du bassin `#8EC5C9`, ombre `#1F2A2C`, soleil `#E0A43A` ;
- typographies : *Marcellus* (titres, inspirée des inscriptions romaines) et *Commissioner* (texte) ;
- photos à fournir dans des cadres en arc romain ; une seule animation (les gradins qui se dessinent), désactivée si l'utilisateur limite les animations.

## 4. À valider avec le propriétaire avant mise en ligne

- [ ] Nom de marque : « Domaine Vaison » (nom du repo) ou conserver « Résidence le Théâtre »
- [ ] Nombre exact de villas et leurs noms — *« Villa l'Olivier » est un nom provisoire inventé pour la maquette*
- [ ] Caractéristiques de chaque villa (climatisation, jardin privatif, etc. sont des **exemples**)
- [ ] Grille tarifaire réelle (le tarif « 550 € » en moyenne saison et les durées minimales sont des **hypothèses**)
- [ ] Téléphone et e-mail de référence uniques
- [ ] Photos professionnelles (hero piscine + Théâtre au coucher du soleil, chaque villa, jardin, environs)
- [ ] Vrais avis clients
- [ ] Temps de trajet / distances (indicatifs)

## 5. Étapes suivantes suggérées

1. Valider la maquette et les contenus.
2. Pages détail par villa (galerie, plan, calendrier de disponibilité).
3. Choisir l'outil de réservation et le brancher sur la barre de disponibilité.
4. Traductions EN / DE / NL, SEO local (balises, données structurées `LodgingBusiness`, fiche Google Business).
