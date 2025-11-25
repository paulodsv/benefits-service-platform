FROM python:3.11-slim

WORKDIR /app

# copia todo o projeto para que os diretórios de pacotes `app/` estejam disponíveis
COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

# roda o servidor Uvicorn para a aplicação FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
