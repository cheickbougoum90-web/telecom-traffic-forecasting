# Crée les labels, jalons (milestones) et issues de départ du projet.
# Prérequis : GitHub CLI installé (gh) et authentifié (gh auth login).
# Usage (depuis la racine du dépôt, dépôt déjà poussé sur GitHub) :
#   powershell -ExecutionPolicy Bypass -File .\scripts\create_issues.ps1

$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)

# ---------- Labels ----------
$labels = @(
    @{ n = "data";          c = "0e8a16"; d = "Données et prétraitement" },
    @{ n = "eda";           c = "1d76db"; d = "Analyse exploratoire" },
    @{ n = "modélisation";  c = "5319e7"; d = "Modèles de prévision" },
    @{ n = "évaluation";    c = "fbca04"; d = "Métriques et comparaison" },
    @{ n = "api";           c = "d93f0b"; d = "API FastAPI" },
    @{ n = "docker";        c = "0052cc"; d = "Conteneurisation" },
    @{ n = "documentation"; c = "c5def5"; d = "README, rapport, figures" }
)
foreach ($l in $labels) {
    gh label create $l.n --color $l.c --description $l.d --force | Out-Null
}

# ---------- Jalons ----------
$milestones = @(
    @{ t = "E0 Cadrage et données";           d = "Dépôt, données Telecom Italia, chargement et agrégation" },
    @{ t = "E1 Exploration";                  d = "EDA : tendance, saisonnalités, anomalies" },
    @{ t = "E2 Baseline et modèles statistiques"; d = "Naïf saisonnier, SARIMA, Prophet" },
    @{ t = "E3 Modèles ML et deep learning";  d = "XGBoost, LSTM, comparaison finale" },
    @{ t = "E4 API et Docker";                d = "Service FastAPI conteneurisé" },
    @{ t = "E5 Documentation";                d = "README FR/EN, rapport, figures, publication" }
)
foreach ($m in $milestones) {
    gh api repos/:owner/:repo/milestones -f title="$($m.t)" -f description="$($m.d)" 2>$null | Out-Null
}

# ---------- Issues ----------
$issues = @(
    @{ t = "Télécharger et documenter les données Telecom Italia"; m = "E0 Cadrage et données"; l = "data,documentation";
       b = "* [ ] Télécharger les fichiers (DOI 10.7910/DVN/EGZHFV) dans data/raw/`n* [ ] Vérifier le format réel des colonnes`n* [ ] Compléter docs/donnees.md (source, licence, période, limites)" },
    @{ t = "Ajuster le chargeur et agréger en séries horaires"; m = "E0 Cadrage et données"; l = "data";
       b = "* [ ] Adapter src/data/load.py au format réel`n* [ ] Séries zone entière et cellules choisies (centre et périphérie)`n* [ ] Sauvegarde dans data/processed/`n* [ ] Test unitaire à jour" },
    @{ t = "Explorer la tendance et les saisonnalités"; m = "E1 Exploration"; l = "eda";
       b = "* [ ] Profils journalier et hebdomadaire`n* [ ] Décomposition (tendance, saisonnalité, résidu)`n* [ ] ACF et PACF`n* [ ] Figures dans reports/figures/" },
    @{ t = "Détecter valeurs manquantes et anomalies"; m = "E1 Exploration"; l = "eda,data";
       b = "* [ ] Trous dans la série`n* [ ] Jours atypiques (fêtes, événements)`n* [ ] Décision de traitement justifiée" },
    @{ t = "Définir le protocole de validation temporelle"; m = "E2 Baseline et modèles statistiques"; l = "évaluation";
       b = "* [ ] Découpage train/test chronologique`n* [ ] Validation glissante (walk-forward)`n* [ ] Métriques : MAE, RMSE, MAPE`n* [ ] Horizon(s) de prévision justifié(s)" },
    @{ t = "Modèle de référence : naïf saisonnier"; m = "E2 Baseline et modèles statistiques"; l = "modélisation,évaluation";
       b = "* [ ] Utiliser src/models/baseline.py`n* [ ] Scores de référence à battre" },
    @{ t = "SARIMA"; m = "E2 Baseline et modèles statistiques"; l = "modélisation";
       b = "* [ ] Tests de stationnarité`n* [ ] Choix des ordres justifié (ACF/PACF, AIC)`n* [ ] Diagnostic des résidus" },
    @{ t = "Prophet"; m = "E2 Baseline et modèles statistiques"; l = "modélisation";
       b = "* [ ] Saisonnalités journalière et hebdomadaire`n* [ ] Effet des jours spéciaux`n* [ ] Évaluation sur le même protocole" },
    @{ t = "XGBoost avec variables retardées"; m = "E3 Modèles ML et deep learning"; l = "modélisation";
       b = "* [ ] Variables calendaires et lags (src/features/build.py)`n* [ ] Réglage des hyperparamètres sans fuite de données`n* [ ] Importance des variables" },
    @{ t = "LSTM"; m = "E3 Modèles ML et deep learning"; l = "modélisation";
       b = "* [ ] Fenêtrage et normalisation (ajustée sur le train uniquement)`n* [ ] Entraînement et courbes de perte`n* [ ] Évaluation sur le même protocole" },
    @{ t = "Comparer les modèles et choisir le meilleur"; m = "E3 Modèles ML et deep learning"; l = "évaluation";
       b = "* [ ] Tableau comparatif (précision, temps d'entraînement, complexité)`n* [ ] Analyse des erreurs aux heures de pointe`n* [ ] Choix argumenté et sauvegarde dans models/" },
    @{ t = "API de prévision FastAPI"; m = "E4 API et Docker"; l = "api";
       b = "* [ ] Endpoint /forecast (horizon en paramètre)`n* [ ] Validation des entrées`n* [ ] Test de l'API" },
    @{ t = "Conteneuriser avec Docker"; m = "E4 API et Docker"; l = "docker";
       b = "* [ ] Dockerfile fonctionnel`n* [ ] Instructions de lancement dans le README" },
    @{ t = "Rédiger les README FR et EN et finaliser"; m = "E5 Documentation"; l = "documentation";
       b = "* [ ] Résultats chiffrés et figures`n* [ ] Limites (valeurs relatives, données de 2013)`n* [ ] README.en.md synchronisé`n* [ ] Ajout au portfolio" }
)
foreach ($i in $issues) {
    gh issue create --title $i.t --body $i.b --label $i.l --milestone $i.m | Out-Null
    Write-Host "Issue créée : $($i.t)"
}
Write-Host "Terminé."
