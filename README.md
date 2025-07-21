# API_Development_task
# 📄 README – FastAPI KPA Form Data Project

## 🚀 Overview
A FastAPI backend project for managing Bogie Checksheet and Wheel Specifications forms, meeting provided Postman specs.

## ✅ Features
- Functional APIs with correct request/response structures
- PostgreSQL/SQLite database support via `.env`
- Dockerized backend (Dockerfile included)
- Pydantic-based input validation
- Auto-generated Swagger/OpenAPI docs (`/docs`)
- Updated Postman collection with working examples

## 🛠 Tech Stack
- FastAPI (Python)
- SQLAlchemy (ORM)
- PostgreSQL / SQLite
- Pydantic
- Docker
- Postman

## ⚙ Setup Instructions
1. Clone/download project zip
2. Create `.env` file:
   ```env
   DATABASE_URL=sqlite:///./kpa_db.sqlite3
   ```
   *(Change to PostgreSQL if needed)*
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run app:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Open docs at: `http://127.0.0.1:8000/docs`

## 🐳 Docker (Optional)
```bash
docker build -t kpa-fastapi .
docker run -d -p 8000:8000 kpa-fastapi
```

## 🧪 Implemented APIs
- `POST /api/forms/bogie-checksheet`: Save bogie checksheet
- `POST /api/forms/wheel-specifications`: Save wheel specs
- `GET /api/forms/wheel-specifications`: Filter/query wheel specs

## 📋 Limitations & Assumptions
- Uses SQLite by default; replace with PostgreSQL for production
- Basic validation; no advanced authentication or permissions

## 🎥 Screen Recording
Record a 2–5 minute video:
- Project features & stack
- Setup instructions
- Running & using Postman
Rename: `yourname_flutter_assignment.mp4`
Upload to Google Drive and share:
- `project-features: <link>`
- `project-technical: <link>`

## 📬 Submission
Email to `contact@suvidhaen.com`:
- Source Code zip: `[https://drive.com/yourname_api_assignment.zip]`
- Postman Collection: `[https://drive.com/yourname_postman_collection.json]`
- README: `[https://drive.com/yourname_readme.txt]`
- Screen Recording: `<link>`

✅ Done: Functional correctness, Docker, validation, environment config, clear documentation.
