# Mothra Front-end

Interface utilisateur pour le projet Mothra - Détection des maladies de la peau par IA.

## 🚀 Technologies

- **React 18** - Framework UI
- **Vite** - Build tool ultra-rapide
- **TailwindCSS** - Framework CSS utility-first
- **React Router** - Navigation côté client

## 📦 Installation

```bash
npm install
```

## 🎯 Lancement

### Mode développement
```bash
npm run dev
```

Le site sera accessible sur [http://localhost:5173](http://localhost:5173)

### Build production
```bash
npm run build
```

### Preview du build
```bash
npm run preview
```

## 📁 Structure du projet

```
src/
├── components/
│   ├── Navbar.jsx       # Barre de navigation
│   └── Footer.jsx       # Pied de page
├── pages/
│   ├── Home.jsx         # Page d'accueil
│   ├── Account.jsx      # Page compte utilisateur
│   ├── Dashboard.jsx    # Dashboard des analyses
│   └── Diagnostic.jsx   # Page de diagnostic
├── assets/              # Images et ressources
├── App.jsx              # Composant principal avec routing
├── main.jsx             # Point d'entrée
└── index.css            # Styles globaux Tailwind
```

## 🎨 Design System

### Couleurs
- **Background principal**: `#F5F1E8` (beige)
- **Texte principal**: `#000000`
- **Boutons primaires**: Noir avec texte blanc
- **Boutons secondaires**: `#E5E5E5` (gris clair)
- **Cartes**: Blanc avec ombre

### Responsive
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 📄 Pages

### 1. Home (`/`)
- Hero section avec CTA
- Section "L'avenir du diagnostic médical"
- 3 cartes (Scientifique, Utilisateur, Visionnaire)

### 2. Account (`/account`)
- Informations utilisateur
- Image de profil (homme de Vitruve)
- Section RGPD et protection des données

### 3. Dashboard (`/dashboard`)
- Liste des diagnostics effectués
- Statistiques (nombre d'analyses, confiance moyenne)
- Cards avec images et résultats

### 4. Diagnostic (`/diagnostic`)
- Zone d'upload d'image (drag & drop)
- Analyse en temps réel
- Affichage des résultats avec niveau de confiance
- Recommandations

## 🔗 Navigation

- `/` - Page d'accueil
- `/account` - Compte utilisateur
- `/dashboard` - Dashboard des analyses
- `/diagnostic` - Effectuer un diagnostic

## 🎯 Fonctionnalités

### Implémentées
- ✅ Navigation responsive avec menu burger
- ✅ 4 pages complètes
- ✅ Upload d'images (drag & drop)
- ✅ Simulation d'analyse ML
- ✅ Affichage des résultats
- ✅ Design system cohérent
- ✅ Footer avec liens sociaux

### À venir (intégration Back-end)
- [ ] Connexion/Inscription réelle
- [ ] Appel API pour les diagnostics
- [ ] Sauvegarde des analyses en BD
- [ ] Récupération de l'historique utilisateur
- [ ] Export des données (RGPD)
- [ ] Gestion du profil utilisateur

## 🔧 Configuration

### TailwindCSS

Les couleurs personnalisées sont définies dans `tailwind.config.js`:

```js
colors: {
  'beige': '#F5F1E8',
  'gray-light': '#E5E5E5',
}
```

## 📸 Images

Les images utilisent des placeholders d'Unsplash. Remplacez-les par vos vraies images.

## 🤝 Intégration avec le Back-end

Le back-end FastAPI tourne sur `http://localhost:8000`.

## 📝 License

Projet Mothra © 2025
