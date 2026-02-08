<div align="center">
  <img src="frontend/public/logo.png" width="120" height="120" alt="HackMate Logo">
  <h1>HackMate v2.0</h1>
  <p><b>Professional Penetration Testing Platform with AI Assistance</b></p>

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
</div>

---

A full-stack web application designed for security professionals to manage penetration testing engagements following the **PTES methodology**. Features include an AI-powered assistant, integrated terminal, whitelisted security tools, and automated report generation.

## 🚀 Features

- 🎯 **Engagement Management** - Track and manage security projects from inception to completion.
- 🛡️ **PTES Methodology** - Structured 8-phase workflow with interactive AI guidance.
- 💻 **Integrated Terminal** - Execute security tools Safely with command whitelisting and persistence.
- 🪲 **Findings Tracker** - Centralized database for documenting vulnerabilities with severity and evidence.
- 🔍 **Automated Scans** - One-click integration with `nmap`, `nikto`, `gobuster`, and `nuclei`.
- 🧠 **AI Assistant** - Intelligent guidance powered by **Google Gemini** for output analysis and strategy.
- 📊 **Report Generation** - Export professional Executive and Technical reports in Markdown and JSON formats.

## 📋 Prerequisites

- **Python 3.9+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **Google Gemini API Key** - For AI features (optional, mock responses available)

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
cd HackMate-v2.0.1
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the backend
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local

# Run the frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
HackMate-v2.0.1/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # SQLAlchemy setup
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── engagement.py    # Engagement model
│   │   ├── phase.py         # PTES Phase model
│   │   ├── finding.py       # Finding model
│   │   ├── scan.py          # Scan model
│   │   ├── terminal.py      # Terminal history model
│   │   ├── chat.py          # Chat message model
│   │   └── report.py        # Report model
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   │   ├── engagements.py   # Engagement CRUD
│   │   ├── methodology.py   # PTES phases
│   │   ├── terminal.py      # Command execution
│   │   ├── findings.py      # Vulnerability tracking
│   │   ├── scans.py         # Automated scans
│   │   ├── reports.py       # Report generation
│   │   └── ai.py            # AI assistant
│   └── services/            # Business logic
│       ├── ai_service.py    # Gemini integration
│       ├── terminal_service.py
│       └── report_service.py
│
└── frontend/
    ├── src/
    │   ├── app/             # Next.js app router pages
    │   │   ├── page.tsx     # Dashboard
    │   │   ├── engagements/ # Engagement pages
    │   │   ├── terminal/    # Terminal page
    │   │   ├── findings/    # Findings page
    │   │   └── ai/          # AI assistant page
    │   ├── components/      # React components
    │   │   ├── ui/          # Reusable UI components
    │   │   └── layout/      # Layout components
    │   └── lib/             # Utilities and API client
    └── tailwind.config.ts   # Dark hacker theme
```

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with SQLite database
- **Pydantic** - Data validation
- **Google Generative AI** - Gemini API integration

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS
- **TanStack Query** - Data fetching
- **Lucide Icons** - Icon library

## 📚 Extended Documentation

For more detailed information, check out the following guides:

- **[Architecture Overview](docs/architecture.md)** - Deep dive into system design and tech stack.
- **[Usage Guide](docs/usage.md)** - Step-by-step manual for typical penetration testing workflows.
- **[Features List](docs/features.md)** - Detailed breakdown of platform capabilities.
- **[API Guide](docs/api_guide.md)** - Documentation for REST endpoints and data schemas.

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/engagements` | List all engagements |
| POST | `/api/engagements` | Create engagement |
| GET | `/api/engagements/{id}` | Get engagement details |
| GET | `/api/methodology/phases/{engagement_id}` | Get PTES phases |
| POST | `/api/terminal/execute/{engagement_id}` | Execute command |
| GET | `/api/findings/engagement/{engagement_id}` | List findings |
| POST | `/api/scans/{engagement_id}` | Start scan |
| POST | `/api/ai/chat/{engagement_id}` | Chat with AI |
| POST | `/api/reports/{engagement_id}` | Generate report |

## 🔒 Security Features

- Command whitelisting in terminal
- Input sanitization
- Scope limitation enforcement
- No RCE vulnerabilities by design

## 📄 License

MIT License - See LICENSE file for details.

---

**⚠️ DISCLAIMER:** This tool is intended for authorized security testing only. Always obtain proper authorization before testing any systems.
