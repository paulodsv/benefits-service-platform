FROM python:3.11-slim

WORKDIR /app

# copia todo o projeto para que os diretórios de pacotes `app/` e `worker/` estejam disponíveis
COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

# roda o consumidor de mensagens
CMD ["python", "-m", "worker.consumer"]
