# 🚀 Flask API — Dockerized CI/CD Deployment

A production-style Flask API project demonstrating containerized application deployment, CI/CD automation, and cloud-ready DevOps workflows using Docker and GitHub Actions.

This project simulates a modern backend deployment pipeline where application changes are automatically tested, containerized, and prepared for deployment workflows.

---

# 🌐 Project Overview

This repository demonstrates:

* Flask API development
* Docker containerization
* CI/CD automation with GitHub Actions
* Cloud-native deployment practices
* Production-ready backend workflows
* Automated build pipelines

The project is designed to showcase practical DevOps engineering concepts used in modern backend infrastructure environments.

---

# 📐 Architecture Diagram

```text id="pnlc3r"
                ┌─────────────────┐
                │    Developer    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ GitHub Repository│
                └────────┬────────┘
                         │ Push Code
                         ▼
              ┌────────────────────┐
              │ GitHub Actions CI  │
              │ Build Workflow     │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Flask API Testing  │
              │ Validation Stage   │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Docker Build       │
              │ Containerization   │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Docker Image       │
              │ Deployment Ready   │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │ Cloud / EC2 Ready  │
              │ Runtime Environment│
              └────────────────────┘
```

---

# ⚙️ Tech Stack

## Backend

* Python
* Flask

## DevOps

* Docker
* GitHub Actions

## Cloud Concepts

* AWS EC2
* CI/CD Automation
* Containerized Deployment

---

# ✨ Features

* Lightweight Flask REST API
* Dockerized application runtime
* GitHub Actions automation
* Production-ready project structure
* Cloud deployment ready
* CI workflow integration
* Fast local container setup

---

# 📂 Project Structure

```bash id="y7e7v3"
.
├── .github/workflows/
│   └── jekyll-gh-pages.yml
├── 2-flask-api-docker/
├── Dockerfile
├── README.md
```

---

# 🔄 CI/CD Workflow

## Continuous Integration

Every repository update triggers:

1. Source code checkout
2. Workflow validation
3. Container build process
4. Deployment preparation

---

# 🐳 Docker Workflow

The application runs inside a Docker container to ensure:

* Consistent runtime environments
* Easy deployment
* Scalability
* Isolation
* Reproducible builds

Build Docker image:

```bash id="hmgp78"
docker build -t flask-api .
```

Run container:

```bash id="b9x1je"
docker run -p 5000:5000 flask-api
```

---

# 🚀 Local Development

Clone repository:

```bash id="0t7n1p"
git clone https://github.com/fastlanegaurav/flask-api.git
```

Navigate into project:

```bash id="zjlwm0"
cd flask-api
```

Run locally:

```bash id="bz0y8d"
python app.py
```

---

# 📊 Engineering Highlights

| Capability         | Value                              |
| ------------------ | ---------------------------------- |
| Containerization   | Consistent deployment environments |
| CI/CD Automation   | Faster engineering workflow        |
| Flask API          | Lightweight backend architecture   |
| Docker Integration | Production-ready packaging         |
| Cloud Readiness    | AWS deployment compatible          |

---

# 🎯 DevOps Concepts Demonstrated

* Containerization
* CI/CD Pipelines
* Backend Deployment
* Cloud-Native Development
* Docker Workflow
* Infrastructure Automation
* Deployment Readiness

---

# 👨‍💻 Author

Gaurav Kumar Singh

DevOps Engineer | AWS | Docker | Kubernetes | Terraform | CI/CD

* GitHub: https://github.com/fastlanegaurav
* Portfolio: https://gaurav-portfolio-navy.vercel.app/
