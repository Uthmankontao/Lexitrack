from openai import OpenAI
import json
from .. import config
from .Reader import WebReader, PDFReader

settings = config.get_settings()


class AIAssistant:
    def __init__(self):
        self.client = OpenAI()

    def _ask_ai(self, prompt: str):
        """Envoie la requête à OpenAI et récupère la réponse brute."""
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant qui résume des textes. Si le texte est en anglais alors résume le en français. Ne te limite pas aux bases et fais un long résumé détaillé si le sujet est long et necessite plus de clarté"
                        " Réponds uniquement avec un JSON valide."
                        " Structure attendue : "
                        '{"title":"...","summary":{"short":"...","detailed":"..."},"questions":[{"question":"...","answer":""}]}'
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        raw_output = resp.choices[0].message.content

        # Extraire le JSON même s'il y a du texte avant/après
        import json, re
        try:
            match = json.loads(raw_output)
            return self._normalize_output(match)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}|\[.*\]", raw_output, re.S)
            if not m:
                return json.dumps({"error": "Impossible d'extraire le JSON de la réponse IA"})
            try:
                return self._normalize_output(json.loads(m.group(0)))
            except Exception as e:
                return json.dumps({"error": f"Erreur JSON finale : {e}"})

    def _normalize_output(self, data: dict) -> str:
        """Transforme le résumé et les questions pour qu'ils soient compatibles Pydantic V2."""
        # Normalisation du résumé
        summary_data = data.get("summary", {})
        if isinstance(summary_data, str):
            summary_data = {"short": summary_data, "detailed": ""}
        elif not isinstance(summary_data, dict):
            summary_data = {"short": "", "detailed": ""}

        # Normalisation des questions en QAItem
        questions = data.get("questions", [])
        normalized_questions = []
        for q in questions:
            if isinstance(q, str):
                normalized_questions.append({"question": q, "answer": ""})
            elif isinstance(q, dict) and "question" in q:
                normalized_questions.append({
                    "question": q["question"],
                    "answer": q.get("answer", "")
                })

        # Assurer que le titre existe
        title = data.get("title", "Sans titre")

        return json.dumps({
            "title": title,
            "summary": summary_data,
            "questions": normalized_questions
        })

    def summarize_url(self, url: str):
        """Récupère la page et demande un résumé."""
        try:
            web_reader = WebReader(url)
            reader = web_reader.fetch()
            reader = web_reader.extract_text()
        except Exception as e:
            return json.dumps({"error": f"Impossible de charger l'URL : {e}"})

        prompt = (
            f"Voici le contenu d'une page web :\n\n{reader}\n\n"
            "(Si ça ressemble à un cours pour étudiant alors resume le cours en detaillant toutes les parties du cours. Prends ton pour bien faire et si c'est un article Fais un résumé bien détaillé, génère aussi une liste de questions pertinentes) "
            "au format JSON {'title':'...','summary':{'short':'...','detailed':'...'},'questions':[{'question':'...','answer':''}]}"
        )
        return self._ask_ai(prompt)

    def summarize_pdf(self, file_path: str):
        """Extrait texte du PDF et demande un résumé."""
        try:
            reader = PDFReader(file_path)
            reader = reader.extract_text()
        except Exception as e:
            return json.dumps({"error": f"Impossible de lire le PDF : {e}"})

        prompt = (
            f"Voici le contenu d'un document PDF :\n\n{reader}\n\n"
            "Fais un résumé bien détaillé, génère aussi une liste de questions pertinentes "
            "au format JSON {'title':'...','summary':{'short':'...','detailed':'...'},'questions':[{'question':'...','answer':''}]}"
        )
        return self._ask_ai(prompt)

