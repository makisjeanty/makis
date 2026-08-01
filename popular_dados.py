import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portfolio.models import Projeto
from blog.models import Post, Categoria, Tag
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.first()

print(f"--> Usando usuário autor: {admin_user.username if admin_user else 'None'}")

# -----------------------------------------------------------------------------
# 1. Cadastrar Projetos no Portfólio
# -----------------------------------------------------------------------------
projetos_data = [
    {
        'titulo': 'Makis Hub & OS',
        'slug': 'makis-hub-os',
        'categoria': 'web',
        'tipo': 'pessoal',
        'descricao_curta': 'Plataforma de utilidades dev client-side, central de IA e ecossistema de produtividade construído com Django 6 e Docker.',
        'descricao_completa': 'O Makis Hub é um centro integrado de ferramentas para engenheiros de software, arquitetos e fundadores. Inclui 18 utilitários desacoplados (calculadora de tokens de LLM, analisador SEO, auditores de segurança OWASP, formatadores JSON, geradores de hash) e integração com agentes autônomos de IA.',
        'tecnologias': 'Python,Django 6.0,Docker,MySQL,Redis,TailwindCSS,JavaScript',
        'link_demo': 'https://makisjeanty.com/utilidades/',
        'link_github': 'https://github.com/makisjeanty/makis',
        'destaque': True,
        'publico': True,
    },
    {
        'titulo': 'Arquitetura SaaS Resiliente Multi-Tenant',
        'slug': 'arquitetura-saas-resiliente',
        'categoria': 'web',
        'tipo': 'pessoal',
        'descricao_curta': 'Arquitetura em nuvem desacoplada para aplicações SaaS de alto tráfego com isolamento de dados e cache distribuído em Redis.',
        'descricao_completa': 'Projeto de referência para plataformas SaaS. Implementa isolamento de esquema de banco de dados, autenticação JWT/OAuth2, gerenciamento de sessões distribuídas via Redis e proxy reverso resiliente via Nginx + Cloudflare em modo Full strict.',
        'tecnologias': 'Python,Django,Docker Compose,PostgreSQL,Redis,Cloudflare',
        'link_demo': 'https://makisjeanty.com/portfolio/',
        'link_github': 'https://github.com/makisjeanty/makis',
        'destaque': True,
        'publico': True,
    },
    {
        'titulo': 'Agentes Autônomos & Automação com LLMs',
        'slug': 'agentes-autonomos-llm',
        'categoria': 'automacao',
        'tipo': 'pessoal',
        'descricao_curta': 'Sistema de orquestração de agentes de IA para análise de requisitos, geração automática de documentação e revisão de código.',
        'descricao_completa': 'Ecossistema de agentes IA autônomos utilizando a API da OpenAI/Anthropic/Gemini para parsing de código, geração de ADRs (Architecture Decision Records) e automação de pipelines de validação técnica.',
        'tecnologias': 'Python,LangChain,OpenAI API,Gemini API,Redis,Celery',
        'link_demo': 'https://makisjeanty.com/utilidades/agente-orientador/',
        'link_github': 'https://github.com/makisjeanty/makis',
        'destaque': True,
        'publico': True,
    }
]

for item in projetos_data:
    proj, created = Projeto.objects.update_or_create(
        slug=item['slug'],
        defaults=item
    )
    status_str = "Criado" if created else "Atualizado"
    print(f"✅ Projeto: {proj.titulo} ({status_str})")

# -----------------------------------------------------------------------------
# 2. Criar Categoria e Tags do Blog
# -----------------------------------------------------------------------------
cat_estudos, _ = Categoria.objects.get_or_create(
    nome='Estudos de Caso',
    defaults={'slug': 'estudos-de-caso'}
)

tag_django, _ = Tag.objects.get_or_create(nome='Django', defaults={'slug': 'django'})
tag_docker, _ = Tag.objects.get_or_create(nome='Docker', defaults={'slug': 'docker'})
tag_ops, _ = Tag.objects.get_or_create(nome='DevOps', defaults={'slug': 'devops'})

