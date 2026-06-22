# Dockerfile da API Bella Tavola
# Versão final da série e05 (Docker): multi-stage build + usuário não-root.
#
# O contexto de build é a pasta api/ — é aqui que vivem main.py, requirements.txt,
# routers/, models/ e model_utils.py. O conteúdo desta pasta vira /app na imagem,
# de modo que `uvicorn main:app` e os imports `from routers import ...` /
# `from model_utils import ...` resolvem sem PYTHONPATH extra.
#
# O projeto usa Python 3.12 (mesma versão do CI). Os gabaritos dos cadernos usam
# 3.11 como exemplo — aqui adaptamos para a versão real do projeto.

# ── Estágio 1: builder ──────────────────────────────────────────────────────
# Tem o necessário para INSTALAR as dependências (inclui ferramentas de compilação
# que numpy/scikit-learn usam). Nada disso precisa sobreviver no runtime.
FROM python:3.12-slim AS builder

WORKDIR /app

# Copia apenas o requirements.txt primeiro: a camada de dependências só é
# refeita quando o requirements.txt muda, não a cada alteração de código.
COPY requirements.txt .

# Instala em /install (prefixo isolado) para copiar facilmente no estágio final.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Estágio 2: final ────────────────────────────────────────────────────────
# Imagem limpa, sem compiladores nem cache de build.
FROM python:3.12-slim

WORKDIR /app

# Diretório de cache do Hugging Face dentro de /app, gravável pelo usuário não-root.
# Sem isso, o download do modelo em runtime tentaria escrever em ~/.cache e falharia.
ENV HF_HOME=/app/.cache/huggingface \
    PYTHONUNBUFFERED=1

# Copia apenas os pacotes instalados do estágio builder.
COPY --from=builder /install /usr/local

# Copia o código da aplicação (depois das dependências, para preservar o cache).
COPY . .

# Usuário sem privilégios (princípio do menor privilégio).
# Criado após o pip install: a instalação de pacotes exige permissão de root.
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    mkdir -p /app/data /app/.cache/huggingface && \
    chown -R appuser:appgroup /app

USER appuser

# Documenta a porta usada pela API (o mapeamento real é feito com -p no run).
EXPOSE 8000

# Forma de lista JSON (sem shell intermediário).
# --host 0.0.0.0: escuta em todas as interfaces, necessário para o -p funcionar.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
