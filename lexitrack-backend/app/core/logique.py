from datetime import datetime
import json
import re
from . import ai_assistant
from typing import Optional


from .. import schemas
from .. import models


from datetime import datetime
import json
import re
from typing import Optional

from . import ai_assistant
from .. import schemas


class LexiProcessor:
    def __init__(self):
        self.ai = ai_assistant.AIAssistant()

    def _safe_parse_json(self, raw: str):
        if not raw or not raw.strip():
            raise ValueError("Réponse IA vide")

        match = re.search(r"\{.*\}|\[.*\]", raw, re.S)
        if not match:
            raise ValueError(f"Aucun JSON détecté dans la sortie IA : {raw}")

        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur JSON : {e} | Contenu extrait : {json_str}")

    def _prepare_payload(
        self,
        parsed: dict,
        source_type: str,
        url: Optional[str] = None,
        file_name: Optional[str] = None,
    ):
        summary_content = parsed.get("summary", {"short": "", "detailed": ""})
        questions_content = parsed.get("questions", [])
        return schemas.SummaryCreate(
            source_type=source_type,
            url=url,
            file_name=file_name,
            title=parsed.get("title") or "Sans titre",
            summary=summary_content,
            questions=questions_content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    def process_from_url(self, url: str):
        raw_output = self.ai.summarize_url(url)
        parsed = self._safe_parse_json(raw_output)
        return self._prepare_payload(parsed, source_type="web", url=url)

    def process_from_pdf(self, file_path: str):
        raw_output = self.ai.summarize_pdf(file_path)
        parsed = self._safe_parse_json(raw_output)
        return self._prepare_payload(
            parsed, source_type="pdf", file_name=file_path.split("/")[-1]
        )
