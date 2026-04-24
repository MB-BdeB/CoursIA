"""
Validation Croisée pour Random Forest
Comparer: SANS SMOTE vs AVEC SMOTE avec test_size=0.3
"""

from sklearn.model_selection import cross_validate, StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, recall_score, precision_score
from imblearn.over_sampling import SMOTE
import pandas as pd
import numpy as np

def cross_validation_comparison(X, y, n_splits=5):
    """
    Compare Random Forest avec et sans SMOTE en cross-validation
    """
    
    print("\n" + "="*80)
    print("VALIDATION CROISÉE: Random Forest avec/sans SMOTE")
    print("="*80)
    
    # Configuration
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # Définir le modèle
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    
    # ==================== 1. SANS SMOTE ====================
    print("\n1️⃣  SANS SMOTE (Balancement Natif)")
    print("-" * 80)
    
    results_without_smote = cross_validate(
        rf, X, y,
        cv=cv,
        scoring={
            'roc_auc': 'roc_auc',
            'f1': 'f1',
            'recall': 'recall',
            'precision': 'precision',
            'accuracy': 'accuracy'
        },
        n_jobs=-1,
        return_train_score=False
    )
    
    print_cv_results("SANS SMOTE", results_without_smote)
    
    # ==================== 2. AVEC SMOTE ====================
    print("\n\n2️⃣  AVEC SMOTE")
    print("-" * 80)
    
    # Stratégie: Appliquer SMOTE à chaque fold d'entraînement
    cv_scores_with_smote = {
        'test_roc_auc': [],
        'test_f1': [],
        'test_recall': [],
        'test_precision': [],
        'test_accuracy': []
    }
    
    fold_num = 1
    for train_idx, test_idx in cv.split(X, y):
        X_train_fold, X_test_fold = X.iloc[train_idx], X.iloc[test_idx]
        y_train_fold, y_test_fold = y.iloc[train_idx], y.iloc[test_idx]
        
        # Appliquer SMOTE UNIQUEMENT au fold d'entraînement
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train_fold, y_train_fold)
        
        # Entraîner le modèle
        rf.fit(X_train_resampled, y_train_resampled)
        
        # Prédire
        y_pred = rf.predict(X_test_fold)
        y_proba = rf.predict_proba(X_test_fold)[:, 1]
        
        # Calculer les métriques
        cv_scores_with_smote['test_roc_auc'].append(roc_auc_score(y_test_fold, y_proba))
        cv_scores_with_smote['test_f1'].append(f1_score(y_test_fold, y_pred))
        cv_scores_with_smote['test_recall'].append(recall_score(y_test_fold, y_pred))
        cv_scores_with_smote['test_precision'].append(precision_score(y_test_fold, y_pred))
        cv_scores_with_smote['test_accuracy'].append((y_pred == y_test_fold).mean())
        
        print(f"   Fold {fold_num}: ROC-AUC={cv_scores_with_smote['test_roc_auc'][-1]:.4f}, "
              f"F1={cv_scores_with_smote['test_f1'][-1]:.4f}, "
              f"Recall={cv_scores_with_smote['test_recall'][-1]:.4f}")
        fold_num += 1
    
    print_cv_results("AVEC SMOTE", cv_scores_with_smote)
    
    # ==================== COMPARAISON ====================
    print("\n\n📊 TABLEAU COMPARATIF")
    print("="*80)
    
    comparison = pd.DataFrame({
        'Métrique': ['ROC-AUC', 'F1-Score', 'Recall', 'Precision', 'Accuracy'],
        'SANS SMOTE (Moyenne)': [
            results_without_smote['test_roc_auc'].mean(),
            results_without_smote['test_f1'].mean(),
            results_without_smote['test_recall'].mean(),
            results_without_smote['test_precision'].mean(),
            results_without_smote['test_accuracy'].mean()
        ],
        'AVEC SMOTE (Moyenne)': [
            np.mean(cv_scores_with_smote['test_roc_auc']),
            np.mean(cv_scores_with_smote['test_f1']),
            np.mean(cv_scores_with_smote['test_recall']),
            np.mean(cv_scores_with_smote['test_precision']),
            np.mean(cv_scores_with_smote['test_accuracy'])
        ]
    })
    
    comparison['Différence'] = comparison['AVEC SMOTE (Moyenne)'] - comparison['SANS SMOTE (Moyenne)']
    comparison['Meilleur'] = comparison.apply(
        lambda row: '✅ SMOTE' if row['Différence'] > 0 else '❌ Sans SMOTE',
        axis=1
    )
    
    print(comparison.to_string(index=False))
    
    # ==================== RECOMMANDATION ====================
    print("\n\n🎯 RECOMMANDATION FINALE")
    print("="*80)
    
    meilleur_auc = max(
        results_without_smote['test_roc_auc'].mean(),
        np.mean(cv_scores_with_smote['test_roc_auc'])
    )
    
    with_smote_better = np.mean(cv_scores_with_smote['test_roc_auc']) > results_without_smote['test_roc_auc'].mean()
    
    if with_smote_better:
        print("✅ UTILISER: Random Forest AVEC SMOTE")
        print(f"   ROC-AUC moyen: {np.mean(cv_scores_with_smote['test_roc_auc']):.4f}")
        print(f"   Avantage: Meilleure Recall (détection de défauts)")
        print(f"   Remarque: SMOTE aide réellement le modèle!")
    else:
        print("✅ UTILISER: Random Forest SANS SMOTE")
        print(f"   ROC-AUC moyen: {results_without_smote['test_roc_auc'].mean():.4f}")
        print(f"   Conseil: Le balancement natif du RF suffit")

def print_cv_results(label, results):
    """Helper pour afficher les résultats CV"""
    metrics = ['roc_auc', 'f1', 'recall', 'precision', 'accuracy']
    
    print(f"\n{label}")
    for metric in metrics:
        key = f'test_{metric}'
        mean = results[key].mean()
        std = results[key].std()
        print(f"  {metric.upper():12s}: {mean:.4f} +/- {std:.4f}")


# Exemple d'utilisation
if __name__ == "__main__":
    """
    # À exécuter dans votre notebook
    from validation_croisee_RF import cross_validation_comparison
    
    cross_validation_comparison(X, y, n_splits=5)
    """
    pass
