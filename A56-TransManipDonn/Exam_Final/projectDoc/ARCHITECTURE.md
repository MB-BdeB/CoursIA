# 🏗️ ARCHITECTURE DU PROJET - SENTIMENT CLASSIFIER

## Flux Data Complet (De gauche à droite)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PIPELINE ML - SENTIMENT CLASSIFIER                  │
└─────────────────────────────────────────────────────────────────────────┘

INPUT: Tweet brut
  │
  ├─→ Text Preprocessing (Étape 2)
  │   ├─ Supprimer URLs:       "http://..." → ""
  │   ├─ Supprimer mentions:   "@user" → ""
  │   ├─ Supprimer ponctuation: "!" "." "?" → ""
  │   ├─ Minuscules:           "HATE" → "hate"
  │   └─ Normaliser espaces:   "  " → " "
  │
  ├─→ Vectorisation TF-IDF (Étape 3)
  │   ├─ Unigrams:       "hate" "speech" "offensive"
  │   ├─ Bigrams:        "hate speech" "offensive language"
  │   └─ Output:         vecteur (9,573 dimensions)
  │
  ├─→ Feature Selection (Étape 5)
  │   ├─ Chi-Carré (χ²):    Mesure dépendance feature/target
  │   ├─ SelectKBest(k=5000): Garde seulement les 5000 meilleures
  │   └─ Output:            vecteur (5,000 dimensions)
  │
  ├─→ Classification (Étape 4)
  │   ├─ Model: BernoulliNB(binarize=0.0)
  │   └─ Output: Score de probabilité pour chaque classe
  │
  └─→ OUTPUT: Classe prédite
      ├─ 0 = Hate Speech
      ├─ 1 = Offensive Language
      └─ 2 = Neither

```

---

## Modèles Testés vs Résultats

```
┌────────────────────────┬──────────┬──────────┬──────────────┐
│ Modèle Testé           │ Accuracy │ F1-Score │ Status       │
├────────────────────────┼──────────┼──────────┼──────────────┤
│ Base (TF-IDF brut)     │  87.45%  │  0.8618  │ ✓ Baseline   │
│ SelectKBest χ²         │  87.90%  │  0.8696  │ ✅ MEILLEUR  │
│ SelectKBest + ROS      │  83.48%  │  0.8528  │ ❌ Pire      │
│ SelectKBest + RUS      │  80.23%  │  0.8313  │ ❌ Pire      │
└────────────────────────┴──────────┴──────────┴──────────────┘
```

---

## Arborescence Fichiers

```
Exam_Final/
│
├── 📂 CODE PYTHON & ML (4 fichiers - 33.7 KB)
│   ├── sentiment_classifier.py              [14.7 KB] - Code complet
│   ├── quick_start.py                       [9.3 KB]  - Copy-paste
│   ├── generate_visualizations.py           [10 KB]   - Graphiques
│   └── sentiment_classifier_pipeline.pkl    [1.1 MB]  - Modèle ML
│
├── 📊 VISUALISATIONS (6 fichiers PNG - 1.3 MB)
│   ├── 1_metrics_comparison.png             [398 KB]  ← 4 modèles comparés
│   ├── 2_class_distribution.png             [171 KB]  ← ROS, RUS, Normal
│   ├── 3_f1_by_class.png                    [168 KB]  ← Hate/Offensive/Neither
│   ├── 4_confusion_matrix.png               [172 KB]  ← Erreurs détaillées
│   ├── 5_summary_table.png                  [129 KB]  ← Tableau récap
│   └── sentiment_comparison.png             [242 KB]  ← Vue globale
│
├── 📄 RAPPORTS MARKDOWN (5 fichiers - 60 KB)
│   ├── ⚡_START_HERE.txt                     [2 KB]   - LIS CECI EN PREMIER!
│   ├── PROJET_TERMINÉ.md                    [9 KB]   - Conclusion générale
│   ├── RÉSUMÉ_FINAL.md                      [8.8 KB] - À retenir
│   ├── INDEX.md                             [10.7 KB]- Navigation
│   ├── RAPPORT_SENTIMENT_CLASSIFIER.md      [8.1 KB] - Technique
│   └── GUIDE_COMPLET.md                     [12.1 KB]- Explications + amélio
│
└── 📥 DATA (1 fichier - 2.5 MB)
    └── labeled_data.csv                     [2.5 MB] - 24,783 tweets

