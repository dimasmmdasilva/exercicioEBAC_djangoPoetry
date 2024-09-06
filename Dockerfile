FROM python:3.12-slim

# Definir variáveis de ambiente para o Poetry e Django
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    DJANGO_SETTINGS_MODULE=bookstore.bookstore.settings

ENV PYTHONPATH="/exercicioEBAC_djangoPoetry:/exercicioEBAC_djangoPoetry/.venv/lib/python3.12/site-packages"

# Log: Início da instalação das dependências do sistema
RUN echo "Instalando dependências do sistema..." && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && pip install "poetry==${POETRY_VERSION}" \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* && \
    echo "Dependências do sistema instaladas com sucesso!"

# Definir o diretório de trabalho
WORKDIR /exercicioEBAC_djangoPoetry

# Copiar os arquivos de dependências do Poetry
COPY pyproject.toml poetry.lock /exercicioEBAC_djangoPoetry/

# Log: Instalação das dependências do projeto via Poetry
RUN echo "Instalando dependências do projeto com o Poetry..." && \
    poetry install --no-root && \
    poetry show django && \
    echo "Dependências do Django instaladas com sucesso!"

# Copiar o restante do código para o contêiner
COPY . .

# Ajustar permissões no projeto
RUN echo "Ajustando permissões do projeto..." && \
    chmod -R 755 /exercicioEBAC_djangoPoetry && \
    echo "Permissões ajustadas com sucesso!"

# Expor a porta que o Django vai rodar
EXPOSE 8000

# Comando para rodar as migrações e iniciar o servidor, ativando o ambiente virtual
CMD ["sh", "-c", "poetry run python bookstore/bookstore/manage.py migrate && poetry run python bookstore/bookstore/manage.py runserver 0.0.0.0:8000"]
