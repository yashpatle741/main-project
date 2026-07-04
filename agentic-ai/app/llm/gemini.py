import json
import re

from google import genai

from config.config import settings
from llm.prompts import SYSTEM_PROMPT
from models.ai_response import AIResponse
from models.analysis import AnalysisReport


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"

    def analyze(self, report: AnalysisReport) -> AIResponse:

        prompt = f"""
{SYSTEM_PROMPT}

Namespace:
{report.namespace}

Pod:
{report.pod}

Issue:
{report.issue}

Events:
{json.dumps(report.events, indent=2)}

Logs:
{report.logs[:4000]}
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            text = response.text.strip()

            # Remove markdown code fences if Gemini returns them
            text = re.sub(r"^```json", "", text, flags=re.IGNORECASE).strip()
            text = re.sub(r"^```", "", text).strip()
            text = re.sub(r"```$", "", text).strip()

            data = json.loads(text)

            return AIResponse(
                root_cause=data.get("root_cause", "Unknown"),
                confidence=int(data.get("confidence", 0)),
                action=data.get("action", "no_action"),
                deployment=data.get("deployment", ""),
                reason=data.get("reason", ""),
            )

        except Exception as e:

            return AIResponse(
                root_cause="Gemini request failed",
                confidence=0,
                action="no_action",
                deployment="",
                reason=str(e),
            )
            