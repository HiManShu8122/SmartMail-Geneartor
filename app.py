"""SmartMail Generator Flask application."""

import os

from flask import Flask, jsonify, render_template, request
from openai import OpenAI


DEFAULT_MODEL = "gpt-5.2"
TONE_OPTIONS = ("professional", "friendly", "formal", "casual", "persuasive")


def create_app() -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)

    @app.get("/")
    def index():
        """Render the email generation form."""
        return render_template("index.html", tones=TONE_OPTIONS)

    @app.post("/generate")
    def generate_email():
        """Generate an email from a topic and tone."""
        payload = request.get_json(silent=True) or {}
        topic = request.form.get("topic") or payload.get("topic")
        tone = request.form.get("tone") or payload.get("tone") or "professional"
        recipient = request.form.get("recipient") or payload.get("recipient") or ""

        if not topic or not topic.strip():
            return jsonify({"error": "Please provide an email topic."}), 400

        normalized_tone = tone.strip().lower()
        if normalized_tone not in TONE_OPTIONS:
            return jsonify({"error": "Please choose a supported tone."}), 400

        email = build_email(topic.strip(), normalized_tone, recipient.strip())
        return jsonify({"email": email})

    return app


def build_email(topic: str, tone: str, recipient: str = "") -> str:
    """Generate an email body with OpenAI's Responses API."""
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    recipient_context = f" The email recipient is {recipient}." if recipient else ""
    prompt = (
        f"Write a concise {tone} email about: {topic}.{recipient_context} "
        "Include a clear subject line, greeting, short body, and sign-off."
    )

    response = client.responses.create(
        model=model,
        instructions=(
            "You are an expert assistant that writes polished, practical emails. "
            "Return only the completed email text."
        ),
        input=prompt,
    )
    return response.output_text.strip()


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
