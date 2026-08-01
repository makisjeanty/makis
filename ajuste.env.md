# Configurar produção do site pessoal makisjeanty.com

## Contexto

O domínio `makisjeanty.com` foi comprado e está sendo gerenciado pela Cloudflare.

O site será minha plataforma pessoal de autoridade e conexão profissional. Ele deverá servir como:

* portfólio profissional;
* apresentação pessoal;
* blog técnico;
* central dos meus projetos;
* publicação de estudos de caso;
* divulgação de produtos digitais;
* página de contato;
* construção de autoridade em software, arquitetura, IA e empreendedorismo;
* conexão com público francófono, crioulo haitiano e internacional.

A aplicação será hospedada na VPS Contabo.

## Infraestrutura disponível

* VPS: Contabo
* IP público: `195.26.252.210`
* Sistema: Ubuntu 24.04 LTS
* Usuário administrativo: `makishub`
* Docker Engine e Docker Compose instalados
* PostgreSQL em container
* Redis em container
* Rede Docker interna: `makishub-backend`
* UFW ativo
* Fail2Ban ativo
* SSH somente por chave
* Cloudflare responsável por domínio e DNS

## Domínios oficiais

```env
PRIMARY_DOMAIN=makisjeanty.com
WWW_DOMAIN=www.makisjeanty.com
SITE_URL=https://makisjeanty.com
```

O domínio canônico deve ser:

```text
https://makisjeanty.com
```

O endereço:

```text
https://www.makisjeanty.com
```

deve redirecionar permanentemente para:

```text
https://makisjeanty.com
```

## Objetivo da tarefa

Analise o projeto e ajuste a configuração de produção, especialmente o `.env`, sem remover variáveis existentes que ainda sejam necessárias.

Não invente nomes de módulos, caminhos, serviços ou variáveis sem verificar primeiro o código existente.

Antes de alterar qualquer arquivo:

1. Identifique o framework e a estrutura real do projeto.
2. Localize como as variáveis de ambiente são carregadas.
3. Encontre o módulo de configurações de produção.
4. Identifique todas as variáveis utilizadas pelo código.
5. Crie backup dos arquivos que serão alterados.
6. Nunca exponha valores secretos nos logs ou na resposta final.

## Configuração esperada para Django

Use ou adapte as seguintes variáveis conforme os nomes já utilizados no projeto:

```env
DJANGO_ENV=production
DJANGO_DEBUG=False

DJANGO_ALLOWED_HOSTS=makisjeanty.com,www.makisjeanty.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://makisjeanty.com,https://www.makisjeanty.com

SITE_NAME=Makis Jeanty
SITE_DOMAIN=makisjeanty.com
SITE_URL=https://makisjeanty.com
SITE_LANGUAGE=fr
SITE_TIME_ZONE=UTC
```

Se o projeto usa nomes simples em vez do prefixo `DJANGO_`, adapte para:

```env
DEBUG=False
ALLOWED_HOSTS=makisjeanty.com,www.makisjeanty.com
CSRF_TRUSTED_ORIGINS=https://makisjeanty.com,https://www.makisjeanty.com
```

Não mantenha duas variáveis equivalentes se apenas uma delas for consumida pelo código.

## Segredos

A chave do Django deve ser exclusiva de produção e gerada de maneira criptograficamente segura:

```env
DJANGO_SECRET_KEY=GENERATE_A_STRONG_RANDOM_SECRET
```

Não reutilize:

* segredo de desenvolvimento;
* senha do usuário Linux;
* senha do PostgreSQL;
* token da Cloudflare;
* chave de outra aplicação.

Não escreva o segredo real em documentação, Git, saída de terminal ou mensagem de resposta.

## PostgreSQL

O banco já roda em container na rede Docker interna.

Use como referência:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=makishub
POSTGRES_USER=makishub_app
POSTGRES_PASSWORD=READ_FROM_EXISTING_SECURE_ENV
```

Se o projeto usa uma única URL:

```env
DATABASE_URL=postgresql://makishub_app:URL_ENCODED_PASSWORD@postgres:5432/makishub
```

Não publique a porta `5432` no host.

Não copie a senha existente para arquivos versionados.

Verifique se esse banco será compartilhado ou se o site pessoal receberá banco e usuário próprios. A opção preferencial é separar por aplicação:

```env
POSTGRES_DB=makisjeanty
POSTGRES_USER=makisjeanty_app
```

Não altere o banco atual automaticamente. Apresente primeiro o impacto e o plano de migração.

## Redis

O Redis está disponível na rede interna:

```env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=READ_FROM_EXISTING_SECURE_ENV
```

Caso o projeto use URL:

```env
REDIS_URL=redis://:URL_ENCODED_PASSWORD@redis:6379/0
```

Não publique a porta `6379`.

Só configure Redis para:

* cache;
* sessões;
* filas;
* Celery;
* rate limiting;

se o projeto realmente utilizar esses recursos.

## Configurações de segurança esperadas

Verifique e configure corretamente:

```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

Como haverá proxy reverso e Cloudflare, verifique no Django:

```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
```

Não ative HSTS antes de confirmar que:

