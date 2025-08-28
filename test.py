# from app.core.reader import PDFReader, WebReader

# reader = PDFReader("les enseignements tirés du récit de Luqman le sage.pdf")

# #print(reader.extract_text())

# web_reader = WebReader("https://cs50.harvard.edu/ai/projects/1/minesweeper/")
# reader = web_reader.fetch()

# reader = web_reader.extract_text()
# print(reader)


# # test de web
# import requests
# import json

# url = "https://cs50.harvard.edu/ai/projects/1/minesweeper/"
# try:
#     page_content = requests.get(url, timeout=10).text
#     print(page_content)
# except Exception as e:
#     print(json.dumps({"error": f"Impossible de charger l'URL : {e}"}))