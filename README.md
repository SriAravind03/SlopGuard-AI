# 🛡️ SlopGuard AI – AI Slop Detection System

An AI-powered web application designed to identify low-quality, repetitive, misleading, spam-like, and potentially AI-generated online content using Natural Language Processing (NLP), Machine Learning, and Large Language Models.

## 🚀 Overview

SlopGuard AI is an intelligent content analysis platform that evaluates the quality and usefulness of online content.

It analyzes text and webpage content to identify common AI slop patterns, including repetitive phrases, generic statements, keyword stuffing, low information density, and suspicious linguistic patterns.

The system combines traditional NLP techniques, Hugging Face Transformers, web scraping, and OpenAI API-powered analysis to generate explainable content quality reports.

**Note:** AI-generated content is not necessarily low-quality. SlopGuard AI evaluates content quality and suspicious patterns rather than claiming to determine authorship with certainty.

## ✨ Key Features

- **Text Analysis:** Analyze user-submitted text for repetitive and low-quality patterns.
- **URL Analysis:** Extract and analyze webpage content using web scraping.
- **AI Pattern Analysis:** Examine linguistic patterns using NLP and transformer models.
- **Content Quality Scoring:** Evaluate information density, vocabulary diversity, and repetition.
- **SEO Spam Detection:** Identify keyword stuffing and unnatural keyword patterns.
- **Semantic Analysis:** Identify redundant sentences and repeated information.
- **AI-Powered Explanations:** Generate detailed analysis using OpenAI API.
- **Interactive Dashboard:** Display analysis results and detection statistics.
- **Scan History:** Store and review previous content analyses.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Flask | Web framework |
| Hugging Face Transformers | NLP and transformer-based analysis |
| OpenAI API | AI-powered content analysis |
| BeautifulSoup | Web scraping |
| Trafilatura | Article extraction |
| Sentence Transformers | Semantic similarity |
| Scikit-learn | Machine learning |
| NLTK | Text preprocessing |
| SQLite | Database |
| HTML, CSS, JavaScript | Frontend |
| Bootstrap | Responsive UI |
| Chart.js | Data visualization |

## 🏗️ System Architecture

1. **Input Layer:** Accepts text or webpage URLs.
2. **Extraction Layer:** Extracts and cleans webpage content.
3. **NLP Processing Layer:** Performs text preprocessing and linguistic analysis.
4. **AI Analysis Layer:** Uses Hugging Face and OpenAI for advanced analysis.
5. **Scoring Engine:** Combines content-quality indicators.
6. **Presentation Layer:** Displays scores, explanations, and recommendations.

## 📊 Detection Parameters

SlopGuard AI evaluates content using several indicators:

- Repetitive sentence patterns
- Generic phrase frequency
- Vocabulary diversity
- Sentence length variation
- Semantic redundancy
- Information density
- Keyword stuffing
- Linguistic patterns

## 📁 Project Structure

```text
SlopGuard-AI/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── detection/
│   ├── text_preprocessor.py
│   ├── repetition_detector.py
│   ├── semantic_analyzer.py
│   ├── quality_analyzer.py
│   ├── ai_pattern_detector.py
│   ├── openai_analyzer.py
│   └── scoring_engine.py
│
├── scraper/
│   └── url_scraper.py
│
├── models/
│   └── database.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   └── analyzer.py
│
├── templates/
├── static/
│   ├── css/
│   └── js/
│
├── tests/
│
└── README.md
```

*The structure above represents the planned architecture; update it to match the actual implemented files.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SlopGuard-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd SlopGuard-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file using `.env.example` as a template.

```env
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///slopguard.db
```

Never upload your `.env` file or API keys to GitHub.

### 7. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## 🔍 Example Use Cases

- Analyze suspicious online articles.
- Identify repetitive AI-generated content patterns.
- Evaluate the informational quality of blog posts.
- Detect keyword-stuffed webpages.
- Investigate low-quality content websites.
- Study the impact of mass-produced AI content.

## 🔐 Security Considerations

- Secure user authentication.
- Password hashing.
- API key protection using environment variables.
- URL validation and SSRF protection.
- Input validation and sanitization.
- Request timeout and response size limits.
- Safe handling of scraped webpage content.

## ⚠️ Limitations

- AI-generated text detection is probabilistic and cannot reliably establish authorship.
- Short text samples may produce unreliable results.
- Different writing styles can affect detection outcomes.
- External API availability can affect advanced analysis.
- Content quality scores are indicators, not objective judgments of truth.

## 🧪 Testing

Run automated tests using:

```bash
pytest
```

## 🔮 Future Enhancements

- Browser extension for real-time webpage analysis.
- Batch URL scanning.
- Duplicate content detection across websites.
- Clickbait headline detection.
- Fact-checking integration.
- Multilingual content analysis.
- Social media content analysis.
- Advanced content moderation dashboard.

## 👨‍💻 Developer

**Project Name:** SlopGuard AI  
**Category:** Artificial Intelligence | Natural Language Processing | Web Security  
**Primary Language:** Python  
**Framework:** Flask

## 📜 License

This project is intended for educational and research purposes. A license can be added to define its reuse and distribution terms.

---

**SlopGuard AI – Detect the noise. Discover the value.**
