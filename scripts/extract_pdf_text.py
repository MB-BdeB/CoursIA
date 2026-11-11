from pathlib import Path
from pypdf import PdfReader

pdf_path = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\A57-EcoSysteme_IA\Projet_Ecosysteme_dIA.pdf")
output_path = Path(r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\scripts\Projet_Ecosysteme_dIA.txt")

reader = PdfReader(str(pdf_path))
with output_path.open("w", encoding="utf-8") as out:
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            out.write(f"--- Page {i} ---\n")
            out.write(text)
            out.write("\n\n")
print(f"WROTE:{output_path}")
