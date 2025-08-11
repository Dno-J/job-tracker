# 💼 Job Tracker — FastAPI App for Managing Job Applications

A FastAPI-powered job tracking platform with JWT authentication, CSV/PDF exports, analytics dashboard, and full Docker support deployable on Render and AWS EC2.

<!-- 🌐 Live Apps -->
[![Live App — Render](https://img.shields.io/badge/Live%20App-00C7B7?logo=render&logoColor=white&style=flat-square)](https://job-tracker-59j1.onrender.com)
[![Live App — AWS EC2](https://img.shields.io/badge/Live%20App%20EC2-FF9900?logo=amazonaws&logoColor=white&style=flat-square)](http://16.171.148.202:8000)

<!-- 🛠️ Tech Badges -->
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat-square)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=flat-square)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat-square)](https://www.docker.com/)
[![Postgres](https://img.shields.io/badge/Postgres-4169E1?logo=postgresql&logoColor=white&style=flat-square)](https://www.postgresql.org/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0F9D58?logo=python&logoColor=white&style=flat-square)](https://sqlmodel.tiangolo.com/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white&style=flat-square)](https://docs.pytest.org/)

<!-- 📜 Meta Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Dno-J/job-tracker?style=flat-square)](https://github.com/Dno-J/job-tracker/commits/main)

---


## 🚀 Features

- 📂 **Job Application Management** — Add, edit, delete, and filter applications with status tracking.  
- 🔐 **Secure Authentication** — JWT (HTTP-only cookies), password hashing, and middleware guards.  
- 📊 **Interactive Dashboard** — Charts, quick stats, and trends for fast insights.  
- 📤 **Data Export** — Export applications to CSV or printable PDF (with charts).  
- 🐳 **Dockerized** — Consistent local and cloud environments via Docker.  
- ☁️ **Multi-cloud Deployment** — Deploy on **Render** and **AWS EC2**.  
- 🛡️ **Environment Management** — Safe `.env` templates for local and cloud setups.  
- 🧪 **Testing** — Comprehensive Pytest suite covering CRUD, authentication/security, and export validation. 

---

## 📦 Local Setup

```bash
# Clone the repository
git clone https://github.com/Dno-J/job-tracker.git
cd job-tracker

# Create and populate env file
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
````

---


## ☁️ Deployment

This app is **fully Dockerized** and runs identically on **Render** and **AWS EC2** for maximum flexibility.  
Containerization ensures smooth, repeatable deployments on any host.

---

### 📦 Quick Deployment Flow

```mermaid
flowchart LR
    A[Code Push to GitHub] --> B[Docker Build]
    B --> C[Deploy to Render]
    B --> D[Deploy to AWS EC2]
    C --> E[Live App (Render)]
    D --> F[Live App (EC2)]
```

---

### 🔷 Render

* Deployment configured with `render.yaml` file
* Environment variables managed via Render dashboard or in `render.yaml`
* Database: **Neon Postgres** (or SQLite for local development)
* Automatic builds & deploys triggered on every push to `main` branch

**Live App:** [job-tracker-59j1.onrender.com](https://job-tracker-59j1.onrender.com)

**Setup Commands:**

```bash
# 1. Push your latest code to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Log in to https://render.com and connect your GitHub repo

# 3. Create a new Web Service on Render:
#    - Select your repo and 'main' branch
#    - Use 'Docker' or 'Python' environment (your render.yaml uses python env)
#    - Set environment variables in Render dashboard OR rely on those in render.yaml
#    - Render will auto-build and deploy your app on push

# 4. Monitor build and deployment logs in Render dashboard

# 5. Access your live app via the provided Render URL
```

---

### 🟠 AWS EC2

* Manual Dockerized deployment on your own **AWS EC2** instance
* Environment variables configured via `.env.ec2.template`

**Setup Commands:**

```bash
# SSH into your EC2 instance
ssh ubuntu@<your-ec2-ip>

# Clone your repo
git clone https://github.com/Dno-J/job-tracker.git
cd job-tracker

# Copy and edit env file for production settings
cp .env.ec2.template .env

# Build the Docker image
docker build -t job-tracker-app .

# Run the container, forwarding port 8000 and passing env vars
docker run -d -p 8000:8000 --env-file .env job-tracker-app
```

**Live App:** [http://16.171.148.202:8000](http://16.171.148.202:8000)

---


## 🧪 Running Tests

To run the automated test suite, make sure you have all dependencies installed, then execute:

```bash
pytest
````

The Pytest suite covers:

* CRUD operations (create, read, update, delete)
* Security checks (authentication, authorization)
* Data export verification (CSV, PDF generation)

Tests run against an isolated SQLite database for consistency and speed.

---

## 🛠️ Tech Stack

| Category         | Tools & Frameworks                                       | Purpose                                                |
|------------------|---------------------------------------------------------|--------------------------------------------------------|
| **Backend**      | FastAPI, SQLModel, Pydantic                              | API endpoints, ORM for DB models, request/response validation |
| **Auth/Security**| JWT (HTTP-only cookies), Password hashing, Middleware guards | Secure login, session handling, route protection         |
| **Testing**      | Pytest, Fixtures, Isolated SQLite DB                     | Automated CRUD, security, and export tests with reproducible results |
| **Deployment**   | Docker, Render, AWS EC2, Neon Postgres                   | Cloud hosting, database hosting, containerized builds    |
| **Utilities**    | Jinja2, Matplotlib, WeasyPrint, CSV/PDF export scripts   | Server-side rendering, data visualization, export generation |

---


## 🏗️ Project Structure

For the complete folder and file layout, including descriptions of each component, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

---

## 🖼️ App preview (screenshots)

Below are some key screens of the Job Tracker app in action.  
All images live in `app/static/assets/screenshots/`

### 📋 Dashboard
![Dashboard](app/static/assets/screenshots/dashboard.png)
- The main view of your job applications with quick-glance stats and filters.

### ➕ Add job
![Add Job Form](app/static/assets/screenshots/add_job_form.png)
- Add a new job entry with title, company, status, and notes; validation ensures clean data.

### ✏️ Edit job
![Edit Job Form](app/static/assets/screenshots/edit_job_form.png)
- Update an existing application; preserve history and keep details current.

### 🔍 Filtered results
![Filtered Jobs](app/static/assets/screenshots/filtered_jobs.png)
- Apply search and status filters to narrow results quickly.

### 📤 Export to PDF
![Export PDF](app/static/assets/screenshots/export_pdf.png)
- Generate a printable PDF report of your applications.

---

## 📬 Contact 

If you’d like to discuss the project or potential opportunities, you can reach me here:

[![LinkedIn](https://img.shields.io/badge/Dino%20Jackson-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/dino-jackson-486840368)
[![GitHub](https://img.shields.io/badge/Dno--J-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Dno-J)
[![Email](https://img.shields.io/badge/jacksodino00%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:jacksodino00@gmail.com)

---

## 🤝 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Dino Jackson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY.
```
<p align="center">
  Built with ❤️ by <strong>Dino Jackson</strong>
</p>

