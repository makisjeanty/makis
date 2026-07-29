# Auditoria de segurança e qualidade — 2026-07-29

Registro do que foi encontrado e corrigido numa revisão completa do projeto, feita em três frentes paralelas (revisor Django, revisor de segurança, revisor de qualidade de código) e depois corrigida em etapas. Commits relevantes no `origin/main`: `965d71d`, `c93f474`, `cfff6e6`.

## Como foi feita a revisão

Três agentes revisaram a base inteira em paralelo, cada um com um foco:
- **Django/ORM**: padrões de model, migrations, N+1, índices.
- **Segurança**: OWASP, injeção, autenticação, segredos, rate limiting.
- **Qualidade geral**: legibilidade, duplicação, cobertura de testes.

## CRITICAL (corrigido)

**Webhook Kiwify inseguro** (`core/views_monitoria.py`)
- Sem `KIWIFY_TOKEN` configurado, o webhook aceitava qualquer POST sem verificação (fail-open). Agora responde 503 e rejeita tudo se o token não estiver configurado.
- Comparação de token trocada para `hmac.compare_digest` (evita timing attack).
- Race condition entre `exists()` e `create()` permitia registros de compra duplicados em retries do provedor de pagamento. Corrigido com `get_or_create()` sobre `referencia_externa`, agora `unique=True` (e `null=True`, para compras manuais sem referência externa não colidirem).
- `order_value` passou a ser validado com try/except em vez de lançar exceção não tratada.

**`ALLOWED_HOSTS` com wildcard no default** (`core/settings.py`)
- O default incluía `'*'`, aceitando qualquer Host header se `.env` não definisse o valor, independente de `DEBUG`. Removido — agora falha fechado.

## HIGH (corrigido)

- **WebSocket sem validação de Origin** (`core/asgi.py`): adicionado `AllowedHostsOriginValidator`, fechando um CSWSH (Cross-Site WebSocket Hijacking) no chat em tempo real.
- **Índices faltando** em campos booleanos/status filtrados com frequência: `Post.publicado`, `Projeto.publico`, `Comentario.aprovado`, `Topico.aprovado`, `Resposta.aprovado`, `Compra.status` — todos agora com `db_index=True`.

## MEDIUM (corrigido)

- **Rate limiter do chat com race condition**: `_dentro_do_limite()` fazia `cache.get()` + `cache.set()`/`incr()` em dois passos, permitindo que mensagens concorrentes passassem do limite. Trocado para `cache.add()` + `cache.incr()` (atômicos).
- **Rate limiter do chat vulnerável a IP spoofing**: usava `scope['client']` direto, que atrás do nginx sempre resolve para o IP do container — compartilhando o limite entre todos os visitantes. Agora lê `X-Forwarded-For` e usa o **último** IP da lista (o que o nginx observou, não o que um cliente malicioso pode forjar).
- **Duplicação de código entre views** (`blog/views.py`, `comunidade/views.py`, `core/urls.py`): o padrão "checar rate-limit → checar antispam → validar form" estava repetido em 3 lugares com pequenas variações. Extraído para `core/antispam.py`'s `bloquear_submissao_suspeita()`.
- **`solicitar_orcamento` sem rate limiting**: essa view (fora do escopo original da revisão) só tinha antispam, sem `@ratelimit`. Adicionado, junto com o helper acima.
- **Zero cobertura de teste para lógica client-side real** (checksum CPF/CNPJ, geração de senha): a lógica pura foi extraída para `static/js/validador_documento.js` e `static/js/gerador_senha.js`, com 17 testes em `tests/js/*.test.js` (`node --test tests/js/*.test.js`). As partes que mexem no DOM continuam inline nos templates.
- **Querysets sem paginação nem teto** (`portfolio.views.cases`, `blog.views.lista_categorias`): adicionado um limite explícito (`CASES_MAX=12`, `CATEGORIAS_MAX=100`).

## LOW (corrigido)

- `antispam_ok()` (helper de teste) estava duplicado em `blog/tests.py` e `comunidade/tests.py` — movido para `core/testing_helpers.py`.
- Configuração do Django REST Framework e `django-filter` em `INSTALLED_APPS`/`settings.py` não tinha nenhuma view usando — removida (`requirements.txt` também), evitando que uma futura view DRF herdasse `permission_classes` silenciosamente de uma config esquecida.
- Linhas em branco sobrando no final de `utilidades/views.py` e `utilidades/tests.py`; um `import json` fora do lugar em `core/tests.py` movido para o topo do arquivo.

## Achados adicionais (fora do escopo original, encontrados no caminho)

Ao mexer em arquivos adjacentes aos achados originais, apareceram mais dois problemas reais que não estavam no escopo da revisão dos três agentes (que não cobriram `docker-compose.yml`, `Dockerfile`, nem `core/urls.py`'s `solicitar_orcamento`):

- **`docker-compose.yml` tinha segredos de fallback hardcoded** (`SECRET_KEY`, senhas de banco, `KIWIFY_TOKEN`) com valores que pareciam reais de produção, mais um `ALLOWED_HOSTS=*` fixo que teria anulado a correção do `settings.py` em qualquer deploy via Docker. Trocado para `${VAR:?mensagem de erro}` — compose recusa subir sem a variável real no `.env`.
- **Faltava `.dockerignore`**: sem ele, `Dockerfile`'s `COPY . /app/` copiaria o `.env` real para dentro da imagem. Criado, espelhando o `.gitignore`.

## Pendência conhecida (não resolvida — decisão de escopo, não bug de segurança)

`solicitar_orcamento` (`/solicitar-orcamento/`, formulário de orçamento voltado ao cliente) passa pela checagem de antispam/rate-limit e define `enviado=True`, mas **não salva a submissão em lugar nenhum nem envia e-mail/notificação** — os dados de contato reais (nome, e-mail, WhatsApp, descrição do projeto) são descartados. Isso não é uma falha de segurança, é uma lacuna funcional: hoje, pedidos de orçamento reais enviados por esse formulário não chegam a lugar nenhum. Fica registrado aqui para decisão — implicaria adicionar persistência (novo model) ou envio de e-mail, o que é uma mudança de funcionalidade, não uma correção do que já existe.

## Setup de repositório (contexto da sessão)

O diretório não tinha `.git` local no início desta sessão, apesar do `CLAUDE.md` descrever um remoto já configurado. Foram necessários, nesta ordem:
1. `git init` local — depois descoberto que `origin/main` já tinha histórico real e desconectado (10+ commits).
2. Reconciliação via `git reset --mixed origin/main` (mantém os arquivos no disco, adota o histórico real).
3. Geração de uma chave SSH dedicada (`~/.ssh/id_ed25519_makis`) e registro como deploy key com escrita em `github.com/makisjeanty/makis` — a chave que o `CLAUDE.md` citava não existia mais.

## Estado final

- **114 testes Django** (`python manage.py test`, via `core/test_settings.py` para rodar sem MySQL local) — todos passando.
- **17 testes JS** (`node --test tests/js/*.test.js`) — todos passando.
- `CLAUDE.md`/`AGENTS.md` atualizados para refletir o app `core/` (model `Compra`, webhook Kiwify, painel de monitoria), as rotas que faltavam documentar, a validação de Origin do WebSocket, o rate-limiter do chat, o stack Docker, e como rodar os testes JS.
