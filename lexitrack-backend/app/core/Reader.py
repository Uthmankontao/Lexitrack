import requests
from bs4 import BeautifulSoup
import pathlib
from pdfminer.high_level import extract_text
import fitz  # PyMuPDF
# Ce qu’il fait : lit et extrait le texte des sources (pages web, PDFs).

# Rôle : première étape du pipeline LexiTrack (capturer le contenu à traiter).

class ReaderError(Exception):
    pass


class WebReader:
    def __init__(self, url: str):
        self.url = url

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ReaderError(f"Erreur lors de la récupération de l'URL : {e}")

    def extract_text(self):
        html = self.fetch()
        soup = BeautifulSoup(html, "html.parser")

        # Supprimer les balises inutiles
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Détection du titre
        title_tag = soup.find("h1") or soup.title
        title = title_tag.get_text(strip=True) if title_tag else "Sans titre"

        content_blocks = []
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            if element.name.startswith('h'):
                content_blocks.append(f"\n\n{element.get_text(strip=True).upper()}\n")
            elif element.name == 'p':
                paragraph = element.get_text(strip=True)
                if paragraph:
                    content_blocks.append(paragraph)

        return {
            "source": "web",
            "title": title,
            "text": "\n".join(content_blocks)
        }


class PDFReader:
    def __init__(self, filepath: str):
        self.filepath = pathlib.Path(filepath)

    def extract_text(self):
        if not self.filepath.exists():
            raise ReaderError(f"Fichier PDF introuvable : {self.filepath}")

        try:
            # Essayer de lire le titre via métadonnées (optionnel)
            try:
                with fitz.open(str(self.filepath)) as doc:
                    metadata = doc.metadata
                    title = metadata.get("title") or "Sans titre"
            except Exception:
                title = "Sans titre"

            text = extract_text(str(self.filepath))
            return {
                "source": "pdf",
                "title": title.strip(),
                "text": text.strip()
            }

        except Exception as e:
            raise ReaderError(f"Erreur lors de la lecture du PDF : {e}")



# def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> dict:
#     with io.BytesIO(pdf_bytes) as pdf_file:
#         try:
#             with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
#                 metadata = doc.metadata
#                 title = metadata.get("title") or "Sans titre"
#                 text = ""
#                 for page in doc:
#                     text += page.get_text()
#             return {
#                 "source": "pdf",
#                 "title": title.strip(),
#                 "text": text.strip()
#             }
#         except Exception as e:
#             raise ReaderError(f"Erreur lors de la lecture du PDF en mémoire : {e}")


# def extract_text_from_url(url: str) -> dict:
#     reader = WebReader(url)
#     return reader.extract_text()