* HTTPS funciona no domínio principal;
* `www` funciona ou redireciona corretamente;
* nenhum subdomínio necessário depende de HTTP;
* a conexão Cloudflare → origem também usa TLS.

Para a primeira publicação, HSTS pode começar com valor reduzido e ser aumentado após validação.

## Cloudflare

A configuração esperada é:

* registro `A` para `makisjeanty.com` apontando para `195.26.252.210`;
* registro `CNAME` para `www` apontando para `makisjeanty.com`;
* proxy Cloudflare ativado;
* SSL/TLS no modo `Full (strict)`;
* nunca usar modo `Flexible`;
* HTTPS obrigatório;
* DNSSEC ativado quando o domínio estiver estável.

Não exponha tokens da Cloudflare no `.env` da aplicação, a menos que exista uma integração real que precise deles.

## Proxy reverso

Prepare o proxy para:

```text
makisjeanty.com
www.makisjeanty.com
```

Requisitos:

* HTTPS;
* redirecionamento HTTP → HTTPS;
* redirecionamento `www` → domínio principal;
* encaminhamento para o container Django;
* cabeçalhos corretos de proxy;
* limites de upload explícitos;
* logs;
* health check;
* compressão segura para conteúdo apropriado.

Não exponha diretamente Gunicorn ou o servidor ASGI à internet.

## E-mail

Não invente credenciais SMTP.

Deixe a configuração claramente pendente caso ainda não exista provedor:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
CONTACT_EMAIL=
```

O formulário de contato não deve ser publicado sem:

* proteção contra spam;
* validação;
* rate limiting;
* tratamento seguro dos dados;
* política de privacidade.

## Idiomas

A arquitetura deve permitir inicialmente:

* francês;
* crioulo haitiano;
* inglês futuramente.

Configuração inicial recomendada:

```env
DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,ht
```

Não implemente internacionalização improvisada. Verifique primeiro se o projeto já utiliza o sistema de tradução do Django.

## SEO e identidade

Configure, quando o projeto oferecer suporte:

```env
SITE_TITLE=Makis Jeanty
SITE_AUTHOR=Makis Jeanty
SITE_DESCRIPTION=Software, architecture, artificial intelligence and digital entrepreneurship.
CANONICAL_URL=https://makisjeanty.com
ROBOTS_INDEX=True
```

Garanta:

* canonical URL;
* sitemap;
* robots.txt;
* metadados Open Graph;
* Twitter Cards;
* páginas 404 e 500;
* nenhuma indexação de admin, staging ou URLs internas.

## Arquivos estáticos e uploads

Verifique:

```env
STATIC_URL=/static/
MEDIA_URL=/media/
```

Para produção:

* executar `collectstatic`;
* usar volume persistente ou object storage conforme necessidade;
* nunca guardar uploads importantes apenas dentro da camada gravável do container;
* definir limites de upload;
* validar extensões e tipos de arquivo.

## Observabilidade

Configure sem expor dados sensíveis:

```env
LOG_LEVEL=INFO
```

Os logs não devem registrar:

* senhas;
* tokens;
* cookies;
* chaves;
* corpo completo de formulários;
* dados pessoais desnecessários.

Adicionar health check público simples, por exemplo:

```text
/health/
```

Ele deve verificar a aplicação sem revelar detalhes internos.

## Resultado esperado

Ao finalizar, apresente:

1. arquivos analisados;
2. variáveis existentes;
3. variáveis adicionadas ou alteradas;
4. valores que ficaram como placeholders;
5. riscos encontrados;
6. comandos de validação;
7. plano de rollback;
8. diferenças entre desenvolvimento e produção;
9. confirmação de que nenhum segredo foi exposto;
10. conteúdo seguro de um `.env.example`, nunca o `.env` real.

## Restrições obrigatórias

* Não commitar `.env`.
* Não exibir segredos.
* Não sobrescrever o `.env` sem backup.
* Não abrir PostgreSQL ou Redis para a internet.
* Não usar `DEBUG=True` em produção.
* Não usar `ALLOWED_HOSTS=*`.
* Não usar SSL `Flexible` na Cloudflare.
* Não executar migrações destrutivas sem análise.
* Não subir a aplicação antes de executar os checks de produção.
* Não alterar DNS sem apresentar previamente os registros propostos.

## exemplo DJANGO_ENV=production

DJANGO_DEBUG=False
DJANGO_SECRET_KEY=replace_with_secure_secret

DJANGO_ALLOWED_HOSTS=makisjeanty.com,www.makisjeanty.com
DJANGO_CSRF_TRUSTED_ORIGINS=<https://makisjeanty.com,https://www.makisjeanty.com>

SITE_NAME=Makis Jeanty
SITE_DOMAIN=makisjeanty.com
SITE_URL=<https://makisjeanty.com>
SITE_LANGUAGE=fr
SITE_TIME_ZONE=UTC

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=makisjeanty
POSTGRES_USER=makisjeanty_app
POSTGRES_PASSWORD=replace_with_secure_password

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=replace_with_secure_password
REDIS_URL=redis://:replace_with_url_encoded_password@redis:6379/0

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

DEFAULT_LANGUAGE=fr
SUPPORTED_LANGUAGES=fr,ht

LOG_LEVEL=INFO

EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
CONTACT_EMAIL=
