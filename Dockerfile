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

# Criar usuário não privilegiado com UID/GID fixos (evita depender de IDs
# atribuídos automaticamente pela imagem, o que ajuda quando volumes são
# montados entre host e container)
RUN addgroup --system --gid 10001 appgroup \
    && adduser --system --uid 10001 --ingroup appgroup --no-create-home appuser

# Copiar código-fonte da aplicação e ajustar permissões
COPY --chown=appuser:appgroup . /app/

# Diretórios graváveis em runtime (staticfiles/media são volumes Docker em
# docker-compose.yml; media/staticfiles/.dockerignore garante que não vêm no
# COPY acima, então appuser precisa de permissão para criá-los do zero)
RUN mkdir -p /app/staticfiles /app/media /app/logs \
    && chown -R appuser:appgroup /app/staticfiles /app/media /app/logs

COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Container inicia como root de propósito: o entrypoint corrige a
# propriedade dos volumes montados em runtime (o chown acima só cobre a
# imagem, não sobrevive a um volume nomeado já existente ou montado depois)
# e derruba o privilégio via setpriv antes de executar qualquer código da
# aplicação — não é o container rodando como root, é uma inicialização
# root->appuser, como as imagens oficiais do Postgres/MySQL fazem.

# Expor a porta 8000 para a aplicação ASGI (Daphne)
EXPOSE 8000

# Checagem de saúde do container chamando a rota /health/. SecurityMiddleware
# valida o Host header contra ALLOWED_HOSTS em toda requisição (é onde o
# redirect HTTPS decide o host, antes até da URL ser resolvida) — em produção
# ALLOWED_HOSTS só tem o domínio real, então um curl puro em "localhost"
# sempre voltaria 400 DisallowedHost. Manda o primeiro host de ALLOWED_HOSTS
# (env var já injetada pelo docker-compose.yml) como Host header em vez de
# afrouxar ALLOWED_HOSTS só pra isso.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f -H "Host: ${ALLOWED_HOSTS%%,*}" http://localhost:8000/health/ || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Executar a aplicação via Daphne (servidor ASGI)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
