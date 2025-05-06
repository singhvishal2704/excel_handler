# 📊 Excel Operations Web App (Backend)

A scalable Django-based backend system for uploading, processing, and exporting Excel files with support for versioning, undo, and AI-driven operations.

---

## 🚀 Features

- Upload and parse Excel files
- Perform operations like:
  - Add columns using GPT-generated expressions
  - Filter rows via natural language
  - Combine columns
- Version tracking and undo support
- Export as Excel blob
- LRU caching using Redis
- Local/S3 file support via environment toggle
- Soft delete support

---

## 🧰 Tech Stack

- Django 4+
- PostgreSQL
- Redis
- Pandas
- Groq API (via `gpt_utils.py`)
- DRF (Django Rest Framework)

---

## 🛠️ Setup Instructions

### 1. Clone the repo
```bash
git clone <repo-url>
cd backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file at the root with:
```env
DB_NAME=excel_db
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=yourpassword

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
AWS_S3_CUSTOM_DOMAIN=

REDIS_CACHE_URL=redis://127.0.0.1:6379/1

DEBUG=True
ENV=dev
GROQ_API_KEY=
GROQ_MODEL=llama3-8b-8192
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start development server
```bash
python manage.py runserver
```

---

## ✅ Running Tests

To run all test cases:
```bash
python manage.py test
```

Or to test specific module:
```bash
python manage.py test excel_handler.tests.test_export
```

---

## 📂 Folder Highlights

- `excel_handler/api/v1/views/` – APIView-based class views
- `services/` – Handles business logic like versioning, file handling, GPT operations
- `common/` – Shared utilities: logging, Redis, S3, GPT wrapper
- `tests/` – Modular test files for all APIs

---

## 📄 License
MIT (Add your license file if applicable)

---

For frontend integration or deployment setup (Docker, Gunicorn, etc.), raise a request! 🚀