TOTAL: 16 fichiers créés / 4 MB
```

---

## Étapes Exécution

```
INPUT: labeled_data.csv (24,783 tweets)
│
├─→ ÉTAPE 1: Chargement & Exploration
│   ├─ Lire le CSV
│   ├─ Analyser la distribution (77% Offensive, 17% Neither, 6% Hate)
│   └─ Détecter le déséquilibre (ratio 13.42x)  ⚠️
│
├─→ ÉTAPE 2: Prétraitement du Texte
│   ├─ Nettoyer 24,783 tweets
│   ├─ Supprimer URLs, mentions, ponctuation
│   └─ Output: 24,783 tweets propres
│
├─→ ÉTAPE 3: Vectorisation TF-IDF
│   ├─ Transformer texte → vecteurs
│   ├─ Unigrams + Bigrams (1-2)
│   └─ Output: Matrice (24,783 x 9,573)
│
├─→ ÉTAPE 4: Modèle de Base
│   ├─ Diviser: Train (19,826) / Test (4,957)
│   ├─ Entraîner: BernoulliNB sur TF-IDF brut
│   ├─ Évaluer: Accuracy 87.45%, F1 0.8618
│   └─ Résultat: ✓ Baseline établie
│
├─→ ÉTAPE 5: Sélection de Caractéristiques
│   ├─ Appliquer SelectKBest(chi2, k=5000)
│   ├─ Réduire: 9,573 → 5,000 features
│   ├─ Ré-entraîner sur features réduites
│   ├─ Évaluer: Accuracy 87.90%, F1 0.8696
│   └─ Résultat: ✅ MEILLEUR (+0.78% F1)
│
├─→ ÉTAPE 6: Équilibrage A - ROS
│   ├─ RandomOverSampler: Dupliquer minoritaires
│   ├─ Nouveau train: 15,352 par classe
│   ├─ Ré-entraîner & Évaluer
│   ├─ Accuracy 83.48%, F1 0.8528
│   └─ Résultat: ❌ Pire (Trade-off: ↑Recall ↓Accuracy)
│
├─→ ÉTAPE 7: Équilibrage B - RUS
│   ├─ RandomUnderSampler: Supprimer majoritaires
│   ├─ Nouveau train: 1,144 par classe
│   ├─ Ré-entraîner & Évaluer
│   ├─ Accuracy 80.23%, F1 0.8313
│   └─ Résultat: ❌ Bien pire (Perte de données)
│
├─→ ÉTAPE 8: Comparaison
│   ├─ Comparer 4 modèles
│   ├─ Créer tableau récapitulatif
│   └─ Résultat: SelectKBest χ² = MEILLEUR
│
├─→ ÉTAPE 9: Pipeline Final
│   ├─ Combiner: TF-IDF + SelectKBest + BernoulliNB
│   ├─ Entraîner sur tout le train set
│   ├─ Tester sur test set
│   └─ Sauvegarder: sentiment_classifier_pipeline.pkl
│
├─→ ÉTAPE 10: Visualisations
│   ├─ Générer 6 graphiques PNG
│   ├─ 300 DPI (prêts pour présentation)
│   └─ Résultat: 1.3 MB PNG files
│
└─→ OUTPUT: Résultats & Rapports
    ├─ 4 rapports Markdown détaillés
    ├─ Modèle sauvegardé réutilisable
    ├─ Graphiques professionnels
    └─ Code modulaire & commenté
