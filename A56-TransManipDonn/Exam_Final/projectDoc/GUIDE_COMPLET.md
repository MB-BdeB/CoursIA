# 📋 GUIDE COMPLET - CLASSIFICATEUR DE SENTIMENTS

## 🎯 Résumé Exécutif (30 secondes)

**Tâche:** Classifier des tweets en 3 catégories (Hate Speech, Offensive Language, Neither)  
**Dataset:** 24,783 tweets **DÉSÉQUILIBRÉ** (77% Offensive, 17% Neither, 6% Hate)  
**Meilleur modèle:** SelectKBest χ² avec F1=0.8696 ✅  
**Problème persistant:** Hate Speech peu détecté (Recall=0.20)

---

## 📊 Résultats Clés

### Comparaison des Modèles

```
┌──────────────────┬──────────┬───────────┬────────┬──────────┐
│ Modèle           │ Accuracy │ Precision │ Recall │ F1-Score │
├──────────────────┼──────────┼───────────┼────────┼──────────┤
│ Base (TF-IDF)    │  87.45%  │   85.60%  │ 87.45% │  86.18%  │
│ SelectKBest χ²   │  87.90%  │   86.47%  │ 87.90% │  86.96%  │ ← MEILLEUR
│ SelectKBest+ROS  │  83.48%  │   88.28%  │ 83.48% │  85.28%  │
│ SelectKBest+RUS  │  80.23%  │   88.67%  │ 80.23% │  83.13%  │
└──────────────────┴──────────┴───────────┴────────┴──────────┘
```

### Par Classe (SelectKBest χ² - MEILLEUR)

```
              Precision  Recall  F1-Score
Hate Speech      0.41     0.20     0.27   ← Très faible!
Offensive        0.91     0.94     0.93   ← Excellent
Neither          0.79     0.81     0.80   ← Bon
```

---

## 🔧 DÉCOMPOSITION TECHNIQUE

### 1️⃣ PRÉTRAITEMENT DU TEXTE

```python
Opérations appliquées:
├── URLs: "http://..." → supprimées
├── Mentions: "@user" → supprimées
├── Ponctuation: "!" "." "?" → supprimées
├── Majuscules: "HATE" → "hate"
└── Espaces: "  " → " "

Exemple:
AVANT: "!!! RT @mayasolovely: As a woman you shouldn't complain about cleaning 
        up your house. &amp; as a man you should always take the trash out..."
APRÈS: "rt as a woman you shouldnt complain about cleaning up your house amp as 
        a man you should always take the trash out"
```

### 2️⃣ VECTORISATION TF-IDF

```python
TfidfVectorizer(
    ngram_range=(1, 2),      # Unigrammes + bigrammes
    max_features=10000,      # Top 10k features
    min_df=5,                # Min 5 documents
    max_df=0.8               # Max 80% du corpus
)

Résultat:
├── 9,573 features initiales
├── 0.15% de sparsité (tres creux)
└── Matrice (19826 x 9573)
```

**Utilité des n-grams:**
- Unigrammes: "hate", "love", "great"
- Bigrammes: "hate speech", "love this", "very great"
- Capture du contexte + vocabulaire individuel

### 3️⃣ SÉLECTION DE CARACTÉRISTIQUES

```python
SelectKBest(chi2, k=5000)  # Top 5000 features selon χ²

Test Chi-Carré (χ²):
├── Mesure l'indépendance entre feature et target
├── Features avec χ² élevé = fortement liées à la classe
└── Élimine 49% des features inutiles (9573 → 5000)

Impact:
├── Accuracy: +0.45% (0.8745 → 0.8790)
├── F1-Score: +0.78% (0.8618 → 0.8696)
└── Réduction du surapprentissage ✅
```

### 4️⃣ ÉQUILIBRAGE DES CLASSES

**Option A: RandomOverSampler (ROS)**
```
Distribution AVANT: {Hate: 1,144  | Offensive: 15,352 | Neither: 3,330}
Distribution APRÈS: {Hate: 15,352 | Offensive: 15,352 | Neither: 15,352}

Technique: Duplication aléatoire des minoritaires

Résultats:
├── Recall Hate: +40% (0.20 → 0.55) ✅
├── Precision Hate: -68% (0.41 → 0.26) ❌
├── Accuracy: -4.58% (87.90% → 83.48%) ❌
└── Trade-off: Plus de détection, mais beaucoup de faux positifs
```

