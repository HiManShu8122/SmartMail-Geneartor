# SmartMail Generator

SmartMail Generator is an intelligent Flask web application that helps users draft professional or personal emails with AI. Provide a topic, optional recipient context, and a tone; the app returns a polished email with a subject line, greeting, concise body, and sign-off.

## Features

- Home page at `/` with a simple email generation form.
- JSON email-generation endpoint at `/generate`.
- Tone options for professional, friendly, formal, casual, and persuasive emails.
- OpenAI Responses API integration with a configurable model.

## Project structure

```text
.
├── app.py
├── static/
│   └── styles.css
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── requirements.txt
└── .env.example
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   export OPENAI_API_KEY="your_api_key_here"
   ```

   Optionally set `OPENAI_MODEL` to another compatible text-generation model.

## Run the app

```bash
flask --app app run
```

Open <http://127.0.0.1:5000> and generate an email from the form.

## API usage

```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H 'Content-Type: application/json' \
  -d '{"topic":"Follow up after a product demo","tone":"professional","recipient":"Jordan"}'
```

## Testing

```bash
pytest
```
