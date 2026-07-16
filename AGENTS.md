# AGENTS.md

## Stack
- Django 6.0 (`requirements.txt` says `Django==6.0.7`; older docs/comments in this repo say "Django 5.0" — that's stale, trust `requirements.txt`), Python 3.13 (venv already created)
- MySQL via `pymysql` (NOT sqlite)
- Env vars via `python-decouple` (`.env` required)
- Real-time chat runs over ASGI/WebSockets via Django Channels + Daphne — `runserver` now serves both HTTP and WebSocket (look for "Starting ASGI/Daphne development server" in its output)
- `requirements.txt` exists (added with Channels/Daphne) — `pip install -r requirements.txt`. Includes `Pillow` (required by `ImageField`: `avatar`, `imagem_principal`, `imagem_capa`). Still no `pyproject.toml`, `setup.py`, or CI
- Tests exist: `<app>/tests.py` per app, Django's built-in `TestCase` (not pytest). Run with `python manage.py test` (74 tests). `core/` needs its `__init__.py` for bare `manage.py test` to pick up `core/tests.py` — it's not in `INSTALLED_APPS`, so it's easy to silently skip

## Setup
```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
MySQL database must exist first: `CREATE DATABASE base_central CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
`.env` contains real credentials and is gitignored.
No MySQL locally? Validate migrations/tests/admin against a throwaway SQLite DB via a settings module that does `from core.settings import *` then reassigns `DATABASES` (and adds `'testserver'` to `ALLOWED_HOSTS` for `Client()`), kept outside the repo — don't edit `core/settings.py` for this.

## App Structure
- `core/` — project settings (`core/settings.py`), root urls (`core/urls.py`)
- `accounts/` — custom user model `PerfilUsuario` (extends `AbstractUser`) + `Habilidade` (skill with `nivel` 1-3 and `categoria`, FK via `related_name='skills'`), admin registered; public profile views implemented (`sobre` = first superuser's profile, `perfil` = profile by username). Profile page groups skills by category with a 3-star meter, and shows `perfil.filosofia` as a "Minha filosofia" card when filled in
- `portfolio/` — `Projeto` (has both `categoria` — web/mobile/data/automacao/outro — **and** a separate `tipo` — pessoal/academico/fork, independently filterable) + `ImagemProjeto` models, admin registered with inline gallery; public views implemented (list/filter by categoria and/or tipo, cases, detail by slug)
- `blog/` — `Categoria`, `Tag`, `Post`, `Comentario` models, admin registered; public views implemented (list/filter, categories index, detail by slug, plus a `ComentarioForm` for the comment form — new comments save with `aprovado=False` and need admin approval). Data migration seeds "Estudos de Caso"/"Resumos Técnicos"/"Desafios" categories; **nav labels this app "Estudos"** even though the app/URLs/templates are still named `blog`
- `utilidades/` — no models; renders a tool index + 4 tools (gerador de senha, validador CPF/CNPJ, formatador JSON, conversor Base64). All 4 run **entirely client-side in vanilla JS** — no data is ever POSTed to Django, by design (privacy)
- `comunidade/` — `Topico` + `Resposta` models, no login (name/email like blog comments), `aprovado=True` by default (posts show immediately, admin can hide after the fact). List view doubles as the "new topic" form, detail view doubles as the "reply" form
- `chat/` — real-time chat, no login. `Mensagem` model persists history; `chat/consumers.py` (`ChatConsumer`) handles the live WebSocket on a single hardcoded room (`SALA_PADRAO = 'geral'`), saves via `database_sync_to_async`, broadcasts to the `chat_geral` channel-layer group. View renders last 50 messages server-side, then JS connects via WebSocket for live updates. Nickname lives in browser `localStorage`, not server-side
- `templates/` — `base.html` (shared nav/footer, loads Tailwind CDN + `static/css/main.css`, renders Django `messages` above `{% block content %}`, floating WhatsApp button fixed bottom-right on every page), `home.html`, `404.html`, `500.html`, `templates/portfolio/`, `templates/blog/`, `templates/accounts/`, `templates/utilidades/`, `templates/comunidade/`, `templates/chat/`
- `static/` + `staticfiles/` — static assets (WhiteNoise compressed); `static/css/main.css` defines the `lw-*`/`lwh-*` design-system classes on top of Tailwind CDN utilities
- `media/` — user uploads, gitignored

## URL Layout
- `/` → `home` view (renders `templates/home.html`)
- `/portfolio/`, `/portfolio/cases/`, `/portfolio/<slug>/` → `portfolio.urls` (namespace `portfolio`)
- `/blog/`, `/blog/rss/`, `/blog/categories/`, `/blog/categoria/<slug>/`, `/blog/<slug>/` → `blog.urls` (namespace `blog`)
- `/sobre/`, `/sobre/<username>/` → `accounts.urls` (namespace `accounts`)
- `/utilidades/`, `/utilidades/gerador-de-senha/`, `/utilidades/validador-cpf-cnpj/`, `/utilidades/formatador-json/`, `/utilidades/conversor-base64/` → `utilidades.urls` (namespace `utilidades`)
- `/comunidade/`, `/comunidade/<slug>/` → `comunidade.urls` (namespace `comunidade`)
- `/chat/` → `chat.urls` (namespace `chat`); the live connection is a WebSocket at `ws://<host>/ws/chat/`, routed separately in `core/asgi.py`, not `core/urls.py`
- `/sitemap.xml` → `django.contrib.sitemaps`, defined in `core/sitemaps.py` (includes `chat:sala`) + `portfolio/sitemaps.py` + `blog/sitemaps.py` + `comunidade/sitemaps.py`
- **Admin is NOT at `/admin/`** — uses obfuscated path from `ADMIN_URL` env var (default: `gestao-dmh8g6skcx`)
- Nav links in `base.html` use `{% url %}` tags — don't hardcode hrefs there
- Nav label ≠ app name: "Portfolio" shows as **"Projetos"**, "Blog" shows as **"Estudos"** — app names/URLs/template dirs are unchanged, only visible text
- List views (`portfolio:lista`, `blog:lista`, `blog:categoria`) are paginated (9/page) via `templates/partials/paginacao.html`, which preserves query params like `?categoria=`/`?tag=`

## Critical Settings
- `DEBUG`, `SECRET_KEY`, `DB_*`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `EMAIL_*` all from `.env`
- `AUTH_USER_MODEL = 'accounts.PerfilUsuario'` — must not be changed after migrations
- `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'` — collectstatic needed in prod
- Redis cache only active when `DEBUG=False`
- Locale: `pt-br`, timezone: `America/Sao_Paulo`

## Design System
- Color palette (`static/css/main.css` `:root`) matches Claude.ai's look: warm dark neutrals (`--bg: #262624`, `--surface: #30302e`) instead of a cool slate/blue theme, with Anthropic's terracotta accent `--accent: #CC785C` used throughout. Stay within this palette.
- Accent color has **three WCAG-AA-verified tiers** — don't merge them, no single shade passes both "white text on this" and "this as text on the page bg": `--accent` (text on dark bg — logo, links, focus rings), `--accent-solid`/`--accent-solid-hover` (solid fills with white text — primary buttons, active filters, WhatsApp FAB), `--accent-light` (accent text on tinted pill/badge backgrounds). `--danger`/`--success` were lightened too (text-only, no tiering needed).
- Tailwind is loaded via CDN in `base.html` — no build step/npm in this repo. Preflight is left enabled; disabling it broke native `<button>` styling in the nav dropdowns.
- Reuse the `lw-*` component classes in `main.css` (`lw-card`, `lw-media-card`, `lw-badge`, `lw-tag`, `lw-filter-btn`, `lw-breadcrumb`, `lw-prose`, `lw-empty-state`) instead of inventing new styles.
- Tailwind CDN is acceptable for this low-traffic site but not for high-traffic production — a compiled build is the eventual upgrade path.
- Don't rely on Tailwind responsive utilities (`md:flex-row`, `md:w-2/5`, etc.) to override unconditional rules in `main.css` for the *same* element/class — `main.css` loads after the Tailwind CDN's injected stylesheet, so at equal specificity `main.css` wins regardless of the media query, silently no-opping the Tailwind utility. Use a dedicated modifier class in `main.css` instead (see `.lw-media-card--horizontal`).

## Real-time chat (Django Channels)
- `core/asgi.py` wires a `ProtocolTypeRouter`: HTTP through normal Django, WebSocket (`/ws/chat/`) through `chat.routing.websocket_urlpatterns` → `ChatConsumer`. `INSTALLED_APPS` has `'daphne'` listed **first** (required for `runserver` to serve ASGI) and `'channels'` with the other third-party apps.
- `CHANNEL_LAYERS` uses `channels.layers.InMemoryChannelLayer` — only correct with a single process. Fine for local `runserver`; **before deploying with multiple workers/processes**, switch to `channels_redis.core.RedisChannelLayer` with a real Redis, or broadcasts won't reach all processes.
- No Redis runs in this dev environment and none is required locally.
- Message times must go through `django.utils.timezone.localtime()` before formatting in the consumer — `.strftime()` alone returns UTC and will visibly disagree with the server-rendered history.

## SEO
- `base.html` defines overridable blocks `meta_description`, `og_type`, `og_title`, `og_description` plus a conditional `og:image` tag driven by an `og_image_url` context variable that detail views pass explicitly.
- `sitemap.xml` and `blog/rss/` build absolute URLs via `django.contrib.sites` (`SITE_ID = 1`), not the request host. The Site row is still the default `example.com` placeholder — **update it before deploying** (`/<ADMIN_URL>/sites/site/1/change/`) or sitemap/RSS links will point to the wrong domain.
- `robots.txt` is served by the `robots_txt` view in `core/urls.py` (plain text, not a static file) — disallows the admin path, points to `/sitemap.xml`.
- JSON-LD: `base.html` emits `Organization` schema everywhere via `{% block structured_data %}`; `blog/detalhe.html` adds `Article`, `portfolio/detalhe.html` adds `CreativeWork` (both render alongside, not instead of, the base block). User-controlled fields go through `|escapejs` to stay JSON-safe.

## Notable
- This is a git repository (remote `origin` → `git@github.com:makisjeanty/makis.git`, branch `main`). Push uses a dedicated SSH key at `~/.ssh/id_ed25519_makis` (not the default identity) — use `GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_makis -o IdentitiesOnly=yes"` for push/fetch unless that key is added to the agent
- `.gitignore` excludes `.claude/settings.local.json` alongside the usual `.env`/`venv/`/`staticfiles/`/`media/`
- `index.html` in the parent directory (one level above this repo) is a standalone shift-control page (localStorage-based), not served by Django, not part of this codebase
- Admin site header overridden to `Painel Makis` (`core/urls.py`)
- Custom 404/500 handlers defined in `core/urls.py` — no debug tracebacks in production
- `portfolio`, `blog`, `accounts`, `utilidades`, `comunidade`, and `chat` all have views/urls/templates implemented, including profile pages, a moderated comment form, 4 client-side tools, an open forum, and real-time chat
- Blog post author names link to `accounts:perfil` for that user
- `copiarTexto(id, botao)` in `static/js/main.js` is the shared clipboard-copy helper used by the utilidades tools — reuse it instead of writing a new copy handler
- Floating WhatsApp button (`.lw-whatsapp-fab`) is fixed-position on every page, separate from the footer's WhatsApp link
- Neither `comunidade` nor `chat` has spam/rate-limit protection (no CAPTCHA, no throttling) — same accepted risk posture as the blog comment form
- `setup.sh` only generates `SECRET_KEY`; it does NOT create the DB, install dependencies, or run migrations
- Accessibility: skip-to-content link (`#conteudo-principal`) first in `base.html`'s body; nav dropdown buttons carry `aria-haspopup`/`aria-expanded` synced by `toggleDropdown()` in `main.js` (also closes on `Escape`). Heading hierarchy is h1→h2→h3 everywhere, no skipped levels — don't demote card-grid titles back to h3 for font-size reasons, use CSS classes for that.
- Migrations dropping a field that might hold real data need a `RunPython` step to migrate that data into its replacement *before* the `RemoveField` — see `accounts/migrations/0002_remove_perfilusuario_habilidades_and_more.py` (`CreateModel` → `RunPython` → `RemoveField`) for the pattern. Don't assume the field is empty just because the local DB is.
- Below-the-fold images (list/gallery/related cards) use `loading="lazy"`; each page's likely LCP element (avatar, blog cover, project hero image) intentionally doesn't.
