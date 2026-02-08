# API Documentation

HackMate v2.0 provides a RESTful API powered by FastAPI. You can access the interactive Swagger documentation at `http://localhost:8000/docs` when the backend is running.

## 🛡️ Authentication & Authorization
Currently, the scaffold uses a single-user model. Future versions will implement JWT-based authentication.

## 📡 Core Endpoints

### 1. Engagements
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/engagements` | GET | List all security engagements. |
| `/api/engagements` | POST | Create a new engagement. |
| `/api/engagements/{id}` | GET | Retrieve detailed engagement info. |
| `/api/engagements/{id}` | DELETE | Remove an engagement and its data. |
| `/api/engagements/stats` | GET | Global stats (findings, active status). |

### 2. PTES Methodology
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/methodology/phases/{id}` | GET | Get phases for an engagement. |
| `/api/methodology/phases/{pid}/toggle` | POST | Toggle a phase status (Done/In Progress). |

### 3. Security Tools & Terminal
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/terminal/execute/{id}` | POST | Run a whitelisted command. |
| `/api/terminal/history/{id}` | GET | Retrieve command history for engagement. |
| `/api/scans/{id}` | POST | Trigger an automated tool scan. |

### 4. Findings & Reporting
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/findings` | POST | Log a new vulnerability finding. |
| `/api/findings/engagement/{id}` | GET | List findings for an engagement. |
| `/api/reports/generate` | POST | Generate a new AI report. |
| `/api/reports` | GET | List all generated reports. |

## 🛠️ Data Schemas

### Engagement Object
```json
{
  "id": "uuid",
  "name": "Project Name",
  "target": "target.com",
  "scope": "IP range / domain",
  "status": "active/completed",
  "created_at": "ISO-date"
}
```

### Finding Object
```json
{
  "title": "SQL Injection",
  "severity": "critical",
  "description": "...",
  "remediation": "...",
  "evidence": "..."
}
```
