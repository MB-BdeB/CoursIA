"""
========================================
QUICK START - SENTIMENT CLASSIFIER
========================================
Guide d'implémentation rapide avec snippets de code
"""

# ============================================
# 1. INSTALLATION DES PACKAGES
# ============================================

"""
pip install scikit-learn pandas numpy matplotlib seaborn imbalanced-learn joblib
"""

# ============================================
# 2. IMPORT DES LIBRAIRES
# ============================================

import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import joblib

# ============================================
# 3. CHARGEMENT ET NETTOYAGE DES DONNÉES
# ============================================

# Charger le dataset
df = pd.read_csv('labeled_data.csv', index_col=0)

# Fonction de nettoyage
def clean_tweet(tweet):
    if not isinstance(tweet, str):
        return ""
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet)  # URLs
    tweet = re.sub(r'@\w+', '', tweet)                      # Mentions
    tweet = re.sub(r'[^\w\s]', '', tweet)                   # Ponctuation
    tweet = tweet.lower().strip()                           # Minuscules
    return re.sub(r'\s+', ' ', tweet)

df['tweet_clean'] = df['tweet'].apply(clean_tweet)

# Diviser train/test
X_train, X_test, y_train, y_test = train_test_split(
    df['tweet_clean'], df['class'],
    test_size=0.2, random_state=42, stratify=df['class']
)

# ============================================
# 4. MODÈLE DE BASE (TF-IDF + NAIVE BAYES)
# ============================================

print("=== MODÈLE DE BASE ===")

# Vectorisation TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Entraînement Naive Bayes
nb = BernoulliNB(binarize=0.0)
nb.fit(X_train_tfidf, y_train)
y_pred = nb.predict(X_test_tfidf)

# Évaluation
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred, average='weighted'):.4f}")
print(f"F1-Score: {f1_score(y_test, y_pred, average='weighted'):.4f}")

# ============================================
# 5. AVEC SÉLECTION DE CARACTÉRISTIQUES
# ============================================

print("\n=== AVEC SELECTKBEST χ² ===")

# Sélection des 5000 meilleures features
selector = SelectKBest(chi2, k=5000)
X_train_selected = selector.fit_transform(X_train_tfidf, y_train)
X_test_selected = selector.transform(X_test_tfidf)

# Entraînement Naive Bayes
nb_selected = BernoulliNB(binarize=0.0)
nb_selected.fit(X_train_selected, y_train)
y_pred_selected = nb_selected.predict(X_test_selected)

# Évaluation
print(f"Accuracy: {accuracy_score(y_test, y_pred_selected):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_selected, average='weighted'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_selected, average='weighted'):.4f}")
print(f"F1-Score: {f1_score(y_test, y_pred_selected, average='weighted'):.4f}")

# ============================================
# 6. AVEC ÉQUILIBRAGE - RANDOM OVER-SAMPLER
# ============================================

print("\n=== AVEC RANDOM OVER-SAMPLER (ROS) ===")

ros = RandomOverSampler(random_state=42)
X_train_ros, y_train_ros = ros.fit_resample(X_train_selected, y_train)

nb_ros = BernoulliNB(binarize=0.0)
nb_ros.fit(X_train_ros, y_train_ros)
y_pred_ros = nb_ros.predict(X_test_selected)

print(f"Accuracy: {accuracy_score(y_test, y_pred_ros):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_ros, average='weighted'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_ros, average='weighted'):.4f}")
print(f"F1-Score: {f1_score(y_test, y_pred_ros, average='weighted'):.4f}")

# ============================================
# 7. AVEC ÉQUILIBRAGE - RANDOM UNDER-SAMPLER
# ============================================

print("\n=== AVEC RANDOM UNDER-SAMPLER (RUS) ===")

rus = RandomUnderSampler(random_state=42)
X_train_rus, y_train_rus = rus.fit_resample(X_train_selected, y_train)

nb_rus = BernoulliNB(binarize=0.0)
nb_rus.fit(X_train_rus, y_train_rus)
y_pred_rus = nb_rus.predict(X_test_selected)

