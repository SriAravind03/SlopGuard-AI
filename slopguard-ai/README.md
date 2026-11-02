# SlopGuard AI

SlopGuard is a Flask application for reviewing low-quality writing patterns. It measures repetition, generic filler, sentence variety, word overlap, potential keyword stuffing, and a simple information-density proxy. It does **not** claim that AI authorship can be determined from these patterns.

## Run locally

Requires Python 3.11 or newer.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `SECRET_KEY` to a random value in `.env`, then start the app:

```powershell
python app.py
```

Open `http://127.0.0.1:5000`. The app creates a local SQLite database automatically. For deployment set `DATABASE_URL` to a PostgreSQL SQLAlchemy URI, `COOKIE_SECURE=1` behind HTTPS, and a strong `SECRET_KEY`.

## Run with Docker Compose

Docker Desktop must be installed and running. From the project directory:

```powershell
Copy-Item .env.example .env
```

Replace `SECRET_KEY` with the output of `python -c "import secrets; print(secrets.token_urlsafe(48))"` and set `POSTGRES_PASSWORD` to a long URL-safe password. Start the app and database:

```powershell
docker compose up --build
```

Open `http://127.0.0.1:5000`; `/health` reports app/database readiness. Compose binds the app port to localhost and stores PostgreSQL data in a named volume. Stop the demo with `Ctrl+C` (data remains in the volume; `docker compose down -v` removes it).

## Optional models

The baseline analyzer works offline. `HF_MODEL` enables a configured Transformers text-classification model and `HF_EMBEDDING_MODEL` enables sentence embeddings for redundancy analysis. Install `requirements-optional.txt` to add those model libraries; model availability and labels depend on the configured models and are not treated as authorship proof. No model weights are downloaded unless a feature is enabled. If a package/model is missing, the analyzer falls back to transparent heuristics.

Set `OPENAI_API_KEY` to enable the optional review checkbox in the text analyzer. Only selected text is sent to the configured OpenAI model. The response is treated as supplementary and failures leave heuristic results intact. Scraped text is passed as quoted untrusted content and the prompt instructs the model not to follow embedded instructions.

## Scoring

The score is intentionally transparent: 25% inverse information-density proxy, 22% repeated-word-pair / sentence repetition, 18% sentence word overlap, 20% generic phrase / transition frequency, 10% potential keyword stuffing, and 5% broad writing-pattern signals. These are heuristic signals, and quality depends on topic and genre. Content quality is `100 - slop pattern score`. Classifications are high quality (<35 slop), mixed (35–59), or likely low quality (60+). AI authorship remains inconclusive.

The semantic redundancy metric uses Jaccard word overlap as an offline proxy unless a sentence-embedding model is configured. Scikit-learn and NLTK are available in `requirements-optional.txt` for future configurable enrichments; no unvalidated detector is silently enabled.

## Security

Passwords use Werkzeug's adaptive password hashing. Forms use Flask-WTF CSRF protection. Scraping accepts public HTTP(S) only, checks DNS results and every redirect against non-public IPs, uses bounded timeouts and response sizes, and only parses HTML text. Authenticated users can see only their own scans. API keys remain server-side.

## Tests

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover scoring, fallback behavior, URL validation, authentication, database-backed scan history, CSRF, and response headers. Network fetching is not exercised against live hosts.
