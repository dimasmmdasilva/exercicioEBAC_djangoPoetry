FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1

# Instalar dependências do sistema e o Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho (ajuste)
WORKDIR /app/bookstore

# Copiar os arquivos de dependências do Poetry
COPY pyproject.toml poetry.lock /app/

# Instalar as dependências do projeto
RUN poetry install --no-root --no-dev

# Copiar todo o código do projeto para o diretório de trabalho no contêiner
COPY . /app/

# Expôr a porta que o Django vai rodar
EXPOSE 8000

# Comando para rodar as migrações e iniciar o servidor Gunicorn
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]
