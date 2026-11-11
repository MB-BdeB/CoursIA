from ultralytics import YOLO
from pathlib import Path

# ── 1. Chemins ──────────────────────────────────────────────────
IMAGE_DIR  = Path("data/images")
OUTPUT_DIR = Path("data/results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 2. Chargement du modèle ─────────────────────────────────────
# yolov8m-seg.pt est téléchargé automatiquement à la racine du projet
# lors de la première exécution (~52 Mo)
model = YOLO("yolov8m-seg.pt")

# ── 3. Inventaire des images ────────────────────────────────────
images = list(IMAGE_DIR.glob("*.jpg")) + list(IMAGE_DIR.glob("*.jpeg"))
print(f"Images disponibles : {len(images)}")

# ── 4. Inférence de segmentation ────────────────────────────────
# On limite à 5 images pour ce test initial
for img_path in images[:5]:
    results = model.predict(
        source=str(img_path),
        conf=0.25,              # seuil de confiance minimal
        save=True,              # sauvegarde les images annotées
        project=str(OUTPUT_DIR),
        name="predict",
        exist_ok=True
    )
    for r in results:
        labels = [model.names[int(c)] for c in r.boxes.cls]
        print(f"{img_path.name}  →  objets détectés : {set(labels)}")

print("Inférence terminée.")
print("Résultats dans : runs/segment/predict/")
