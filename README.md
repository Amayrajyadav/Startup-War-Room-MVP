# Startup War Room

Startup War Room is an AI boardroom powered entirely by a locally running Gemma model. Users submit a startup idea, and multiple stakeholders (Investor, CTO, Customer, Competitor, Growth Expert) critique it. Finally, a synthesized report with a 7-day action plan is provided.

## Tech Stack
- **Frontend**: React, Vite, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python
- **AI**: LM Studio (OpenAI-compatible API), Gemma 4 (local)

## Folder Structure
- `/frontend` - React SPA
- `/backend` - FastAPI application

## Setup Instructions

### Prerequisites
1. Node.js (v18+)
2. Python (3.9+)
3. [LM Studio](https://lmstudio.ai/) with Gemma 4 model loaded. Start the local server in LM Studio.

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment variables example:
   ```bash
   cp .env.example .env
   ```
5. Start the development server:
   ```bash
   python main.py
   # Or using uvicorn directly:
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Copy the environment variables example:
   ```bash
   cp .env.example .env
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

The application will be accessible at `http://localhost:5173`.

## Why Local Gemma?

Startup War Room runs entirely on a locally hosted Gemma model through LM Studio.

Benefits:

- No cloud dependency
- Lower inference cost
- Privacy-preserving analysis
- Offline operation
- Demonstrates practical deployment of Gemma in real-world decision support systems

User Idea
    │
    ▼
+------------------+
| Investor Agent   |
+------------------+

+------------------+
| CTO Agent        |
+------------------+

+------------------+
| Customer Agent   |
+------------------+

+------------------+
| Competitor Agent |
+------------------+

+------------------+
| Growth Agent     |
+------------------+
          │
          ▼
+------------------+
| Final Board      |
+------------------+
          │
          ▼
Board Decision
