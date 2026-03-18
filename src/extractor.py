import json
import base64
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

CSV_FIELDS = [
    "Belegnummer",
    "Belegdatum",
    "Belegart",
    "Vertragspartner",
    "Bereich",
    "Kategorie",
    "Fälligkeitsdatum",
    "Steuerbetrag",
    "Bruttobetrag",
]

SYSTEM_PROMPT = """You are a receipt and invoice data extraction assistant.
Extract the following fields from the provided document and return ONLY a JSON object with these keys:

- Belegnummer (Receipt Number)
- Belegdatum (Receipt Date, format: DD.MM.YYYY)
- Belegart (Receipt Type, e.g. Rechnung, Quittung, Gutschrift)
- Vertragspartner (Contract Partner / vendor name)
- Bereich (Area/Department)
- Kategorie (Category, e.g. Büromaterial, Reisekosten, IT)
- Fälligkeitsdatum (Due Date, format: DD.MM.YYYY)
- Steuerbetrag (Tax Amount, numeric with 2 decimals)
- Bruttobetrag (Gross Amount, numeric with 2 decimals)

If a field cannot be determined from the document, use an empty string "".
Return ONLY the JSON object, no other text."""


def extract_from_text(text: str) -> dict:
    """Extract receipt fields from plain text (e.g. PDF text content)."""
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Extract data from this document:\n\n{text}"}
        ],
    )
    return _parse_response(message)


def extract_from_image(file_path: str) -> dict:
    """Extract receipt fields from an image file."""
    path = Path(file_path)
    image_data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")

    extension = path.suffix.lower()
    media_type_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    media_type = media_type_map.get(extension, "image/png")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Extract data from this receipt/invoice image.",
                    },
                ],
            }
        ],
    )
    return _parse_response(message)


def _parse_response(message) -> dict:
    """Parse Claude's response into a dict with the expected fields."""
    raw = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0]

    data = json.loads(raw)

    # Ensure all expected fields are present
    return {field: data.get(field, "") for field in CSV_FIELDS}
