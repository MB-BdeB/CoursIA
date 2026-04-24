"""
========================================
CLASSIFICATEUR DE SENTIMENTS MULTICLASSE
========================================
Analyse de tweets: Hate Speech / Offensive Language / Neither
Dataset: labeled_data.csv (déséquilibré)

Étapes:
1. Prétraitement du texte
2. Modèle de base (Naive Bayes)
3. Sélection de caractéristiques (SelectKBest)
4. Équilibrage des classes (ROS, RUS)
5. Pipeline final
"""

import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

# ============================================
# IMPORTS SCIKIT-LEARN ET AUTRES OUTILS
# ============================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline

import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# 1. CHARGEMENT ET EXPLORATION DES DONNÉES
# ============================================

print("="*60)
print("ÉTAPE 1: CHARGEMENT ET EXPLORATION")
print("="*60)

df = pd.read_csv('labeled_data.csv', index_col=0)

print(f"\nShape du dataset: {df.shape}")
print(f"\nPremières lignes:")
print(df.head(3))

print(f"\nDistribution des classes:")
print(df['class'].value_counts())

print(f"\nPourcentages:")
print(df['class'].value_counts(normalize=True) * 100)

# Détection du déséquilibre
class_counts = df['class'].value_counts()
imbalance_ratio = class_counts.max() / class_counts.min()
print(f"\n⚠️ Ratio de déséquilibre: {imbalance_ratio:.2f}x")

# Mapping des classes
class_mapping = {0: 'Hate Speech', 1: 'Offensive Language', 2: 'Neither'}
df['class_name'] = df['class'].map(class_mapping)

# ============================================
# 2. PRÉTRAITEMENT DU TEXTE
# ============================================

print("\n" + "="*60)
print("ÉTAPE 2: PRÉTRAITEMENT DU TEXTE")
print("="*60)

def clean_tweet(tweet):
    """
    Nettoyer les tweets:
    - URLs
    - Mentions @
    - Ponctuation
    - Minuscules
    """
    if not isinstance(tweet, str):
        return ""
    
    # Supprimer les URLs
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
    
    # Supprimer les mentions @
    tweet = re.sub(r'@\w+', '', tweet)
    
    # Supprimer les caractères spéciaux et ponctuation (sauf space)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    
    # Convertir en minuscules
    tweet = tweet.lower()
    
    # Supprimer les espaces multiples
    tweet = re.sub(r'\s+', ' ', tweet).strip()
    
    return tweet

# Appliquer le nettoyage
print("\nNettoyage des tweets...")
df['tweet_clean'] = df['tweet'].apply(clean_tweet)

print(f"\nExemples avant/après:")
for i in range(2):
    print(f"\nTweet {i}:")
    print(f"  Avant: {df['tweet'].iloc[i][:80]}...")
    print(f"  Après: {df['tweet_clean'].iloc[i][:80]}...")

# ============================================
# 3. VECTORISATION TF-IDF
# ============================================

print("\n" + "="*60)
print("ÉTAPE 3: VECTORISATION TF-IDF")
print("="*60)

# Diviser en train/test
X_train, X_test, y_train, y_test = train_test_split(
    df['tweet_clean'],
    df['class'],
    test_size=0.2,
    random_state=42,
    stratify=df['class']
)

print(f"\nTrain: {X_train.shape[0]}, Test: {X_test.shape[0]}")
print(f"Distribution Train:\n{pd.Series(y_train).value_counts()}")

# Vectorisation TF-IDF (unigrams + bigrams)
print("\nVectorisation TF-IDF (unigrams + bigrams)...")
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),  # unigrams + bigrams
    max_features=10000,
    min_df=5,
    max_df=0.8
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"Nombre de features: {X_train_tfidf.shape[1]}")
print(f"Densité: {X_train_tfidf.nnz / (X_train_tfidf.shape[0] * X_train_tfidf.shape[1]):.2%}")

# ============================================
# 4. MODÈLE DE BASE: NAIVE BAYES
# ============================================

print("\n" + "="*60)
print("ÉTAPE 4: MODÈLE DE BASE (NAIVE BAYES)")
print("="*60)

# Entraîner Naive Bayes sur TF-IDF brut
print("\nEntraînement Naive Bayes (BernoulliNB)...")
nb_base = BernoulliNB(binarize=0.0)
nb_base.fit(X_train_tfidf, y_train)

# Prédictions
y_pred_base = nb_base.predict(X_test_tfidf)

# Évaluations
print("\n📊 RÉSULTATS - MODÈLE DE BASE:")
print("-" * 40)

accuracy_base = accuracy_score(y_test, y_pred_base)
precision_base = precision_score(y_test, y_pred_base, average='weighted')
recall_base = recall_score(y_test, y_pred_base, average='weighted')
f1_base = f1_score(y_test, y_pred_base, average='weighted')

print(f"Accuracy:  {accuracy_base:.4f}")
print(f"Precision: {precision_base:.4f}")
print(f"Recall:    {recall_base:.4f}")
print(f"F1-Score:  {f1_base:.4f}")