**Option B: RandomUnderSampler (RUS)**
```
Distribution AVANT: {Hate: 1,144  | Offensive: 15,352 | Neither: 3,330}
Distribution APRÈS: {Hate: 1,144  | Offensive: 1,144  | Neither: 1,144}

Technique: Suppression aléatoire des majoritaires

Résultats:
├── Recall Hate: +52% (0.20 → 0.67) ✅
├── Accuracy: -8.80% (87.90% → 80.23%) ❌
├── Perte massive de données (-92% pour Offensive) ❌
└── Trade-off: Excellent Recall mais mauvaise Accuracy globale
```

**Conclusion:**
- ✅ Sans équilibrage = Meilleur compromis
- ❌ ROS et RUS dégradent la performance
- 💡 Alternative: SMOTE (meilleur que ROS/RUS) ou class_weight

---

## 🚀 AMÉLIORATIONS POSSIBLES

### A. Court Terme (Faciles à implémenter)

#### 1. Tuning de class_weight
```python
# Au lieu de ROS/RUS, utiliser les poids de classe
nb = BernoulliNB()
sample_weight = class_weight.compute_sample_weight('balanced', y_train)
nb.fit(X_train, y_train, sample_weight=sample_weight)

Avantage: Pas de duplication/suppression, juste pondération
```

#### 2. Threshold Tuning
```python
# Par défaut, threshold=0.5 pour binarisation
# Réduire le threshold pour augmenter Recall "Hate"

from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
# Choisir threshold optimal selon objectif métier
```

#### 3. SMOTE (Synthetic Minority Over-sampling)
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
# Génère des échantillons synthétiques (meilleur que duplication)
```

### B. Moyen Terme (Modèle amélioré)

#### 4. Feature Engineering Avancé
```python
# Ajouter des features linguistiques:
├── Sentiment lexicon (VADER, TextBlob)
├── Nombre de majuscules (capslock = agressivité)
├── Nombre de ponctuation (!!! = émotion)
├── Nombre d'exclamations/interrogations
├── Longueur du texte
└── Nombre de mots rares

Résultat: Features (9573 + 6) = 9579 features
```

#### 5. Autre Classifieur: SVM
```python
from sklearn.svm import SVC

svm = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    class_weight='balanced'  # Gère le déséquilibre
)

Avantage: SVM > Naive Bayes pour texte
```

#### 6. Autre Classifieur: Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    class_weight='balanced',
    random_state=42
)

Avantage: Gère l'imbalance naturellement + explainabilité
```

### C. Long Terme (Deep Learning)

#### 7. Word Embeddings + LSTM
```python
# Utiliser pré-trained embeddings
from gensim.models import Word2Vec

w2v = Word2Vec.load('word2vec_model')
# Transformer tweets en sequences d'embeddings
# Entraîner LSTM ou Bi-LSTM

Avantage: Capture du contexte sémantique + ordre des mots
```

#### 8. BERT (Bidirectional Encoder Representations from Transformers)
```python
from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=3
)

Avantage: SOTA (State-of-the-Art), pré-trained sur texte massif
```

---

## 📈 PLAN D'EXPÉRIMENTATION

### Expérience 1: Optimiser Recall "Hate" sans dégrader Accuracy
```
Essayer:
├── Threshold tuning (0.5 → 0.3 ou 0.4)
├── SMOTE au lieu de ROS/RUS
├── class_weight='balanced' dans BernoulliNB
├── SVM avec kernel RBF
└── Random Forest

Métrique cible: Recall "Hate" > 0.50, Accuracy > 0.85
```

### Expérience 2: Ajouter Features Linguistiques
```
Ajouter:
├── VADER sentiment scores (positif/négatif/neutre)
├── Nombre majuscules
├── Nombre ponctuation
├── Longueur du tweet
└── TF-IDF des emoji/emoticons

Ré-évaluer SelectKBest sur (9573 + 5) = 9578 features
```

### Expérience 3: Comparer Classifieurs
```
Tester:
├── Naive Bayes (actuel)
├── SVM avec γ²
├── Random Forest
├── Logistic Regression
├── Gradient Boosting (XGBoost)
└── Neural Network (Keras)

Comparer avec F1-Score pondéré
```

