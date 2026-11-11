from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from pathlib import Path

out_path = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\Synthese_Ecosysteme_IA.docx")
watchdog_output = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\scripts\watchdog_output.txt")

# Contenu de la synthèse (français technique)
title = "Synthèse technique — Mise en place d'un Écosystème d'IA"

doc = Document()

# Styles
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Page de garde
doc.add_heading(title, level=0)
doc.add_paragraph("Cours : Mise en place d'un écosystème d'IA — AEC (Spécialisation technique)")
doc.add_paragraph("Enseignant : Dr. Komi Sodoké")
doc.add_paragraph("Date : 06/06/2026")

doc.add_page_break()

# Résumé
doc.add_heading('Résumé', level=1)
doc.add_paragraph(
    "Ce document présente une synthèse technique du projet de mise en place, virtualisation et monitoring d'un écosystème d'entraînement pour modèles d'intelligence artificielle. "
    "Il couvre le dimensionnement matériel (analyse comparée de deux options), les contrôles d'environnement d'exécution, la conteneurisation via Docker et la conception d'un agent de monitoring (watchdog) pour détecter et réagir aux anomalies matérielles."
)

# Introduction
doc.add_heading('Introduction', level=1)
doc.add_paragraph(
    "La montée en charge des modèles IA impose une architecture maîtrisée entre performances GPU, admission CPU et interconnexions PCIe. L'objectif de ce projet est de fournir un protocole reproductible pour dimensionner, containeriser et surveiller une plateforme d'entraînement."
)

# Partie 1
doc.add_heading("1. Dimensionnement et choix matériel", level=1)
doc.add_paragraph("Contexte : entraînement d'un grand modèle de traitement de langage (LLM). Deux options sont proposées :")

doc.add_paragraph("Option A : 1x NVIDIA A100 (40 Go), CPU 8 cœurs, 16 lignes PCIe Gen4.")
doc.add_paragraph("Option B : 4x NVIDIA RTX 4090 (24 Go chacun), CPU 16 cœurs, 24 lignes PCIe Gen4 (partagées).")

doc.add_paragraph("Analyse technique :")
doc.add_paragraph(
    "- L'Option A offre une grande VRAM unifiée (40 Go) adaptée aux modèles larges sans sharding agressif; moins de complexité en communication inter-GPU. "
    "- L'Option B fournit davantage de cœurs de calcul cumulés mais nécessite une orchestration multi-GPU (NVLink/PCIe) et pose des contraintes PCIe où le partage des lignes peut engendrer des goulots d'étranglement lors des transferts CPU↔GPU."
)

doc.add_paragraph("Recommandation technique : choisir l'Option A si le modèle tient en 40 Go VRAM ou si l'on privilégie la simplicité opérationnelle; choisir l'Option B pour entraînements distribués massifs nécessitant un partitionnement de données, en s'assurant d'un réseau NVLink ou d'une architecture PCIe adaptée et d'un CPU plus puissant (≥32 cœurs recommandés dans ce cas).")

# Partie 2
doc.add_heading('2. Audit de l’environnement et validation (Colab)', level=1)
doc.add_paragraph('Procédure de vérification clés :')
doc.add_paragraph('1) Vérifier le système et l’architecture : commande uname et /proc/cpuinfo.')
doc.add_paragraph('2) Vérifier la présence du pilote NVIDIA et la version CUDA via nvidia-smi.')
doc.add_paragraph('3) Vérifier l’accessibilité GPU par PyTorch (torch.cuda.is_available()).')

doc.add_paragraph('Interprétation : la sortie de nvidia-smi fournit le nom du GPU, la mémoire totale VRAM et la version du driver; ces informations conditionnent le choix des binaires PyTorch/CUDA. En cas d’incompatibilité, aligner les versions CUDA entre driver et package PyTorch.')

# Partie 3
doc.add_heading('3. Conteneurisation (Dockerfile)', level=1)
doc.add_paragraph('Dockerfile recommandé (expliqué) :')

dockerfile = (
"FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04\n"
"RUN apt-get update && apt-get install -y \\\n    python3-pip \\\n    python3-dev \\\n    && rm -rf /var/lib/apt/lists/*\n"
"RUN pip3 install torch pandas\n"
"WORKDIR /app\n"
"COPY train.py /app/\n"
"CMD [\"python3\", \"train.py\"]\n"
)

doc.add_paragraph(dockerfile)

doc.add_paragraph('Commentaires : utiliser une image CUDA fournie par NVIDIA garantit la compatibilité runtime. Pour PyTorch GPU, préférez installer la roue officielle adaptée à la version CUDA cible (ex : index URL PyTorch si besoin).')

# Partie 4
doc.add_heading('4. Monitoring et Watchdog', level=1)
doc.add_paragraph('Principe : une boucle de surveillance lit périodiquement des métriques (température GPU, erreurs ECC, utilisation mémoire) et déclenche des contre-mesures. Les règles métiers typiques présentées :')

doc.add_paragraph('- Rule 1 : Température >82°C → alerte Thermal Throttling.')
doc.add_paragraph('- Rule 2 : Erreurs ECC >10 → basculement/isolement du nœud (maintenance).')

doc.add_paragraph('Watchdog — script Python (extrait en annexe) : logique de collecte simulée, règles de seuil et action de mise hors ligne. Le script de simulation génère une sortie qui est jointe en annexe.')

# Critères d’évaluation
doc.add_heading('Critères d’évaluation', level=1)
doc.add_paragraph('- Rigueur de l’analyse matérielle : 25 points')
doc.add_paragraph('- Exécution et justesse des commandes systèmes : 25 points')
doc.add_paragraph('- Syntaxe et logique du Dockerfile : 25 points')
doc.add_paragraph('- Fonctionnement de la boucle d’alerte du Watchdog : 25 points')

# Conclusion
doc.add_heading('Conclusion et recommandations', level=1)
doc.add_paragraph('Pour déployer un écosystème IA robuste, prioriser la compatibilité CUDA/driver, dimensionner la VRAM en fonction du modèle, et mettre en place un monitoring proactif. Automatiser la construction d’images et les tests d’intégrité GPU dans la CI/CD.')

# Annexes
doc.add_page_break()
doc.add_heading('Annexes', level=1)

# Annex A: Dockerfile complet
doc.add_heading('Annexe A — Dockerfile complet', level=2)
doc.add_paragraph(dockerfile)

# Annex B: Script Watchdog complet
doc.add_heading('Annexe B — Script Watchdog (watchdog_simulate.py)', level=2)

watchdog_code = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\scripts\watchdog_simulate.py").read_text(encoding='utf-8')
for line in watchdog_code.splitlines():
    p = doc.add_paragraph(line)
    p.style = doc.styles['No Spacing'] if 'No Spacing' in doc.styles else p.style

# Annex C: Exemple de sortie de la simulation
if watchdog_output.exists():
    doc.add_heading('Annexe C — Exemple de sortie (watchdog_output.txt)', level=2)
    sample = watchdog_output.read_text(encoding='utf-8')
    for line in sample.splitlines():
        p = doc.add_paragraph(line)
        p.style = doc.styles['No Spacing'] if 'No Spacing' in doc.styles else p.style

# Save
out_path.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(out_path))
print(f"WROTE:{out_path}")
