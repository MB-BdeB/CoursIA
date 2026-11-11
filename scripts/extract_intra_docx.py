from pathlib import Path
from docx import Document

docx_path = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\A57-EcoSysteme_IA\Examen_Intra_Marouane_Bouriel.docx")
out_path = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\scripts\Examen_Intra_Marouane_Bouriel.txt")

doc = Document(str(docx_path))
lines = []
for p in doc.paragraphs:
    text = p.text.strip()
    if text:
        lines.append(text)

out_path.write_text("\n".join(lines), encoding="utf-8")
print(f"WROTE:{out_path}")
