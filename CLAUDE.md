# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack
- Django 6.0 (`requirements.txt` says `Django==6.0.7`; older docs/comments in this repo say "Django 5.0" — that's stale, trust `requirements.txt`), Python 3.13 (venv already created at `venv/`)
- MySQL via `pymysql` (NOT sqlite) — `pymysql.install_as_MySQLdb()` is called in `core/settings.py`
- Env vars via `python-decouple` (`.env` required, gitignored, contains real credentials)
- **Real-time chat runs over ASGI/WebSockets via Django Channels + Daphne** — `python manage.py runserver` now serves both HTTP and WebSocket (you'll see "Starting ASGI/Daphne development server" in its output, not the old WSGI dev server banner)
- `requirements.txt` exists (added when Channels/Daphne were introduced — install with `pip install -r requirements.txt`); still no `pyproject.toml`, `setup.py`, tests, or CI

## Setup / common commands
```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
MySQL database must exist first: `CREATE DATABASE base_central CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

`setup.sh` (run with `source setup.sh`) only generates a `SECRET_KEY` and prints these steps — it does NOT create the DB, install dependencies, or run migrations.

## App structure
- `core/` — project settings (`core/settings.py`), root urls (`core/urls.py`)
- `accounts/` — custom user model `PerfilUsuario` (extends `AbstractUser`), admin registered; public profile views in `accounts/views.py` (`sobre` = first superuser's profile, `perfil` = profile by username)
- `portfolio/` — `Projeto` + `ImagemProjeto` models, admin registered with inline gallery; public views in `portfolio/views.py` (list/filter by categoria, cases, detail by slug)
- `blog/` — `Categoria`, `Tag`, `Post`, `Comentario` models, admin registered; public views in `blog/views.py` (list/filter by categoria or tag, categories index, detail by slug, and a `ComentarioForm` in `blog/forms.py` for the comment-submission form on the detail page — new comments save with `aprovado=False` and need admin approval before showing publicly)
- `utilidades/` — no models; `utilidades/views.py` renders 5 static-ish pages (tool index + 4 tools). All 4 tools (gerador de senha, validador CPF/CNPJ, formatador JSON, conversor Base64) run **entirely client-side in vanilla JS** (inline `<script>` per template) — no data is ever POSTed to Django, by design (privacy, since some inputs are sensitive like passwords/documents)
- `comunidade/` — `Topico` + `Resposta` models (no login — name/email like blog comments), `aprovado=True` by default (posts show immediately; admin can hide after the fact via the `aprovado` checkbox, not pre-moderation). List view doubles as the "new topic" form (`TopicoForm`), detail view doubles as the "reply" form (`RespostaForm`)
- `chat/` — real-time chat, no login. `Mensagem` model persists history; `chat/consumers.py` (`ChatConsumer`, `AsyncWebsocketConsumer`) handles the live WebSocket connection on a single hardcoded room (`SALA_PADRAO = 'geral'`), saves each message via `database_sync_to_async`, then broadcasts to the `chat_geral` channel-layer group. `chat/views.py` renders the last 50 messages server-side for instant load, then `templates/chat/sala.html`'s JS connects via WebSocket for live updates. Nickname is stored in the browser's `localStorage`, not server-side
- `templates/` — `base.html` (shared nav/footer, loads Tailwind CDN + `static/css/main.css`, renders Django `messages` above `{% block content %}`, floating WhatsApp button fixed bottom-right on every page), `home.html`, `404.html`, `500.html`, plus `templates/portfolio/`, `templates/blog/`, `templates/accounts/`, `templates/utilidades/`, `templates/comunidade/`, `templates/chat/` for the app pages
- `static/` + `staticfiles/` — static assets (WhiteNoise compressed); `static/css/main.css` defines the `lw-*`/`lwh-*` design-system classes (cards, badges, tags, filter buttons, breadcrumbs, prose) shared by all templates, on top of Tailwind CDN utility classes
- `media/` — user uploads, gitignored

## URL layout
- `/` → `home` view in `core/urls.py` (renders `templates/home.html`)
- `/portfolio/`, `/portfolio/cases/`, `/portfolio/<slug>/` → `portfolio.urls` (namespace `portfolio`)
- `/blog/`, `/blog/rss/`, `/blog/categories/`, `/blog/categoria/<slug>/`, `/blog/<slug>/` → `blog.urls` (namespace `blog`)
- `/sobre/`, `/sobre/<username>/` → `accounts.urls` (namespace `accounts`)
- `/utilidades/`, `/utilidades/gerador-de-senha/`, `/utilidades/validador-cpf-cnpj/`, `/utilidades/formatador-json/`, `/utilidades/conversor-base64/` → `utilidades.urls` (namespace `utilidades`)
- `/comunidade/`, `/comunidade/<slug>/` → `comunidade.urls` (namespace `comunidade`)
- `/chat/` → `chat.urls` (namespace `chat`), the actual live connection is a WebSocket at `ws://<host>/ws/chat/` (routed separately in `core/asgi.py`, not `core/urls.py`)
- `/sitemap.xml` → `django.contrib.sitemaps`, defined in `core/sitemaps.py` (static pages, includes `chat:sala`) + `portfolio/sitemaps.py` + `blog/sitemaps.py` + `comunidade/sitemaps.py`
- **Admin is NOT at `/admin/`** — path comes from `ADMIN_URL` env var (default: `gestao-dmh8g6skcx`)
- Nav links in `base.html` use `{% url %}` tags (namespaced) — don't hardcode hrefs there
- List views (`portfolio:lista`, `blog:lista`, `blog:categoria`) are paginated (9 per page via `django.core.paginator.Paginator`) and render `templates/partials/paginacao.html`, which preserves existing query params (`?categoria=`, `?tag=`) when building prev/next links

## Critical settings (`core/settings.py`)
- `DEBUG`, `SECRET_KEY`, `DB_*`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `EMAIL_*` all come from `.env` via `decouple.config`
- `AUTH_USER_MODEL = 'accounts.PerfilUsuario'` — must not be changed after migrations exist
- `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'` — run `collectstatic` in prod
- Redis cache (`django.core.cache.backends.redis.RedisCache`) only configured when `DEBUG=False`
- Locale: `pt-br`, timezone: `America/Sao_Paulo`
- Security hardening (HSTS, SSL redirect, secure cookies, XSS filter, `X_FRAME_OPTIONS='DENY'`) is toggled by `not DEBUG`

## Design system
- Color palette (`static/css/main.css` `:root`) intentionally matches Claude.ai's look: warm dark neutrals (`--bg: #262624`, `--surface: #30302e`) instead of a cool slate/blue dark theme, with Anthropic's terracotta accent `--accent: #CC785C` carried through buttons, badges, pills, and hover states. Keep new UI within this palette rather than introducing cool blues/purples.
- Tailwind is loaded via CDN script in `base.html` (`<script src="https://cdn.tailwindcss.com">`) — there is no build step/npm in this repo, so utility classes like `grid-cols-3`, `md:flex`, `max-w-7xl` only work because of that CDN include. Preflight is left **enabled** (don't disable it again) — disabling it broke native `<button>` styling in the nav dropdowns.
- Custom component classes (`lw-card`, `lw-media-card`, `lw-badge`, `lw-tag`, `lw-filter-btn`, `lw-breadcrumb`, `lw-prose`, `lw-empty-state`, etc.) live in `static/css/main.css` alongside the Tailwind utilities — reuse these instead of inventing new ad-hoc styles when building more pages.
- The Tailwind CDN approach is fine for this low-traffic personal/portfolio site but is not recommended by Tailwind for high-traffic production use — a compiled build would be the eventual upgrade path if traffic grows.

## Real-time chat (Django Channels)
- `core/asgi.py` wires a `ProtocolTypeRouter`: HTTP goes through normal Django, WebSocket (`/ws/chat/`) goes through `chat.routing.websocket_urlpatterns` → `ChatConsumer`. `INSTALLED_APPS` has `'daphne'` listed **first** (required so `runserver` serves ASGI instead of falling back to the plain WSGI dev server) and `'channels'` alongside the other third-party apps.
- `CHANNEL_LAYERS` in `core/settings.py` uses `channels.layers.InMemoryChannelLayer` — this only works correctly with a **single process**. It's fine for `runserver` locally, but **before deploying with multiple workers/processes** (gunicorn+daphne behind nginx, several uvicorn workers, etc.), switch to `channels_redis.core.RedisChannelLayer` pointed at a real Redis instance, or messages won't reliably broadcast across processes.
- No Redis is running in this dev environment and none is required for local testing — only the (already-configured) production `CACHES` Redis backend and this future channel layer would need it.
- When writing/debugging the consumer, remember all message times must go through `django.utils.timezone.localtime()` before formatting — `criado_em.strftime(...)` on its own returns UTC, which visibly disagrees with the page's server-rendered history (already fixed once, don't reintroduce it).

## SEO
- `base.html` defines overridable blocks `meta_description`, `og_type`, `og_title`, `og_description` plus a `{% if og_image_url %}og:image{% endif %}` tag — every page template sets these; detail views (`portfolio:detalhe`, `blog:detalhe`, `accounts:sobre`/`perfil`) also pass an `og_image_url` context variable (the object's image/avatar URL, or `None`) since `og:image` needs an absolute URL that a block alone can't build cleanly.
- `sitemap.xml` and `blog/rss/` both build absolute URLs through `django.contrib.sites` (`get_current_site`), **not** from the request host — this means their domain comes from the `Site` row (`SITE_ID = 1`) in the DB, currently still Django's default `example.com` placeholder. **Before deploying**, update that Site's domain in `/<ADMIN_URL>/sites/site/1/change/` (or a data migration) to the real domain, otherwise sitemap/RSS links will be wrong even in production.

## Notable
- Not a git repository — there is no `.git` here (or in the parent `intervalo-termico/` directory either)
- `index.html` in the parent directory (`intervalo-termico/index.html`, one level above this repo) is a standalone shift-control page (localStorage-based) — not served by Django and not part of this codebase
- Admin site header/title overridden to "Painel Makis" in `core/urls.py`
- Custom 404/500 handlers defined in `core/urls.py` (`handler404`, `handler500`) — no debug tracebacks in production
- `portfolio`, `blog`, `accounts`, `utilidades`, `comunidade`, and `chat` all have views/urls/templates implemented (list, filter, detail pages, profile pages, a moderated comment form, 4 client-side tools, an open forum, and real-time chat)
- Blog post author names link to `accounts:perfil` for that user
- `copiarTexto(id, botao)` in `static/js/main.js` is the shared clipboard-copy helper used by the utilidades tools (Clipboard API with an `execCommand('copy')` fallback) — reuse it instead of writing a new copy handler per page
- Floating WhatsApp button (`.lw-whatsapp-fab` in `base.html`/`main.css`) is fixed-position on every page, separate from the footer's WhatsApp link
- Neither `comunidade` (topics/replies) nor `chat` (messages) has any spam/rate-limit protection (no CAPTCHA, no throttling) — same accepted risk posture as the blog comment form, worth revisiting before this gets real public traffic
- `AGENTS.md` at repo root duplicates this file's content for non-Claude agents — keep both in sync if either changes
