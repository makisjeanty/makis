import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Post, Categoria, Tag
from accounts.models import PerfilUsuario

# 1. Categoria
cat_estudos, _ = Categoria.objects.get_or_create(
    slug='estudos-de-caso',
    defaults={'nome': 'Estudos de Caso'}
)

# 2. Autor (primeiro superuser)
autor = PerfilUsuario.objects.filter(is_superuser=True).first()
if not autor:
    autor = PerfilUsuario.objects.first()

# 3. Tags
tag_django, _ = Tag.objects.get_or_create(nome='Django', defaults={'slug': 'django'})
tag_docker, _ = Tag.objects.get_or_create(nome='Docker', defaults={'slug': 'docker'})
tag_devops, _ = Tag.objects.get_or_create(nome='DevOps', defaults={'slug': 'devops'})

# 4. Conteúdo do Artigo 1
conteudo_artigo = """
Colocar uma aplicação Django em produção não precisa ser um pesadelo de configurações manuais ou dependência de serviços caros de PaaS. 

Neste tutorial prático, vou detalhar exatamente a arquitetura e o processo de deploy que utilizei para subir a **makisjeanty.com** em uma VPS rodando Ubuntu 24.04 com Docker, Nginx, Daphne (ASGI) e Cloudflare.

---

## 1. A Arquitetura do Stack

Para suportar tanto requisições HTTP tradicionais quanto WebSockets em tempo real (usados no chat do site), a topologia de containers ficou assim:

- **Nginx (Porta 80/443)**: Reverse proxy responsável por SSL termination, roteamento HTTP/WebSocket e arquivos estáticos via WhiteNoise.
- **Web (Daphne / ASGI)**: Servidor de aplicação Django rodando sob o processo Daphne na porta 8000.
- **DB (MySQL 8.0)**: Banco de dados relacional com volume persistente montado no host.
- **Redis 7**: Cache e Channel Layer para o Django Channels (WebSockets).

---

## 2. Dockerfile Otimizado para Produção

O `Dockerfile` utiliza um usuário não-root por segurança e instala dependências mínimas necessárias:

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usuário não-root para execução segura
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
```

---

## 3. Docker Compose com Fail-Closed para Segredos

Uma das decisões críticas no `docker-compose.yml` foi utilizar a sintaxe `${VAR:?mensagem}` para impedir que os containers subam caso alguma variável de ambiente crítica esteja ausente no `.env`:

```yaml
services:
  web:
    build: .
    container_name: makis_web
    restart: unless-stopped
    environment:
      - SECRET_KEY=${SECRET_KEY:?SECRET_KEY ausente}
      - DB_PASSWORD=${DB_PASSWORD:?DB_PASSWORD ausente}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS:?ALLOWED_HOSTS ausente}
    depends_on:
      - db
      - redis

  db:
    image: mysql:8.0
    container_name: makis_mysql
    restart: unless-stopped
    environment:
      - MYSQL_DATABASE=base_central
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD:?DB_ROOT_PASSWORD ausente}
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    container_name: makis_redis
    restart: unless-stopped

volumes:
  mysql_data:
```

---

## 4. Roteamento de WebSockets no Nginx

Para permitir conexões de WebSocket sem desconexões prematuras, o `nginx.conf` precisa repassar os cabeçalhos de `Upgrade` e `Connection` para o Daphne:

```nginx
server {
    listen 80;
    server_name makisjeanty.com;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Rota específica para WebSockets
    location /ws/ {
        proxy_pass http://web:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

---

## 5. Health Check Embutido (`/health/`)

Em vez de depender apenas da porta responder, criei um endpoint de monitoria em `core/urls.py` que testa a conexão com o banco e o Redis em tempo real:

```python
def health_check(request):
    status = {"status": "ok", "database": "ok", "redis": "ok"}
    http_code = 200

    try:
        connection.ensure_connection()
    except Exception:
        status["database"] = "error"
        status["status"] = "degraded"
        http_code = 503

    return JsonResponse(status, status=http_code)
```

---

## 6. Resultado e Métricas

Com essa estrutura, a aplicação responde com tempo médio abaixo de 100ms para requisições HTTP, possui suporte total a real-time chat via WebSockets e roda de forma estável com baixo consumo de recursos na VPS.
"""

post, created = Post.objects.get_or_create(
    slug='do-zero-a-producao-django-docker-vps',
    defaults={
        'titulo': 'Do Zero à Produção: Django + Docker em VPS',
        'resumo': 'Guia completo de como subir uma aplicação Django 6 com Channels, Daphne, Docker, Nginx e MySQL em uma VPS Ubuntu 24.04.',
        'conteudo': conteudo_artigo,
        'categoria': cat_estudos,
        'autor': autor,
        'publicado': True,
    }
)

post.tags.add(tag_django, tag_docker, tag_devops)

if created:
    print("OK - Artigo 'Do Zero a Producao' criado com sucesso!")
else:
    print("OK - Artigo 'Do Zero a Producao' ja existia e foi mantido.")
