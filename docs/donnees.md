# Données

Source : Telecom Italia Big Data Challenge, jeu « Telecommunications, SMS, Call, Internet, MI »
(Harvard Dataverse, DOI 10.7910/DVN/EGZHFV). Activité issue des CDR (Call Detail Records), agrégée par
cellule d'une grille couvrant Milan, par intervalle de 10 minutes, de novembre à décembre 2013.

## Format des fichiers (vérifié sur les fichiers du 1er au 3 novembre 2013)

Un fichier par jour, texte séparé par tabulations, sans en-tête :

| Colonne | Contenu |
|---|---|
| cell_id | identifiant de la cellule de la grille |
| timestamp | début de l'intervalle de 10 min, en millisecondes epoch, UTC |
| country_code | code pays de l'interlocuteur (0 pour les non identifiés, 39 pour l'Italie, etc.) |
| sms_in, sms_out | activité SMS reçus et envoyés |
| call_in, call_out | activité d'appels reçus et émis |
| internet | activité de connexion Internet |

Particularités :
* Les lignes sont creuses : un champ vide ou absent signifie aucune activité pour cette mesure.
* Il y a une ligne par cellule, par intervalle et par code pays : le trafic d'une cellule est la somme sur les codes pays.
* Les timestamps sont en UTC : le 1er novembre commence à 23:00 UTC la veille. On convertit en heure de Milan (Europe/Rome) avant toute analyse de profil journalier.
* Les valeurs sont proportionnelles au trafic réel, avec un facteur d'échelle gardé secret par l'opérateur : on prévoit une activité relative, pas des Mo.

## Obtention

Téléchargement manuel depuis Harvard Dataverse, fichiers placés dans data/raw/ (non versionnés).
Ensuite : `python scripts/prepare_data.py` produit data/processed/traffic_zone_1h.csv.
