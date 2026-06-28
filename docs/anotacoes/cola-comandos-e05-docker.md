# Cola de comandos — Vídeos e05 (Docker) · só comandos (PowerShell)

> Use `curl.exe` (não `curl`). Encadeie com `;` (não `&&`). Modelo: monte a **pasta**.

## Setup (uma vez)
```powershell
cd "$HOME\Documents\GitHub\cdia-m7-PUCSP"
docker info | Select-Object -First 3
docker rm -f bella-test 2>$null ; docker rmi bella-tavola:v1 2>$null   # reset p/ vídeo 1
```

## 🎬 Vídeo 1 — Dockerfile + build + run
```powershell
docker build -t bella-tavola:v1 ./api          # mostrar layers
docker images bella-tavola:v1                  # ~776 MB
docker run -d -p 8000:8000 --name bella-test bella-tavola:v1

curl.exe http://localhost:8000/                # {"mensagem":"Bem-vindo ao Bella Tavola!"}
curl.exe -L http://localhost:8000/pratos/      # lista de 6 pratos

# cache: edite a msg da rota / em api/main.py, salve, e rebuilde:
docker build -t bella-tavola:v1 ./api          # pip install = CACHED

docker stop bella-test ; docker rm bella-test
```

## 🎬 Vídeo 2 — Compose + boas práticas
```powershell
# Compose: API + PostgreSQL + Nginx
docker compose up -d
docker compose ps                              # db = healthy; api depois
curl.exe http://localhost/                     # via Nginx, porta 80
curl.exe -L http://localhost/pratos/
docker compose down                            # preserva volumes
docker volume ls                               # bella-* continuam

# Segurança
docker run --rm bella-tavola:v1 find /app -name ".env"   # (vazio = .env fora da imagem)
docker run --rm bella-tavola:v1 whoami                   # appuser (não-root)

# /ml/predict (modelo montado, sem token) — cada comando em UMA linha; cole inteiro
docker run -d -p 8000:8000 --name bella-test -e MODEL_PATH=/models/credit_rf.pkl -v "${PWD}\datagen\models:/models:ro" bella-tavola:v1 #ate aqui
Start-Sleep -Seconds 4
curl.exe -s http://localhost:8000/health                 # {"api":"ok","model":"loaded"}
curl.exe -s -X POST http://localhost:8000/ml/predict -H "Content-Type: application/json" -d '{\"renda_mensal\":3000,\"divida_atual\":1500,\"historico_pagamentos\":40,\"idade\":30,\"num_dependentes\":3}'
# {"prediction":1,"probability":0.65,"label":"inadimplente",...}
docker stop bella-test ; docker rm bella-test
```

## 🎬 Vídeo 3 — CI + Docker Hub
```powershell
gh run list --branch main --limit 1            # último run: 4 jobs, success
gh secret list                                 # DOCKER_USERNAME, DOCKER_PASSWORD, HF_TOKEN

# RESET p/ "outra máquina": apaga a cópia LOCAL antes, senão o pull diz "up to date"
docker rm -f bella-ci 2>$null ; docker rmi zaras210/bella-tavola:latest 2>$null

# "outra máquina": puxa a imagem publicada pelo CI e roda (agora baixa de verdade)
docker pull zaras210/bella-tavola:latest
docker run -d -p 8000:8000 --name bella-ci -e MODEL_PATH=/models/credit_rf.pkl -v "${PWD}\datagen\models:/models:ro" zaras210/bella-tavola:latest
Start-Sleep -Seconds 4
curl.exe -s http://localhost:8000/ ; curl.exe -s http://localhost:8000/health
docker stop bella-ci ; docker rm bella-ci
```
**Abrir na tela:** Actions → `github.com/Czar210/cdia-m7-PUCSP/actions` · Imagem → `hub.docker.com/r/zaras210/bella-tavola/tags`
