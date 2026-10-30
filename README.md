# Prévision du trafic télécom (séries temporelles)

Projet de data science : prévoir l'activité Internet d'un réseau mobile avec ARIMA/SARIMA, Prophet,
XGBoost et LSTM, puis exposer le meilleur modèle via une API FastAPI conteneurisée.

> Version anglaise : [README.en.md](README.en.md)

## Problématique
Comment anticiper la charge d'un réseau mobile pour dimensionner et planifier la capacité ?

## Données
Voir [docs/donnees.md](docs/donnees.md).

## Structure du dépôt
```
data/raw, data/processed   données brutes et nettoyées (non versionnées)
notebooks/                 exploration, modélisation
src/data, features, models, api   code réutilisable
models/                    modèles entraînés (non versionnés)
reports/figures/           graphiques pour le rapport
tests/                     tests unitaires
```

## Méthodologie
1. Exploration (tendance, saisonnalité journalière et hebdomadaire, valeurs aberrantes)
2. Modèle de référence (naïf saisonnier)
3. SARIMA, Prophet, XGBoost, LSTM
4. Validation temporelle (pas de mélange aléatoire) et comparaison MAE, RMSE, MAPE
5. API FastAPI et Docker

## Résultats
À compléter.

## Lancer le projet
```
pip install -r requirements.txt
pytest
uvicorn src.api.main:app --reload
```
