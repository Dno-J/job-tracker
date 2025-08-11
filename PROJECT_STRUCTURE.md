## 🏗️ Project Structure

```plaintext
job-tracker/
├── app/
│   ├── auth/                 # JWT logic, password hashing, auth dependencies
│   ├── middleware/           # FastAPI middleware for route protection
│   ├── models/               # SQLModel ORM models (Job, User)
│   ├── routers/              # FastAPI route handlers (auth, jobs, dashboard, API)
│   ├── schemas/              # Pydantic schemas for request/response
│   ├── static/               # Charts, exports, screenshots
│   │   ├── charts/           # Rendered chart images
│   │   └── exports/          # Generated PDFs (git-kept via .keep)
│   ├── templates/            # Jinja2 HTML templates (dashboard, auth, jobs)
│   ├── tests/                # Pytest suite (CRUD, security, exports)
│   ├── utils/                # CSV/PDF generation, charts, template helpers
│   ├── database.py           # DB engine + session config
│   └── __init__.py
├── static/                   # Frontend static files (served by FastAPI)
├── .idea/                    # IDE settings
├── .pytest_cache/            # Pytest cache
├── .venv/                    # Local virtual environment
├── .env                      # Local env variables (not committed)
├── .env.example              # Safe template for shared usage
├── .env.ec2.template         # Safe template for EC2 deployment
├── aws_setup.sh              # EC2 provisioning and setup script
├── .gitignore                # Files and dirs to ignore in Git
├── config.py                 # Environment and config handling
├── Dockerfile                # Production Docker image config
├── jobtracker.db             # Dev SQLite database
├── main.py                   # FastAPI entrypoint
├── pytest.ini                # Pytest config
├── render.yaml               # Deployment settings for Render
├── requirements.txt          # Python dependencies
└── test.db                   # Isolated test SQLite database
