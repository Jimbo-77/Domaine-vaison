/* Script commun aux pages du site (accueil et pages des maisons).
   Les textes qu'il affiche sont dans le bloc <script id="textes"> de chaque page,
   traduits dans i18n/*.json (section "script"). */
const T = JSON.parse(document.getElementById('textes').textContent);
/* Les pages traduites sont un dossier plus bas : <body data-racine="../">. */
const PHOTOS = (document.body.dataset.racine || '') + 'photos/';
/* Lien vers le formulaire de contact (sur l'accueil pour les pages des maisons). */
const LIEN_CONTACT = document.body.dataset.contact || '#contact';
const remplir = (modele, valeurs) => modele.replace(/\{(\w+)\}/g, (_, k) => valeurs[k]);

/* ====== Configuration Smoobu ======
   Dans Smoobu : Paramètres > Booking Engine (moteur de réservation) > « Intégrer au site web ».
   Copiez l'adresse (src / url) du module « tous les logements » dans `toutes`,
   puis celle de chaque logement dans la maison correspondante.
   Tant qu'une adresse est vide, un encart d'attente s'affiche à la place. */
const SMOOBU = {
  toutes: '',
  olivier: '',
  lavande: '',
  cigales: '',
};

/* ====== Galeries ======
   Photos reprises des pages du site actuel (« Villa côté Piscine » pour Olivier et Lavande,
   « Villa les 2 Terrasses » pour Les Cigales). Grandes images : photos/site-actuel/,
   vignettes : photos/vignettes/ (mêmes noms de fichier). */
const GALERIES = {
  'olivier-lavande': [
    '1676558f1dcadd750df69defc4e16d6b',
    'b43e242cade5996541ba6e9c69d9f5f1',
    'acab24f7e5fa35498ca3f2d838189ca4',
    '1bbe75eccf3c669e7b0264b18bec25dd',
    '0bd4cf0e386fd8f8ccead8c2620ed2a8',
    '9c72197f964bf7e96d040866d01b06f8',
    '97548f86d54bb1ae1ce0378e1f556614',
    'residentheatre-11',
    'residentheatre-13',
    'residentheatre-16',
    'residentheatre-18',
    'residentheatre-19',
  ],
  cigales: [
    'residentheatre-25',
    'be8b8119b11970aa71271cd23073fc59',
    '5e3053176e2a2425d135e1fbb8cadc44',
    '9d833aa5a4ec348f3d3a9529076c95dc',
    '90883b51c77162f16da73cf929f9f2fd',
    '5b9ca37211e2e5999a2a4f4898e55eb6',
    'residentheatre-12',
    'residentheatre-15',
    'residentheatre-14',
    'residentheatre-20',
    'residentheatre-17',
  ],
  domaine: [
    'SAM_3534_1080',
    'SAM_2168_1080',
    'SAM_2128_1080',
    'SAM_2117_1080',
    'SAM_2122_1080',
    'SAM_2109_1080',
    'residentheatre-34',
    'residentheatre-21',
  ],
};

const visionneuse = document.getElementById('visionneuse');
const vImg = visionneuse.querySelector('figure img');
let galerieOuverte = null, indexPhoto = 0;

function afficherPhoto(i) {
  const photos = GALERIES[galerieOuverte];
  indexPhoto = (i + photos.length) % photos.length;
  const fichier = photos[indexPhoto], legende = T.legendes[fichier];
  vImg.src = PHOTOS + 'site-actuel/' + fichier + '.webp';
  vImg.alt = legende;
  visionneuse.querySelector('.visionneuse-legende').textContent = legende;
  visionneuse.querySelector('.visionneuse-compteur').textContent = remplir(T.compteur, { n: indexPhoto + 1, total: photos.length });
  [1, -1].forEach(d => { new Image().src = PHOTOS + 'site-actuel/' + photos[(indexPhoto + d + photos.length) % photos.length] + '.webp'; });
}

function ouvrirGalerie(nom, i = 0) {
  galerieOuverte = nom;
  visionneuse.querySelector('.visionneuse-titre').textContent = T.galeries[nom];
  afficherPhoto(i);
  visionneuse.showModal();
}

visionneuse.querySelector('.precedente').addEventListener('click', () => afficherPhoto(indexPhoto - 1));
visionneuse.querySelector('.suivante').addEventListener('click', () => afficherPhoto(indexPhoto + 1));
visionneuse.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft') afficherPhoto(indexPhoto - 1);
  if (e.key === 'ArrowRight') afficherPhoto(indexPhoto + 1);
});
let toucheX = null;
vImg.addEventListener('touchstart', e => { toucheX = e.touches[0].clientX; }, { passive: true });
vImg.addEventListener('touchend', e => {
  if (toucheX === null) return;
  const dx = e.changedTouches[0].clientX - toucheX;
  if (Math.abs(dx) > 40) afficherPhoto(indexPhoto + (dx < 0 ? 1 : -1));
  toucheX = null;
});

/* data-vignettes="nom" : 4 vignettes et un bouton « Voir les N photos » ;
   avec data-tout : toutes les vignettes, en grille. */
