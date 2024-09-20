FROM python:3.12-slim

# Definir variáveis de ambiente para o Poetry e Django
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    DJANGO_SETTINGS_MODULE=bookstore.settings

# Adicionar o ambiente virtual do Poetry ao PATH
ENV PATH="/exercicioEBAC_djangoPoetry/.venv/bin:$PATH"

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /exercicioEBAC_djangoPoetry

# Copiar os arquivos de dependências do Poetry
COPY pyproject.toml poetry.lock /exercicioEBAC_djangoPoetry/

# Instalar as dependências do Poetry
RUN poetry install

# Verificar a instalação do Django
RUN poetry show django

# Copiar o restante do código para o contêiner
COPY . .

# Coletar os arquivos estáticos
RUN poetry run python manage.py collectstatic --noinput

# Expor a porta que o Django vai rodar
EXPOSE 8000

# Adicionar o PYTHONPATH
ENV PYTHONPATH="/exercicioEBAC_djangoPoetry:/exercicioEBAC_djangoPoetry/.venv/lib/python3.12/site-packages"

# Comando para rodar as migrações e iniciar o servidor, ativando o ambiente virtual
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run gunicorn bookstore.wsgi:application --bind 0.0.0.0:8000"]