print(f"Accuracy: {accuracy_score(y_test, y_pred_rus):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_rus, average='weighted'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_rus, average='weighted'):.4f}")
print(f"F1-Score: {f1_score(y_test, y_pred_rus, average='weighted'):.4f}")

# ============================================
# 8. PIPELINE FINAL AUTOMATISÉ
# ============================================

print("\n=== PIPELINE FINAL ===")

final_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        min_df=5,
        max_df=0.8
    )),
    ('selector', SelectKBest(chi2, k=5000)),
    ('classifier', BernoulliNB(binarize=0.0))
])

# Entraînement
final_pipeline.fit(X_train, y_train)

# Prédictions
y_pred_final = final_pipeline.predict(X_test)

# Évaluation
print(f"Accuracy: {accuracy_score(y_test, y_pred_final):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_final, average='weighted'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_final, average='weighted'):.4f}")
print(f"F1-Score: {f1_score(y_test, y_pred_final, average='weighted'):.4f}")

# ============================================
# 9. SAUVEGARDER LE MODÈLE
# ============================================

joblib.dump(final_pipeline, 'sentiment_pipeline.pkl')
print("\n✅ Pipeline sauvegardé: sentiment_pipeline.pkl")

# ============================================
# 10. CHARGER ET UTILISER LE MODÈLE
# ============================================

# Charger
loaded_pipeline = joblib.load('sentiment_pipeline.pkl')

# Prédictions sur nouveaux tweets
test_tweets = [
    "I love this product",
    "This is disgusting",
    "Nice weather"
]

predictions = loaded_pipeline.predict(test_tweets)
confidences = loaded_pipeline.predict_proba(test_tweets).max(axis=1)

class_names = ['Hate Speech', 'Offensive Language', 'Neither']

print("\n=== PRÉDICTIONS ===")
for tweet, pred, conf in zip(test_tweets, predictions, confidences):
    print(f"'{tweet}' → {class_names[pred]} ({conf:.2%})")

# ============================================
# 11. RAPPORT DE CLASSIFICATION DÉTAILLÉ
# ============================================

print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred_final, target_names=class_names))

# ============================================
# 12. MATRICE DE CONFUSION
# ============================================

cm = confusion_matrix(y_test, y_pred_final)
print("\n=== CONFUSION MATRIX ===")
print(cm)

# ============================================
# VARIANTES À ESSAYER
# ============================================

"""
# Variante A: Avec SMOTE (meilleur que ROS)
# -----------------------------------------
from imblearn.over_sampling import SMOTE

smote_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
    ('selector', SelectKBest(chi2, k=5000)),
    ('smote', SMOTE(random_state=42)),
    ('classifier', BernoulliNB(binarize=0.0))
])

smote_pipeline.fit(X_train, y_train)
y_pred_smote = smote_pipeline.predict(X_test)
print(f"SMOTE F1-Score: {f1_score(y_test, y_pred_smote, average='weighted'):.4f}")

# Variante B: Avec SVM (plus puissant que Naive Bayes)
# -------------------------------------------------------
from sklearn.svm import SVC

svm_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
    ('selector', SelectKBest(chi2, k=5000)),
    ('classifier', SVC(kernel='rbf', class_weight='balanced'))
])

svm_pipeline.fit(X_train, y_train)
y_pred_svm = svm_pipeline.predict(X_test)
print(f"SVM F1-Score: {f1_score(y_test, y_pred_svm, average='weighted'):.4f}")

# Variante C: Avec Random Forest (explainablility)
# -------------------------------------------------------
from sklearn.ensemble import RandomForestClassifier

rf_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
    ('selector', SelectKBest(chi2, k=5000)),
    ('classifier', RandomForestClassifier(n_estimators=100, class_weight='balanced'))
])

rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_test)
print(f"Random Forest F1-Score: {f1_score(y_test, y_pred_rf, average='weighted'):.4f}")
"""

print("\n✅ ANALYSE COMPLÈTE TERMINÉE!")
