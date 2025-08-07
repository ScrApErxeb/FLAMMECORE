# 🔥 FlammeCore — Le Cerveau Numérique Hybride

**FlammeCore** est un agent intelligent extensible, auto-apprenant, conçu pour fonctionner localement et via le cloud.
Il apprend en continu grâce à ses interactions avec l’utilisateur et le monde, et peut exécuter des actions via des plugins dynamiques.

---

## ✨ Fonctionnalités Clés

- 🧠 Traitement d’entrée utilisateur (`gomde`) → encodage (`porte`) → réponse
- 🗂️ Mémoire vectorielle pour contextualiser et apprendre
- ⚖️ Balancer pour décider entre exécution locale, plugin ou appel cloud
- 🔌 Plugins Python/JS pour fonctions autonomes (ex : météo, résumé, calculs)
- 📡 Signals pour interagir avec le monde (API, objets, scripts)
- 📊 Historique complet des actions pour audit et amélioration

---

## 🚀 Objectifs à court terme

- [x] Dictionnaire de données défini
- [ ] MVP V1 : gomde → porte → réponse + mémoire
- [ ] Plugins simples (résumé texte, météo)
- [ ] Balancer local/cloud
- [ ] Interface CLI ou Web simple

---

## 🛠️ Installation (dev en local)

```bash
git clone https://github.com/your-user/FlammeCore.git
cd FlammeCore
pip install -r requirements.txt
```

> ⚠️ Ce projet utilise Python 3.10+ et (bientôt) Node.js pour les plugins JS.

---

## 📁 Structure du projet

```
flammecore/
├── core/           # Traitement logique de l’agent
├── memory/         # Moteur de mémoire vectorielle
├── plugins/        # Fonctions autonomes
├── balancer/       # Module de routage
├── signals/        # Communication avec le monde
├── interface/      # CLI ou Web (React)
├── data/           # YAML/JSON de config
└── utils/          # Aides diverses
```

---

## 🤝 Contribution

> Ce projet est personnel mais pourra être ouvert à contribution plus tard.  
Propose une idée, ouvre une issue, ou balance une PR stylée 🔥

---

## 🧠 Créé par flamme + ChatGPT  
Un duo homme/machine pour construire un cerveau libre et lucide.

