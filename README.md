# LegalEase - AI-Powered Legal Document Generator

LegalEase is a FastAPI + Streamlit application based on the supplied project brief.

## Architecture

```text
Streamlit Frontend
       |
       | POST /generate
       v
FastAPI Backend
       |
       v
GeminiDocumentGenerator
       |
       v
Google Gemini API
       |
       v
Generated legal draft
       |
       +---- HTML preview
       +---- TXT export
       +---- DOCX export
       +---- PDF export
```

## Project structure

```text
LegalEaseAI/
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── generator.py
│   └── ai_core/
│       ├── __init__.py
│       └── gemini_generator.py
├── frontend/
│   ├── __init__.py
│   └── app.py
├── image/
│   └── logo.png
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
├── run_backend.bat
├── run_frontend.bat
├── run_backend.sh
├── run_frontend.sh
└── README.md
```

## 1. Open the project

Windows PowerShell:

```powershell
cd LegalEaseAI
```

## 2. Create virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

Create `.env` from `.env.example`.

```text
GEMINI_API_KEY=YOUR_REAL_API_KEY
GEMINI_MODEL=gemini-1.5-pro
BACKEND_URL=http://127.0.0.1:8000
```

Do not commit `.env` to Git.

## 5. Start FastAPI

```powershell
python -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8000 --reload
```

API:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## 6. Start Streamlit

Open a second terminal, activate the same environment, then:

```powershell
python -m streamlit run frontend/app.py
```

Streamlit normally opens:

```text
http://localhost:8501
```

## 7. Test

Example values:

Document Type:
```text
Freelance Work Contract
```

Parties:
```text
Jane Doe (Service Provider), TechNova Inc. (Client)
```

Terms:
```text
Payment to be made within 30 days of invoice; Confidentiality must be maintained; Either party may terminate with 15 days notice
```

Effective Date:
```text
April 15, 2025
```

The generated draft can be edited and exported as TXT, DOCX, or PDF.

## Notes

- The supplied brief specifies Gemini 1.5 Pro and `google-generativeai`; those choices are reflected in this implementation.
- Model availability can change. If the configured Gemini model is unavailable for your API account, change `GEMINI_MODEL` in `.env`.
- Replace `image/logo.png` with the organization's real logo if required.
- This application generates drafts and does not replace legal review.
