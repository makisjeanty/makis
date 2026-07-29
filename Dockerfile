# Imagem base oficial do Python 3.13
FROM python:3.13-slim

# Evitar gravação de arquivos .pyc e garantir output direto no stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências de sistema necessárias para compilação/conexão (ex: gcc, pkg-config, mariadb/mysql dev libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte da aplicação
COPY . /app/

# Expor a porta 8000 para a aplicação ASGI (Daphne)
EXPOSE 8000

# Executar a aplicação via Daphne (servidor ASGI)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