```

---

## Structure du Code

```
sentiment_classifier.py (2,500 lignes)
│
├─ Imports & Setup (30 lignes)
│
├─ ÉTAPE 1: Exploration (150 lignes)
│  └─ print(df.shape, df['class'].value_counts(), etc.)
│
├─ ÉTAPE 2: Preprocessing (100 lignes)
│  └─ def clean_tweet(tweet): regex + lower + strip
│
├─ ÉTAPE 3: Vectorisation (80 lignes)
│  └─ TfidfVectorizer(ngram_range=(1,2), max_features=10k)
│
├─ ÉTAPE 4: Modèle Base (100 lignes)
│  └─ BernoulliNB.fit() → y_pred → metrics
│
├─ ÉTAPE 5: SelectKBest (100 lignes)
│  └─ SelectKBest(chi2, k=5000) → fit_transform → metrics
│
├─ ÉTAPE 6: ROS (100 lignes)
│  └─ RandomOverSampler → fit_resample → metrics
│
├─ ÉTAPE 7: RUS (100 lignes)
│  └─ RandomUnderSampler → fit_resample → metrics
│
├─ ÉTAPE 8: Comparaison (200 lignes)
│  └─ DataFrame(results) → visualisation
│
├─ ÉTAPE 9: Pipeline (150 lignes)
│  └─ Pipeline([TF-IDF, SelectKBest, BernoulliNB]) → save
│
├─ ÉTAPE 10: Tests (80 lignes)
│  └─ predict(test_tweets) → afficher résultats
│
└─ Comments (800 lignes)
```

---

## Performance par Classe (SelectKBest)

```
CLASS 0: Hate Speech ⚠️ (286 samples)
├─ Precision: 0.41  ← Beaucoup de faux positifs
├─ Recall: 0.20     ← Peu de vrais positifs détectés
├─ F1-Score: 0.27   ← Très faible
└─ Problème: Classe minoritaire (5.8%), confusion avec "Offensive"

CLASS 1: Offensive Language ✅ (3,838 samples)
├─ Precision: 0.91  ← Très bon
├─ Recall: 0.94     ← Excellent
├─ F1-Score: 0.93   ← Très excellent
└─ Raison: Classe majoritaire (77%), bien représentée

CLASS 2: Neither ✓ (833 samples)
├─ Precision: 0.79  ← Correct
├─ Recall: 0.81     ← Bon
├─ F1-Score: 0.80   ← Bon
└─ Raison: Classe intermédiaire (17%)
```

---

## Utilisation du Pipeline en 3 Étapes

```
ÉTAPE 1: Charger
└─ import joblib
└─ pipeline = joblib.load('sentiment_classifier_pipeline.pkl')

ÉTAPE 2: Prédire
└─ predictions = pipeline.predict(["I hate this!"])
└─ confidence = pipeline.predict_proba(["I hate this!"]).max()

ÉTAPE 3: Interpréter
└─ classes = ['Hate', 'Offensive', 'Neither']
└─ print(f"{classes[predictions[0]]} ({confidence:.2%})")
```

---

## Recommandations Futures

```
Court Terme (Facile - 1 heure)
├─ SMOTE au lieu de ROS/RUS
├─ class_weight='balanced' dans BernoulliNB
└─ Threshold tuning (0.5 → 0.3)

Moyen Terme (Intermédiaire - 3 heures)
├─ Features linguistiques (sentiment, majuscules, ponctuation)
├─ SVM(kernel='rbf', class_weight='balanced')
└─ Random Forest avec class_weight

Long Terme (Advanced - 1+ jours)
├─ Word2Vec embeddings + LSTM
├─ BERT fine-tuning
└─ Ensemble methods
```

---

## Fichiers à Consulter Selon Besoin

```
Je dois faire un rapport techniqe
  → RAPPORT_SENTIMENT_CLASSIFIER.md

Je dois donner une présentation
  → Utiliser les 6 graphiques + RÉSUMÉ_FINAL.md

Je dois coder quelque chose de similaire
  → quick_start.py (copy-paste friendly)

Je veux améliorer le modèle
  → GUIDE_COMPLET.md (Solutions proposées)

Je veux comprendre chaque ligne de code
  → sentiment_classifier.py (2500 lignes bien commentées)

Je suis perdu
  → ⚡_START_HERE.txt (2 min de lecture)

Je veux naviguer tous les fichiers
  → INDEX.md (Table des matières complète)
```

---

**Architecture complète et documentée ✅**
