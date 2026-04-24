"""
Script pour générer les visualisations des résultats
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration visuelle
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

# ============================================
# DONNÉES DES RÉSULTATS
# ============================================

results = {
    'Modèle': [
        'Base (TF-IDF brut)',
        'SelectKBest χ²',
        'SelectKBest + ROS',
        'SelectKBest + RUS'
    ],
    'Accuracy': [0.8745, 0.8790, 0.8348, 0.8023],
    'Precision': [0.8560, 0.8647, 0.8828, 0.8867],
    'Recall': [0.8745, 0.8790, 0.8348, 0.8023],
    'F1-Score': [0.8618, 0.8696, 0.8528, 0.8313]
}

df_results = pd.DataFrame(results)

# ============================================
# FIGURE 1: COMPARAISON DES MÉTRIQUES
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Sentiment Classifier - Comparaison des Modèles', fontsize=16, fontweight='bold')

# Palette de couleurs
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
best_model_idx = df_results['F1-Score'].idxmax()

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']

for idx, metric in enumerate(metrics):
    ax = axes[idx // 2, idx % 2]
    
    # Créer les barres colorées
    bar_colors = [colors[i] if i != best_model_idx else '#2ECC71' for i in range(len(df_results))]
    bars = ax.bar(range(len(df_results)), df_results[metric], color=bar_colors, edgecolor='black', linewidth=1.5)
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom', fontweight='bold')
    
    ax.set_xticks(range(len(df_results)))
    ax.set_xticklabels(df_results['Modèle'], rotation=45, ha='right')
    ax.set_ylabel(metric, fontweight='bold')
    ax.set_title(f'{metric} par modèle', fontweight='bold')
    ax.set_ylim([0.75, 0.95])
    ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('1_metrics_comparison.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 1 sauvegardé: 1_metrics_comparison.png")
plt.close()

# ============================================
# FIGURE 2: DISTRIBUTION DES CLASSES
# ============================================

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fig.suptitle('Distribution des Classes - Dataset Déséquilibré', fontsize=14, fontweight='bold')

# Avant équilibrage
train_dist = {0: 1144, 1: 15352, 2: 3330}
ax = axes[0]
classes = ['Hate Speech', 'Offensive\nLanguage', 'Neither']
values = [train_dist[0], train_dist[1], train_dist[2]]
bars = ax.bar(classes, values, color=['#e74c3c', '#f39c12', '#2ecc71'], edgecolor='black', linewidth=1.5)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height}\n({height/sum(values)*100:.1f}%)',
            ha='center', va='bottom', fontweight='bold')
ax.set_ylabel('Nombre d\'échantillons', fontweight='bold')
ax.set_title('AVANT Équilibrage (Train)', fontweight='bold')
ax.set_ylim([0, 17000])
ax.grid(axis='y', alpha=0.3)

# Après ROS
ros_dist = {0: 15352, 1: 15352, 2: 15352}
ax = axes[1]
values_ros = [ros_dist[0], ros_dist[1], ros_dist[2]]
bars = ax.bar(classes, values_ros, color=['#3498db', '#9b59b6', '#1abc9c'], edgecolor='black', linewidth=1.5)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height}\n({height/sum(values_ros)*100:.1f}%)',
            ha='center', va='bottom', fontweight='bold')
ax.set_ylabel('Nombre d\'échantillons', fontweight='bold')
ax.set_title('APRÈS RandomOverSampler (ROS)', fontweight='bold')
ax.set_ylim([0, 17000])
ax.grid(axis='y', alpha=0.3)

# Après RUS
rus_dist = {0: 1144, 1: 1144, 2: 1144}
ax = axes[2]
values_rus = [rus_dist[0], rus_dist[1], rus_dist[2]]
bars = ax.bar(classes, values_rus, color=['#e67e22', '#c0392b', '#16a085'], edgecolor='black', linewidth=1.5)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height}\n({height/sum(values_rus)*100:.1f}%)',
            ha='center', va='bottom', fontweight='bold')
ax.set_ylabel('Nombre d\'échantillons', fontweight='bold')
ax.set_title('APRÈS RandomUnderSampler (RUS)', fontweight='bold')
ax.set_ylim([0, 17000])
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('2_class_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 2 sauvegardé: 2_class_distribution.png")
plt.close()

# ============================================
# FIGURE 3: F1-SCORE DÉTAILLÉ PAR CLASSE
# ============================================

f1_scores = {
    'Base (TF-IDF)': {'Hate': 0.21, 'Offensive': 0.93, 'Neither': 0.79},
    'SelectKBest': {'Hate': 0.27, 'Offensive': 0.93, 'Neither': 0.80},
    'SelectKBest+ROS': {'Hate': 0.36, 'Offensive': 0.90, 'Neither': 0.82},
    'SelectKBest+RUS': {'Hate': 0.35, 'Offensive': 0.87, 'Neither': 0.81}
}

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(f1_scores))
width = 0.25

hate_scores = [f1_scores[model]['Hate'] for model in f1_scores.keys()]
offensive_scores = [f1_scores[model]['Offensive'] for model in f1_scores.keys()]
neither_scores = [f1_scores[model]['Neither'] for model in f1_scores.keys()]

bars1 = ax.bar(x - width, hate_scores, width, label='Hate Speech', color='#e74c3c', edgecolor='black')
bars2 = ax.bar(x, offensive_scores, width, label='Offensive Language', color='#f39c12', edgecolor='black')
bars3 = ax.bar(x + width, neither_scores, width, label='Neither', color='#2ecc71', edgecolor='black')

# Ajouter les valeurs sur les barres
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel('F1-Score', fontweight='bold', fontsize=12)
ax.set_title('F1-Score Détaillé par Classe et par Modèle', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(f1_scores.keys(), rotation=30, ha='right')
ax.legend(loc='lower right', fontsize=11)
ax.set_ylim([0, 1.05])
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('3_f1_by_class.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 3 sauvegardé: 3_f1_by_class.png")
plt.close()

# ============================================
# FIGURE 4: CONFUSION MATRIX (MEILLEUR MODÈLE)
# ============================================

cm = np.array([[158, 100, 28],
               [401, 3247, 190],
               [41, 59, 733]])

fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(cm, cmap='Blues', aspect='auto')

# Ajouter les étiquettes
classes = ['Hate Speech', 'Offensive Language', 'Neither']
ax.set_xticks(np.arange(len(classes)))
ax.set_yticks(np.arange(len(classes)))
ax.set_xticklabels(classes, rotation=45, ha='right')
ax.set_yticklabels(classes)

ax.set_xlabel('Prédictions', fontweight='bold', fontsize=12)
ax.set_ylabel('Réalité', fontweight='bold', fontsize=12)
ax.set_title('Matrice de Confusion - SelectKBest χ² (Meilleur Modèle)', fontweight='bold', fontsize=14)

# Ajouter les valeurs
for i in range(len(classes)):
    for j in range(len(classes)):
        text = ax.text(j, i, cm[i, j],
                      ha="center", va="center", color="black", fontsize=14, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Fréquence', rotation=270, labelpad=20, fontweight='bold')

plt.tight_layout()
plt.savefig('4_confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 4 sauvegardé: 4_confusion_matrix.png")
plt.close()

# ============================================
# FIGURE 5: TABLEAU RÉCAPITULATIF
# ============================================

fig, ax = plt.subplots(figsize=(14, 5))
ax.axis('tight')
ax.axis('off')

# Préparer les données du tableau
table_data = []
table_data.append(['Modèle', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Observations'])
for idx, row in df_results.iterrows():
    obs = '🏆 MEILLEUR' if idx == best_model_idx else ''
    if idx == 2:
        obs = '↑ Rappel / ↓ Précision'
    elif idx == 3:
        obs = '↑↑ Rappel / Données ↓'
    table_data.append([
        row['Modèle'],
        f"{row['Accuracy']:.4f}",
        f"{row['Precision']:.4f}",
        f"{row['Recall']:.4f}",
        f"{row['F1-Score']:.4f}",
        obs
    ])

table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.12, 0.12, 0.12, 0.12, 0.27])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Colorer les en-têtes
for i in range(len(table_data[0])):
    table[(0, i)].set_facecolor('#3498db')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Colorer la meilleure ligne
for i in range(len(table_data[0])):
    table[(best_model_idx + 1, i)].set_facecolor('#d5f4e6')

plt.title('Tableau Récapitulatif - Tous les Modèles', fontweight='bold', fontsize=14, pad=20)
plt.savefig('5_summary_table.png', dpi=300, bbox_inches='tight')
print("✅ Graphique 5 sauvegardé: 5_summary_table.png")
plt.close()

print("\n✅ TOUS LES GRAPHIQUES GÉNÉRÉS AVEC SUCCÈS!")
print("\nFichiers créés:")
print("  1. 1_metrics_comparison.png - Comparaison des métriques")
print("  2. 2_class_distribution.png - Distribution des classes")
print("  3. 3_f1_by_class.png - F1-Score par classe")
print("  4. 4_confusion_matrix.png - Matrice de confusion")
print("  5. 5_summary_table.png - Tableau récapitulatif")
