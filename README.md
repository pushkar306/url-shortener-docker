# Containerized URL Shortner Platform

A high-performance URL Shortner service built with **FastAPI** and **Postgresql**

## 🚀 Features

- **FastAPI Backend :** Asynchronous API for high-speed shortening and redirection
- **Postgresql Storage :** Relational database to store URL mapping
- **Data Persistence :** Uses Docker Volumes to ensure Data isn't lost when containers stop
- **Container Orchestration :** one-command deployment via Docker Compose
- **Auto Documentation :** Interactive API docs via Swagger UI

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| Framework | FastAPI |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy |
| Infrastructure | Docker, Docker Compose |

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Installation
1. Clone the repository
```bash
git clone https://github.com/pushkar306/url-shortener-docker.git
cd url-shortner-docker
```
2. Spin up the containers
```bash
docker compose up -d --build
```
3. API Available at : `http://localhost:8000`

4. Swagger UI at : `http://localhost:8000/docs`

## ♨️ Testing the API 

**Shorten a url :**
```bash
$ curl -X POST http://localhost:8000/shorten/
    -H "Content-Type: application/json"
    -d "{\"url\": \"https://www.google.com"}"
```

## 🗄️ Volume Persistence

This project uses a named volume `pgdata` , even after running `docker compose down` your shortened URLs remain safe at pgdata

## 🏛️ System Architecture

API and Database run on isolated *Docker Bridge Network*. Only FastAPI service exposes a port to host. PostgreSQL is unreachable from public internet , can communicate with only the API container permitted to communicate with it.