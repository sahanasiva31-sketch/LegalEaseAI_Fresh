import os
from typing import Optional

from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    genai = None

load_dotenv()


class GeminiDocumentGenerator:
    """Generate structured legal-document drafts using Google's Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Create a .env file from .env.example."
            )

        if genai is None:
            raise RuntimeError(
                "google-generativeai is not installed. Run: pip install -r requirements.txt"
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        prompt = f"""
You are a legal-document drafting assistant.

Create a professional draft for the requested document. Do not claim that
the result is legal advice, legally binding, or reviewed by a lawyer.

Document type:
{document_type}

Parties:
{parties}

Terms and conditions:
{terms}

Effective date:
{dates}

Requirements:
1. Use clear professional legal language.
2. Include a title.
3. Include the parties and effective date.
4. Convert the supplied terms into appropriate clauses.
5. Add sensible standard sections when appropriate, such as definitions,
   obligations, confidentiality, payment, termination, governing law,
   notices, and signatures. Do not invent specific facts that were not supplied.
6. Use plain text headings rather than Markdown tables.
7. End with signature placeholders.
8. Return only the document draft.
"""
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