print("\n📋 Classification Report (Modèle de Base):")
print(classification_report(y_test, y_pred_base, target_names=['Hate', 'Offensive', 'Neither']))

# ============================================
# 5. SÉLECTION DE CARACTÉRISTIQUES (SelectKBest)
# ============================================

print("\n" + "="*60)
print("ÉTAPE 5: SÉLECTION DE CARACTÉRISTIQUES (SelectKBest)")
print("="*60)

k_best = 5000
print(f"\nSélection des {k_best} meilleures features (χ²)...")

selector = SelectKBest(chi2, k=k_best)
X_train_selected = selector.fit_transform(X_train_tfidf, y_train)
X_test_selected = selector.transform(X_test_tfidf)

print(f"Avant: {X_train_tfidf.shape[1]} features")
print(f"Après: {X_train_selected.shape[1]} features")

# Entraîner Naive Bayes sur features sélectionnées
print("\nEntraînement Naive Bayes avec features sélectionnées...")
nb_selected = BernoulliNB(binarize=0.0)
nb_selected.fit(X_train_selected, y_train)

y_pred_selected = nb_selected.predict(X_test_selected)

print("\n📊 RÉSULTATS - MODÈLE AVEC SELECT K-BEST:")
print("-" * 40)

accuracy_selected = accuracy_score(y_test, y_pred_selected)
precision_selected = precision_score(y_test, y_pred_selected, average='weighted')
recall_selected = recall_score(y_test, y_pred_selected, average='weighted')
f1_selected = f1_score(y_test, y_pred_selected, average='weighted')

print(f"Accuracy:  {accuracy_selected:.4f}")
print(f"Precision: {precision_selected:.4f}")
print(f"Recall:    {recall_selected:.4f}")
print(f"F1-Score:  {f1_selected:.4f}")

print("\n📋 Classification Report (SelectKBest):")
print(classification_report(y_test, y_pred_selected, target_names=['Hate', 'Offensive', 'Neither']))

# ============================================
# 6. ÉQUILIBRAGE DES CLASSES
# ============================================

print("\n" + "="*60)
print("ÉTAPE 6: ÉQUILIBRAGE DES CLASSES")
print("="*60)

results_comparison = {
    'Modèle': ['Base (TF-IDF brut)', 'SelectKBest χ²'],
    'Accuracy': [accuracy_base, accuracy_selected],
    'Precision': [precision_base, precision_selected],
    'Recall': [recall_base, recall_selected],
    'F1-Score': [f1_base, f1_selected]
}

# ============================================
# 6A. RANDOM OVER-SAMPLER (ROS)
# ============================================

print("\n### 6A. RANDOM OVER-SAMPLER (ROS) ###")
print("Sur-pondération des classes minoritaires")

ros = RandomOverSampler(random_state=42)
X_train_selected_ros, y_train_ros = ros.fit_resample(X_train_selected, y_train)

print(f"\nDistirbution avant ROS: {pd.Series(y_train).value_counts().to_dict()}")
print(f"Distribution après ROS: {pd.Series(y_train_ros).value_counts().to_dict()}")

# Entraîner Naive Bayes
nb_ros = BernoulliNB(binarize=0.0)
nb_ros.fit(X_train_selected_ros, y_train_ros)

y_pred_ros = nb_ros.predict(X_test_selected)

print("\n📊 RÉSULTATS - MODÈLE AVEC ROS:")
print("-" * 40)

accuracy_ros = accuracy_score(y_test, y_pred_ros)
precision_ros = precision_score(y_test, y_pred_ros, average='weighted')
recall_ros = recall_score(y_test, y_pred_ros, average='weighted')
f1_ros = f1_score(y_test, y_pred_ros, average='weighted')

print(f"Accuracy:  {accuracy_ros:.4f}")
print(f"Precision: {precision_ros:.4f}")
print(f"Recall:    {recall_ros:.4f}")
print(f"F1-Score:  {f1_ros:.4f}")

print("\n📋 Classification Report (ROS):")
print(classification_report(y_test, y_pred_ros, target_names=['Hate', 'Offensive', 'Neither']))

# ============================================
# 6B. RANDOM UNDER-SAMPLER (RUS)
# ============================================

print("\n### 6B. RANDOM UNDER-SAMPLER (RUS) ###")
print("Sous-pondération des classes majoritaires")

rus = RandomUnderSampler(random_state=42)
X_train_selected_rus, y_train_rus = rus.fit_resample(X_train_selected, y_train)

print(f"\nDistribution avant RUS: {pd.Series(y_train).value_counts().to_dict()}")
print(f"Distribution après RUS: {pd.Series(y_train_rus).value_counts().to_dict()}")

# Entraîner Naive Bayes
nb_rus = BernoulliNB(binarize=0.0)
nb_rus.fit(X_train_selected_rus, y_train_rus)

y_pred_rus = nb_rus.predict(X_test_selected)

print("\n📊 RÉSULTATS - MODÈLE AVEC RUS:")
print("-" * 40)

accuracy_rus = accuracy_score(y_test, y_pred_rus)
precision_rus = precision_score(y_test, y_pred_rus, average='weighted')
recall_rus = recall_score(y_test, y_pred_rus, average='weighted')
f1_rus = f1_score(y_test, y_pred_rus, average='weighted')

