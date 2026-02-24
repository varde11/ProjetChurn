# Churn Decision Intelligence App

> Une application de machine learning qui va au-delà de la simple prédiction de churn en intégrant la stratégie métier et l'optimisation du ROI.

**Démo en ligne:** [https://varde11-churn-frontend.hf.space/](https://varde11-churn-frontend.hf.space/)

---

## Vue d'ensemble du projet

La plupart des projets de churn s'arrêtent à la classification. Mais **prédire le churn ne suffit pas.**

Cette application transforme un modèle de churn classique en **système d'intelligence décisionnelle** qui répond à une question plus importante :

> **Est-il financièrement rentable d'agir ?**

### Capabilités principales

- ✓ **Prédiction de churn** – Modèles optimisés Précision & Rappel
- ✓ **Seuil de décision ajustable** – Contrôler la sensibilité des prédictions
- ✓ **Intégration métier** – Coût du churn, coût de rétention, taux de succès
- ✓ **Recommandations d'actions** – Stratégies de rétention personnalisées
- ✓ **Calcul du ROI** – Analyse d'impact financier
- ✓ **Simulation de portefeuille** – Optimisation de stratégie globale
- ✓ **Sélection automatique du seuil** – Découverte de la stratégie optimale

---

## Fonctionnalités clés

### 1 - Prédiction au niveau client

Pour un client sélectionné :
- Choisir le modèle d'optimisation (Précision / Rappel)
- Ajuster le seuil de décision
- Définir les hypothèses métier
- **Résultat :** Probabilité de churn + Actions recommandées + Gain financier attendu

### 2 - Simulation ROI au niveau portefeuille

Analyser l'impact de la stratégie sur l'ensemble de la clientèle :
- Comparer plusieurs seuils
- Calculer le ROI attendu par seuil
- Identifier automatiquement le seuil optimal
- Visualiser les gains via tableaux et courbes
- Identifier les clients à risque prioritaires

### 3 - Architecture

- **Backend :** FastAPI
- **Base de données :** PostgreSQL (Neon)
- **Frontend :** Streamlit
- **Orchestration :** Docker Compose
- **ML :** Modèles Scikit-learn (optimisés précision & rappel)

---

## Pourquoi ce projet est différent

**Un modèle avec 90% de précision peut quand même perdre de l'argent.**

Les projets ML traditionnels se concentrent sur les métriques. Ce système montre comment le ML doit intégrer :

1. **Contraintes métier** – Structures de coûts réels
2. **Modélisation financière** – Calcul de la valeur attendue
3. **Stratégie de décision** – Quand et comment agir

Il passe de *"prédire le churn"* → *"optimiser la stratégie d'action"*

---

## Stack technologique

| Composant | Technologie |
|-----------|------------|
| **Backend** | Python, FastAPI |
| **Frontend** | Streamlit |
| **ML** | Scikit-learn, Pandas |
| **Base de données** | PostgreSQL (Neon) / SQLite (dev) |
| **ORM** | SQLAlchemy |
| **Orchestration** | Docker Compose |
| **Déploiement** | Hugging Face Spaces |

---

## Structure du projet

```
ProjetChurn/
├── app/                      # Backend FastAPI
│   ├── main.py              # Routes API
│   ├── schema.py            # Modèles Pydantic
│   ├── db.py                # Session base de données
│   ├── table_structure.py   # Modèles SQLAlchemy
│   ├── logic.py             # Logique de prédiction
│   ├── decision_logic.py    # Logique ROI & actions
│   ├── model/               # Modèles ML sauvegardés
│   └── preprocessing/       # Scaler & encodeur
├── ui/                       # Frontend Streamlit
│   ├── app.py               # Page principale
│   └── pages/               # Pages des fonctionnalités
├── initdb/                   # Initialisation base de données
│   ├── 01create_table.sql   # Schéma
│   └── 02fill_table.sql     # Données d'exemple
├── test/                     # Tests Pytest
│   └── test_api.py          # Tests API
├── docker-compose.yml       # Orchestration des services
└── readme.md                # Ce fichier
```

---

## Démarrage rapide

### Prérequis

- Docker & Docker Compose
- Python 3.9+ (pour le développement local)

### Installation

1. **Cloner et naviguer**
   ```bash
   cd ProjetChurn
   ```

2. **Construire et démarrer les services**
   ```bash
   docker compose build --progress=plain
   docker compose up
   ```

3. **Accéder aux applications**
   - **Documentation API :** `http://localhost:8000/docs`
   - **Frontend :** `http://localhost:8501`

---

## Points terminaux API

### Gestion des clients

- `GET /GetClientByIdClient` – Récupérer un client spécifique
- `POST /AddClient` – Créer un nouveau client
- `DELETE /DeleteClientByIdClient` – Supprimer un client et ses prédictions

### Prédictions

- `POST /Decision` – **Point d'entrée principal** – Intelligence décisionnelle complète
  ```json
  {
    "id_client": 1,
    "option": "precision",
    "threshold": 0.5,
    "churn_cost": 500.0,
    "retention_cost": 50.0,
    "success_rate": 0.3
  }
  ```
- `GET /getPredictionByIdClient` – Lister les prédictions d'un client
- `GET /getPredictionByIdPrediction` – Récupérer une prédiction spécifique
- `DELETE /deletePredictionByIdPrediction` – Supprimer une prédiction

### Analytics

- `GET /GetAllClientByLabel` – Filtrer les clients par statut de churn

---

## Tests

Exécuter la suite de tests :

```bash
pytest test/test_api.py -v
```

---

## Améliorations futures

- [ ] Modélisation d'uplift avancée
- [ ] Apprentissage sensible aux coûts
- [ ] Sélection automatique des hyperparamètres pour le ROI
- [ ] Optimisation de stratégie multi-segment
- [ ] Intégration de framework de test A/B

---

## Auteur

**Vannel** – Ingénieur IA spécialisé en ML et Systèmes Décisionnels