# -----------------------------------------------------------------------------
# 3. Publicar o 1º Artigo Técnico no Blog
# -----------------------------------------------------------------------------
artigo_conteudo = """# Como Estruturei uma Arquitetura Web Resiliente com Django 6, Docker e Cloudflare em VPS

Publicar uma aplicação web em produção envolve muito mais do que simplesmente executar um comando `manage.py runserver`. Quando o objetivo é entregar alta performance, segurança rigorosa contra ameaças e disponibilidade contínua em uma **VPS de baixo custo**, a arquitetura precisa ser planejada do sistema operacional até a camada de CDN.

Neste artigo, compartilho os detalhes técnicos de como estruturei o ambiente de produção do **`makisjeanty.com`** combinando **Django 6**, **Daphne ASGI**, **Docker Compose**, **MySQL 8.0**, **Redis** e **Cloudflare Full Proxy**.

---

## 🛡️ 1. Segurança & Execução Não-Root em Containers

O primeiro princípio adotado foi o da **menor permissão**. No `Dockerfile`, a aplicação não roda com privilégios de `root`. Um usuário de sistema dedicado (`appuser:appgroup`) foi provisionado para isolar o processo:

```dockerfile
# Criar usuário não privilegiado para execução do container
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app
COPY --chown=appuser:appgroup . /app/
USER appuser
```

Isso garante que, mesmo na hipótese remota de uma vulnerabilidade no nível de aplicação, o atacante não terá acesso root ao container ou ao host.

---

## 🔒 2. SSL/TLS com Cloudflare & Proxy Reverso Nginx

Para garantir criptografia ponta a ponta e proteção contra ataques DDoS, o servidor web **Nginx** atua como proxy reverso escutando nas portas `80` (HTTP) e `443` (HTTPS):

1. **Redirecionamento Canônico**: O tráfego para `www.makisjeanty.com` é redirecionado via regra 301 para a raiz `https://makisjeanty.com`.
2. **Strict-Transport-Security (HSTS)**: Forçado para subdomínios com pré-carregamento.
3. **Modo Full Proxy**: A Cloudflare atua como escudo frontal na borda (Edge Network), terminando a conexão SSL pública e trafegando criptografado até o Nginx de origem.

---

## ⚡ 3. Concorrência e WebSockets com Daphne ASGI e Redis

Em vez de utilizar o WSGI tradicional, optamos pelo servidor de aplicação **Daphne (ASGI)**. Isso permite que a mesma infraestrutura sirva requisições HTTP síncronas e conexões **WebSocket bidirecionais** (utilizadas pelo Chat ao Vivo e Fórum da Comunidade).

O **Redis** é utilizado simultaneamente como:
- **Backend de Cache de Sessões**: Reduzindo consultas repetitivas ao banco MySQL.
- **Layer de Canais (Django Channels)**: Roteando mensagens de WebSocket entre clientes com latência inferior a 10ms.

---

## 📊 4. Verificação de Saúde (Health Checks Automatizados)

A aplicação conta com um endpoint seguro de monitoria em `/health/` que valida a conectividade com o banco de dados e o Redis antes de responder `HTTP 200 OK`:

```python
def health_check(request):
    db_ok = connection.ensure_connection() is None
    cache.set('_health_check', '1', 5)
    redis_ok = (cache.get('_health_check') == '1')
    
    status_code = 200 if (db_ok and redis_ok) else 503
    return JsonResponse({
        'status': 'ok' if status_code == 200 else 'degraded',
        'database': 'ok' if db_ok else 'error',
        'redis': 'ok' if redis_ok else 'error',
    }, status=status_code)
```

---

## 🎯 Conclusão

Construir uma infraestrutura moderna não exige investimentos estratosféricos em nuvens proprietárias. Com **containers bem configurados**, **práticas de menor privilégio** e uma **camada de CDN bem ajustada**, é possível alcançar um nível de maturidade e performance enterprise mantendo custos operacionais extremamente baixos.
"""

if admin_user:
    post, created = Post.objects.update_or_create(
        slug='como-estruturei-arquitetura-web-resiliente-django-docker-cloudflare',
        defaults={
            'titulo': 'Como Estruturei uma Arquitetura Web Resiliente com Django 6, Docker e Cloudflare em VPS',
            'autor': admin_user,
            'categoria': cat_estudos,
            'resumo': 'Guia prático e estudo de caso real sobre como provisionar um servidor de produção resiliente com SSL Full, containerização não-root, cache em Redis e monitoramento de saúde.',
            'conteudo': artigo_conteudo,
            'publicado': True,
            'data_publicacao': timezone.now(),
        }
    )
    post.tags.add(tag_django, tag_docker, tag_ops)
    status_str = "Criado" if created else "Atualizado"
    print(f"✅ Post do Blog: {post.titulo} ({status_str})")

print("\n🚀 Povoamento concluído com sucesso!")