print(f"Accuracy:  {accuracy_rus:.4f}")
print(f"Precision: {precision_rus:.4f}")
print(f"Recall:    {recall_rus:.4f}")
print(f"F1-Score:  {f1_rus:.4f}")

print("\n📋 Classification Report (RUS):")
print(classification_report(y_test, y_pred_rus, target_names=['Hate', 'Offensive', 'Neither']))

# ============================================
# 7. COMPARAISON DES RÉSULTATS
# ============================================

print("\n" + "="*60)
print("ÉTAPE 7: COMPARAISON DES RÉSULTATS")
print("="*60)

# Créer un DataFrame comparatif
results_comparison = {
    'Modèle': [
        'Base (TF-IDF brut)',
        'SelectKBest χ²',
        'SelectKBest + ROS',
        'SelectKBest + RUS'
    ],
    'Accuracy': [accuracy_base, accuracy_selected, accuracy_ros, accuracy_rus],
    'Precision': [precision_base, precision_selected, precision_ros, precision_rus],
    'Recall': [recall_base, recall_selected, recall_ros, recall_rus],
    'F1-Score': [f1_base, f1_selected, f1_ros, f1_rus]
}

df_results = pd.DataFrame(results_comparison)

print("\n📊 TABLEAU COMPARATIF:")
print(df_results.to_string(index=False))

# Déterminer le meilleur modèle
best_idx = df_results['F1-Score'].idxmax()
best_model_name = df_results.loc[best_idx, 'Modèle']
best_f1 = df_results.loc[best_idx, 'F1-Score']

print(f"\n🏆 MEILLEUR MODÈLE: {best_model_name}")
print(f"F1-Score: {best_f1:.4f}")

# Visualisation
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
for idx, metric in enumerate(metrics):
    ax = axes[idx // 2, idx % 2]
    colors = ['#ff6b6b' if i != best_idx else '#51cf66' for i in range(len(df_results))]
    ax.bar(range(len(df_results)), df_results[metric], color=colors)
    ax.set_xticks(range(len(df_results)))
    ax.set_xticklabels(df_results['Modèle'], rotation=45, ha='right')
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} par modèle')
    ax.set_ylim([0, 1])
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('sentiment_comparison.png', dpi=300, bbox_inches='tight')
print("\n✅ Graphique sauvegardé: sentiment_comparison.png")

# ============================================
# 8. PIPELINE FINAL (MEILLEUR MODÈLE)
# ============================================

print("\n" + "="*60)
print("ÉTAPE 8: PIPELINE FINAL (MEILLEUR MODÈLE)")
print("="*60)

# Créer le pipeline final avec le meilleur modèle (ROS)
print("\nCréation du pipeline final...")

final_pipeline = ImbPipeline([
    ('tfidf', TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        min_df=5,
        max_df=0.8
    )),
    ('selector', SelectKBest(chi2, k=5000)),
    ('ros', RandomOverSampler(random_state=42)),
    ('classifier', BernoulliNB(binarize=0.0))
])

print("Entraînement du pipeline sur tout le train set...")
final_pipeline.fit(X_train, y_train)

y_pred_final = final_pipeline.predict(X_test)

print("\n📊 RÉSULTATS - PIPELINE FINAL:")
print("-" * 40)

accuracy_final = accuracy_score(y_test, y_pred_final)
precision_final = precision_score(y_test, y_pred_final, average='weighted')
recall_final = recall_score(y_test, y_pred_final, average='weighted')
f1_final = f1_score(y_test, y_pred_final, average='weighted')

print(f"Accuracy:  {accuracy_final:.4f}")
print(f"Precision: {precision_final:.4f}")
print(f"Recall:    {recall_final:.4f}")
print(f"F1-Score:  {f1_final:.4f}")

print("\n📋 Classification Report (Pipeline Final):")
print(classification_report(y_test, y_pred_final, target_names=['Hate', 'Offensive', 'Neither']))

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred_final)
print("\n Confusion Matrix:")
print(cm)

# Sauvegarder le pipeline
import joblib
joblib.dump(final_pipeline, 'sentiment_classifier_pipeline.pkl')
print("\n✅ Pipeline sauvegardé: sentiment_classifier_pipeline.pkl")

# ============================================
# 9. TEST SUR DE NOUVEAUX TWEETS
# ============================================

print("\n" + "="*60)
print("ÉTAPE 9: TEST SUR DE NOUVEAUX TWEETS")
print("="*60)

test_tweets = [
    "I love this product, it's amazing!",
    "This is absolutely horrible and disgusting",
    "The weather today is nice"
]

print("\nPrédictions sur nouveaux tweets:")
for tweet in test_tweets:
    pred = final_pipeline.predict([tweet])[0]
    confidence = final_pipeline.predict_proba([tweet]).max()
    class_name = class_mapping[pred]
    print(f"\n  Tweet: '{tweet}'")
    print(f"  →  {class_name} (confiance: {confidence:.2%})")

print("\n✅ ANALYSE COMPLÈTE TERMINÉE!")
