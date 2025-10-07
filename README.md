# 🏋️ Güdlft - Plateforme de Réservation pour Compétitions Régionales

## 🎯 Présentation du Projet

**Güdlft Regional** est une application web développée avec **Flask** qui permet aux clubs de force régionaux de gérer les inscriptions aux compétitions de manière équitable et transparente.

> ⚡ **Statut du projet** : Phase 1 terminée • Phase 2 terminée • Tests et débogages terminées

## 🎓 Contexte de l'Exercice

### Mission :
En tant que développeur chez Güdlft, nous devions :
- **🔍 Déboguer** l'application existante de la Phase 1
- **🧪 Implémenter** une suite de tests complète (TDD)
- **🚀 Développer** les fonctionnalités de la Phase 2

## GUDLFT Regional - Documentation

## Phase 1 - Espace Club 

- Tableau de bord club
- Système de réservation intelligent
- Messages d'erreur gérés
- Gestion des sessions

## Phase 2 - Fonctionnalités Publiques

- Tableau public des points
- Optimisation des performances

## Installation & Démarrage

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

### 🚀 Installation Express

```bash
# 1. Cloner le projet
git clone 
cd gudlft-regional

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python -m flask run
```

L'application sera accessible sur : http://localhost:5000

## 📁 Structure du Projet

```text
gudlft-regional/
├── app.py                 # Application Flask principale
├── clubs.json            # Base de données des clubs
├── competitions.json     # Base de données des compétitions
├── requirements.txt      # Dépendances Python
├── tests/               # Suite de tests complète
└── templates/           # Templates HTML
    ├── index.html       # Page de connexion
    ├── welcome.html     # Tableau de bord
    ├── booking.html     # Page de réservation
    └── points.html      # Tableau public des points
```

## Tour de l'Application

### 1. Page d'Accueil (/)

- Interface de connexion simple avec email
- Validation des emails existants dans la base
- Redirection vers le tableau de bord personnel

### 2. Tableau de Bord (/board)

```python
# Données affichées :
- Club: "Iron Legends"
- Points: 25
- Compétitions à venir:
  * "Spring Festival" (13 places disponibles)
  * "Fall Classic" (20 places disponibles)
```

### 3. Réservation de Places (/book/competition_name)

- Sélection du nombre de places (1-12 max)
- Vérification en temps réel des contraintes
- Confirmation avec mise à jour immédiate des points

### 4. Tableau Public (/points)

- Classement de tous les clubs
- Affichage des points disponibles
- Accessible sans connexion

### 📊 Métriques de Qualité

- Couverture de code : > 60% visé
- Temps de réponse : < 5s (compétitions), < 2s (points)
- Tests automatisés : pytest 

## Développement & Bonnes Pratiques

###  Conventions de Code

#### Gestion des Branches

```bash
# Types de branches
feature/tableau-points-public    # Nouvelle fonctionnalité
bug/email-issue       # Correction de bug
```

#### Méthodologie TDD

```python
# Cycle Red-Green-Refactor
1. Écrire un test qui échoue (Red)
2. Implémenter le code minimal pour passer (Green)  
3. Optimiser et nettoyer le code (Refactor)
```

## 🐛 Débogage et Résolution de Problèmes

## 🚀 Performance et Optimisation

### Contraintes

- 6 utilisateurs simultanés minimum
- Temps de chargement < 5 secondes
- Mises à jour < 2 secondes

### Ressources Utiles

📚 Documentation Flask : https://flask.palletsprojects.com/

🧪 Documentation pytest : https://docs.pytest.org/

📊 Documentation Locust : https://docs.locust.io/

### Workflow de Contribution

```bash
# 1. Créer une branche
git checkout -b feature/ma-nouvelle-fonctionnalite

# 2. Développer avec tests
# 3. Vérifier la couverture
pytest --cov=app

# 4. Tests de performance
locust --headless -u 6 -r 2

# 5. Merge après validation
git checkout master
git merge feature/ma-nouvelle-fonctionnalite
```

---

