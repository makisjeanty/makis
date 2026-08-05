# makis-home · Site Pessoal

Plataforma pessoal em Django 6 integrando portfólio, blog/estudos, chat em tempo real, ferramentas client-side e plataforma de cursos interativos.

**Produção:** [makisjeanty.com](https://makisjeanty.com)

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Django 6.0.7 · Python 3.13 |
| Banco de dados | MySQL 8 via `pymysql` |
| Real-time | Django Channels 4 + Daphne (ASGI) |
| Cache / Broker | Redis 7 (`InMemoryChannelLayer` local, Redis em produção) |
| Deploy | Docker · nginx · Daphne · Contabo VPS (Ubuntu 24.04) |
| CDN / SSL | Cloudflare Full Strict |
| Static files | WhiteNoise (CompressedManifest) |

**Dependências:**
```
Django==6.0.7
PyMySQL==1.2.0
cryptography==49.0.0
python-decouple==3.8
whitenoise==6.12.0
channels==4.3.2
daphne==4.2.2
Pillow==12.3.0
channels_redis==4.3.0
django-ratelimit==4.1.0
```

---

## Setup local

### Pré-requisitos
- Python 3.13 (venv já criado em `venv/`)
- MySQL 8 rodando localmente
- Redis — apenas com `DEBUG=False` (não necessário para dev)

### Passos

```bash
# 1. Criar o banco de dados no MySQL
mysql -u root -p -e "CREATE DATABASE base_central CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Copiar e preencher as variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# 3. Ativar o venv e instalar dependências
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt

# 4. Migrações e superusuário
python manage.py migrate
python manage.py createsuperuser

# 5. Iniciar servidor (ASGI/Daphne)
python manage.py runserver
# Saída: "Starting ASGI/Daphne development server"
```

> **Sem MySQL local?** Use `core/test_settings.py` para rodar contra SQLite throwaway.
> Atenção: SQLite pode ocultar bugs reais do MySQL (ex.: `TransactionTestCase` vs `TestCase` com Channels).

---

## Estrutura de apps

```
makis-home/
├── core/          # Settings, root URLs, ASGI, model Compra, painel monitoria, antispam, webhook Kiwify
├── accounts/      # Modelo custom PerfilUsuario (AbstractUser) + Habilidade
├── portfolio/     # Projeto + ImagemProjeto (filtro por categoria e tipo)
├── blog/          # Post + Categoria + Tag + Comentario (moderado) + gerenciador-ia
├── utilidades/    # 20 ferramentas client-side em vanilla JS (sem POST para o servidor)
├── comunidade/    # Fórum aberto (Topico + Resposta)
├── chat/          # Chat em tempo real via WebSocket (Mensagem + ChatConsumer)
├── cursos/        # Plataforma de lições: Curso → Modulo → Licao → Etapa
├── templates/     # base.html + templates por app
├── static/        # main.css (design system lw-*) + JS
├── tests/js/      # Testes Node.js para lógica pura de utilidades
├── nginx/         # nginx.conf para produção
└── docs/adr/      # Architecture Decision Records
```

---

## URLs principais

| URL | Destino |
|---|---|
| `/` | Home |
| `/sobre/` | Perfil do superusuário |
| `/portfolio/` | Lista de projetos |
| `/portfolio/cases/` | Cases |
| `/portfolio/<slug>/` | Detalhe do projeto |
| `/blog/` | Estudos / blog |
| `/blog/rss/` | Feed RSS |
| `/blog/categories/` | Índice de categorias |
| `/blog/categoria/<slug>/` | Posts por categoria |
| `/blog/gerenciador-ia/` | Gerenciador IA (blog) |
| `/blog/<slug>/` | Detalhe do post |
| `/utilidades/` | Índice de ferramentas (20 ferramentas) |
| `/comunidade/` | Fórum |
| `/comunidade/<slug>/` | Tópico do fórum |
| `/chat/` | Chat em tempo real |
| `/cursos/` | Lista de cursos |
| `/cursos/<slug>/` | Trilha do curso |
| `/cursos/licao/<id>/` | Executar lição |
| `/sitemap.xml` | Sitemap |
| `/robots.txt` | robots.txt |
| `/health/` | Health check |
| `/solicitar-orcamento/` | Formulário de orçamento |
| `/produtos/kit-dev-pro/` | Página de produto digital |
| `/<ADMIN_URL>/` | Admin (URL obfuscada via `ADMIN_URL` no `.env`) |
| `/<MONITORIA_URL>/` | Dashboard de monitoria (superuser-only) |
| `/api/webhook/kiwify/` | Webhook de pagamento Kiwify |

WebSocket: `ws://<host>/ws/chat/`

---

## Testes

```bash
# Suite Django completa (142 testes)
python manage.py test

# Testes JS — lógica de CPF/CNPJ e gerador de senha (17 testes, roda local, não no CI)
node --test tests/js/*.test.js

# Rodar com SQLite (sem MySQL local)
python manage.py test --settings=core.test_settings
```

**CI** (`.github/workflows/tests.yml`) roda `python manage.py test` com MySQL 8 a cada push/PR em `main`. Os testes JS **não rodam no CI** — apenas localmente.

> Testes do `ChatConsumer` via `WebsocketCommunicator` devem usar `TransactionTestCase`,
> não `TestCase` — o MySQL rejeita o acesso cross-thread criado pelo `TestCase`; o SQLite
> tolera e esconde o bug.

---

## Deploy com Docker

```bash
docker compose up --build -d
docker compose logs -f web
```

Stack: `nginx` (porta 80) → `web` (Daphne 8000) → `db` (MySQL 8) + `redis`

O `docker-compose.yml` usa `${VAR:?erro}` para todos os secrets — falha fechado se qualquer variável obrigatória estiver ausente. Nunca use `:-default` para secrets.

---

## Variáveis de ambiente

Ver `.env.example` para a lista completa. Variáveis críticas:

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta Django |
| `DEBUG` | `True` local, `False` em produção |
| `ALLOWED_HOSTS` | Domínios permitidos |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` | Conexão MySQL |
| `REDIS_URL` | Redis (padrão: `redis://127.0.0.1:6379`) |
| `ADMIN_URL` | Caminho do admin (padrão: `gestao-dmh8g6skcx`) |
| `MONITORIA_URL` | Caminho do painel de monitoria (padrão: `monitoria`) |
| `KIWIFY_TOKEN` | Token HMAC para webhook Kiwify |
| `EMAIL_*` | Configurações de e-mail |

---

## Design system

Paleta warm-dark — `static/css/main.css`:

| Variável CSS | Uso |
|---|---|
| `--bg: #262624` | Fundo da página |
| `--surface: #30302e` | Cards, painéis |
| `--accent: #CC785C` | Texto accent sobre fundo escuro (links, logo) |
| `--accent-solid: #B35738` | Botões primários, filtros ativos (texto branco) |
| `--accent-light: #DF957C` | Texto accent sobre badges/pills tintados |

O accent tem 3 tiers WCAG-AA distintos — não colapsá-los num único valor.
Classes de componente: `lw-card`, `lw-media-card`, `lw-badge`, `lw-tag`, `lw-filter-btn`, `lw-breadcrumb`, `lw-prose`, `lw-empty-state`.

---

## Scripts de seed de dados

```bash
python popular_dados.py             # Projetos de portfólio
python popular_cursos.py            # Árvore completa de cursos
python adicionar_artigos_blog.py    # Posts do blog
python adicionar_produtos_anuncio.py # Entradas de portfólio de produto
```

Cada script faz `django.setup()` internamente — rodar diretamente, não via `manage.py`.
Verificar idempotência antes de re-executar contra um DB populado.

---

## Documentação

| Arquivo/Pasta | Conteúdo |
|---|---|
| [`AGENTS.md`](./AGENTS.md) | Contexto completo para agentes de IA |
| [`CLAUDE.md`](./CLAUDE.md) | Contexto para Claude Code |
| [`RUNBOOK.md`](./RUNBOOK.md) | Operação em produção, incidentes, backup |
| [`GO_LIVE_CHECKLIST.md`](./GO_LIVE_CHECKLIST.md) | DNS / SSL / Cloudflare / go-live |
| [`AUDITORIA_SEGURANCA.md`](./AUDITORIA_SEGURANCA.md) | Auditoria de segurança |
| `business/` | Visão, roadmap, monetização, personas, micro-SaaS, experimentos |
| `docs/adr/` | Architecture Decision Records |

---

## Licença

Privado — © Makis Jeanty. Todos os direitos reservados.