document.querySelectorAll('[data-vignettes]').forEach(zone => {
  const nom = zone.dataset.vignettes, photos = GALERIES[nom], tout = 'tout' in zone.dataset;
  (tout ? photos : photos.slice(0, 4)).forEach((fichier, i) => {
    const b = document.createElement('button');
    b.className = 'vignette';
    b.setAttribute('aria-label', remplir(T.agrandir, { legende: T.legendes[fichier] }));
    b.innerHTML = `<img src="${PHOTOS}vignettes/${fichier}.webp" alt="" width="360" height="270" loading="lazy">`;
    b.addEventListener('click', () => ouvrirGalerie(nom, i));
    zone.appendChild(b);
  });
  if (tout) return;
  const bouton = document.createElement('button');
  bouton.className = 'tout-voir';
  bouton.textContent = remplir(nom === 'domaine' ? T.voir_photos_domaine : T.voir_photos, { n: photos.length });
  bouton.addEventListener('click', () => ouvrirGalerie(nom));
  zone.appendChild(bouton);
});
document.querySelectorAll('.photo-galerie').forEach(b => b.addEventListener('click', () => ouvrirGalerie(b.dataset.galerie)));

const NOMS = T.maisons;
const cadre = document.getElementById('resa-frame');

function afficherVilla(villa) {
  if (!cadre) return;
  document.querySelectorAll('.onglets button').forEach(b => b.setAttribute('aria-selected', b.dataset.villa === villa));
  const url = SMOOBU[villa] || SMOOBU.toutes;
  if (url) {
    cadre.innerHTML = '';
    const f = document.createElement('iframe');
    f.src = url;
    f.title = remplir(T.titre_reservation, { maison: NOMS[villa] });
    f.loading = 'lazy';
    cadre.appendChild(f);
  } else {
    cadre.innerHTML = `<div class="resa-vide">
      <h3>${T.attente_titre}</h3>
      <p>${remplir(T.attente_texte, { maison: villa === 'toutes' ? T.attente_maison_choix : NOMS[villa] })}</p>
      <a class="btn" href="${LIEN_CONTACT}">${T.attente_bouton}</a></div>`;
  }
}

function ouvrirReservation(villa) {
  afficherVilla(villa);
  document.getElementById('reservation').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
}

function envoyerDemande(form) {
  form.querySelector('.confirmation').textContent = T.demande_envoyee;
  form.querySelector('button').disabled = true;
}

function basculerMenu(btn) {
  const ouvert = document.getElementById('nav').classList.toggle('ouvert');
  btn.setAttribute('aria-expanded', ouvert);
}

document.querySelectorAll('.onglets button').forEach(b => b.addEventListener('click', () => afficherVilla(b.dataset.villa)));
document.querySelectorAll('#nav ul a').forEach(a => a.addEventListener('click', () => {
  document.getElementById('nav').classList.remove('ouvert');
  document.querySelector('.menu-btn').setAttribute('aria-expanded', false);
}));
afficherVilla(cadre ? cadre.dataset.villa || 'toutes' : 'toutes');

/* Carte OpenStreetMap chargée seulement à la demande (poids et vie privée). */
function afficherCarte() {
  const zone = document.getElementById('carte');
  const f = document.createElement('iframe');
  f.className = 'carte';
  f.src = zone.dataset.src;
  f.title = zone.title;
  zone.replaceWith(f);
}

/* Bandeau de suggestion de langue : si le navigateur du visiteur préfère une autre langue
   disponible, on lui propose la même page dans cette langue, sans jamais le rediriger.
   Le choix est mémorisé (changement de langue ou fermeture du bandeau). */
const MEMOIRE_LANGUE = 'langue-choisie';
function memoriserLangue(code) {
  try { localStorage.setItem(MEMOIRE_LANGUE, code); } catch (e) { /* stockage indisponible : sans conséquence */ }
}
function langueMemorisee() {
  try { return localStorage.getItem(MEMOIRE_LANGUE); } catch (e) { return null; }
}
document.querySelectorAll('a[hreflang]').forEach(a => a.addEventListener('click', () => memoriserLangue(a.getAttribute('hreflang'))));
(function proposerLangue() {
  const bloc = document.getElementById('suggestion-langue');
  if (!bloc || langueMemorisee()) return;
  const disponibles = JSON.parse(bloc.textContent);
  const langueDeLaPage = document.documentElement.lang;
  let choix = null;
  for (const preference of navigator.languages || [navigator.language || '']) {
    const code = preference.toLowerCase().split('-')[0];
    if (code === langueDeLaPage) return;          // le visiteur lit déjà sa langue préférée
    if (disponibles[code]) { choix = code; break; }
  }
  if (!choix) return;
  const s = disponibles[choix];
  const bandeau = document.createElement('div');
  bandeau.className = 'suggestion-langue';
  bandeau.lang = choix;
  bandeau.innerHTML = `<p></p><a hreflang="${choix}"></a><button type="button"><span aria-hidden="true">×</span></button>`;
  bandeau.querySelector('p').textContent = s.texte;
  const lien = bandeau.querySelector('a');
  lien.href = s.href;
  lien.textContent = s.lien;
  lien.addEventListener('click', () => memoriserLangue(choix));
  const fermer = bandeau.querySelector('button');
  fermer.setAttribute('aria-label', s.fermer);
  fermer.addEventListener('click', () => { memoriserLangue(langueDeLaPage); bandeau.remove(); });
  document.body.prepend(bandeau);
})();

/* Menu des langues : se ferme au clic ailleurs ou avec Échap. */
const langues = document.querySelector('.langues');
if (langues) {
  document.addEventListener('click', e => { if (!langues.contains(e.target)) langues.open = false; });
  langues.addEventListener('keydown', e => { if (e.key === 'Escape') { langues.open = false; langues.querySelector('summary').focus(); } });
}

const entete = document.querySelector('header');
const ctaMobile = document.querySelector('.cta-mobile');
const ouverture = document.querySelector('.ouverture, .entete-maison');
addEventListener('scroll', () => {
  entete.classList.toggle('defile', scrollY > 8);
  if (ctaMobile && ouverture) ctaMobile.classList.toggle('visible', ouverture.getBoundingClientRect().bottom < 0);
}, { passive: true });