---

## 💾 UTILISATION DU PIPELINE

### Load et Utilisation

```python
import joblib

# Charger le modèle sauvegardé
pipeline = joblib.load('sentiment_classifier_pipeline.pkl')

# Prédictions sur nouveaux tweets
tweets = [
    "I love this product!",
    "This is absolutely disgusting",
    "Nice weather today"
]

predictions = pipeline.predict(tweets)
confidences = pipeline.predict_proba(tweets).max(axis=1)

for tweet, pred, conf in zip(tweets, predictions, confidences):
    class_name = ['Hate Speech', 'Offensive', 'Neither'][pred]
    print(f"'{tweet}' → {class_name} ({conf:.2%})")
```

### Fichiers Disponibles

```
📦 Exam_Final/
├── 📄 sentiment_classifier.py          ← Script principal
├── 💾 sentiment_classifier_pipeline.pkl ← Modèle sauvegardé
├── 📊 1_metrics_comparison.png         ← Graphiques
├── 📊 2_class_distribution.png
├── 📊 3_f1_by_class.png
├── 📊 4_confusion_matrix.png
├── 📊 5_summary_table.png
├── 📋 RAPPORT_SENTIMENT_CLASSIFIER.md  ← Ce rapport
└── 📝 generate_visualizations.py       ← Script visualisation
```

---

## 🎓 CONCEPTS PÉDAGOGIQUES (Réf. Cours A56)

### Séance 10: Prétraitement du Texte
```
Concepts:
├── Nettoyage (URLs, ponctuation)
├── Tokenization
├── Normalisation (minuscules)
└── Suppression stop words (optionnel)

Implémentation:
└── expressions régulières (regex)
```

### Séance 11: Vectorisation TF-IDF
```
Concepts:
├── TF (Term Frequency) = fréquence du mot dans doc
├── IDF (Inverse Document Frequency) = importance inverse
├── Formule: TF-IDF = TF × IDF
└── N-grams: capture des séquences

Utilité:
└── Transformer texte en nombres pour modèles ML
```

### Séance 12: Sélection de Caractéristiques
```
Concepts:
├── SelectKBest: choisir les K meilleures features
├── Chi-Carré (χ²): test d'indépendance
├── Variance Threshold: éliminer features à faible variance
└── RFE: élimination récursive

Trade-off:
├── Moins de features = moins d'overfit
├── Mais plus de features = plus d'info
└── Sweet spot: SelectKBest k=5000
```

### Séance 13: Équilibrage des Classes
```
Concepts:
├── Imbalanced Classification
├── Oversampling: dupliquer minoritaires (ROS)
├── Undersampling: supprimer majoritaires (RUS)
├── SMOTE: synthétiser minoritaires
└── class_weight: pondérer les classes

Résultat:
└── Pour ce dataset: SelectKBest seul > ROS/RUS
```

---

## 🏆 Conclusion Finale

### ✅ Ce qui Fonctionne Bien
- ✅ SelectKBest χ² améliore légèrement la performance (+0.78% en F1)
- ✅ TF-IDF + Bigrammes capture bien le vocabulaire offensant
- ✅ Naive Bayes converge rapidement, bonnes prédictions globales
- ✅ Accuracy 87.9% sur dataset déséquilibré est acceptable

### ❌ Difficultés Persistantes
- ❌ "Hate Speech" très sous-détecté (Recall=0.20)
- ❌ Confusion entre "Hate" et "Offensive Language"
- ❌ ROS/RUS ne résolvent pas le problème
- ❌ Accuracy/Recall trade-off difficile

### 🎯 Recommandations
1. **Court terme:** SMOTE + class_weight + seuil tuning
2. **Moyen term:** Features linguistiques + SVM/Random Forest
3. **Long term:** Embeddings (Word2Vec) + LSTM/BERT
4. **Métier:** Définir la tolérance Faux Positifs/Faux Négatifs

---

**Généré:** 12 mars 2026  
**Par:** Classificateur de Sentiments Automatisé  
**Dataset:** 24,783 tweets Twitter (labeled_data.csv)  
**Framework:** Scikit-learn, Imbalanced-learn, Pandas
