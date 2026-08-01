# 🚀 Manual Operacional & Checklist de Go-Live (`makisjeanty.com`)

Este documento consolida a estratégia de infraestrutura, rotinas operacionais, monitoramento, plano de backup/restauração e o checklist final para a publicação oficial do site **`makisjeanty.com`** na VPS Contabo.

---

## 🔒 1. Configuração de DNS, Cloudflare e SSL/TLS

### Requisitos Obrigatórios da Cloudflare
1. **Modo SSL/TLS**: Definir obrigatoriamente para **`Full (strict)`**.
   - *Nunca* utilizar o modo `Flexible` (previne ataques man-in-the-middle entre a Cloudflare e a VPS).
2. **Registros de DNS**:
   - **Registro A**: `makisjeanty.com` ➔ `195.26.252.210` (Proxy Status: **Proxied / Orange Cloud**).
   - **Registro CNAME**: `www` ➔ `makisjeanty.com` (Proxy Status: **Proxied / Orange Cloud**).
3. **Regras de Redirecionamento (Edge & Nginx)**:
   - **HTTP ➔ HTTPS**: Forçar HTTPS na Cloudflare (*Always Use HTTPS: ON*).
   - **www ➔ Domínio Principal**: Redirecionar `https://www.makisjeanty.com/*` permanentemente (301) para `https://makisjeanty.com/$1`.
4. **Certificado de Origem (Origin CA Certificate)**:
   - Gerar Certificado de Origem na Cloudflare para a VPS.
   - Instalar o certificado na VPS em `/etc/ssl/certs/makisjeanty.pem` e chave em `/etc/ssl/private/makisjeanty.key`.

---

## 🗄️ 2. Persistência de Dados & Gestão do MySQL

### Topologia de Volumes Docker & Política de Reinício
O banco de dados roda no container `makis_mysql` (MySQL 8.0). Todos os containers utilizam a política `restart: unless-stopped` no [docker-compose.yml](file:///d:/makis-home/makis-home/docker-compose.yml):

```yaml
services:
  db:
    image: mysql:8.0
    container_name: makis_mysql
    restart: unless-stopped
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:      # Mapeado em /var/lib/mysql no container
  media_data:      # Mapeado em /app/media no container
  static_data:     # Mapeado em /app/staticfiles no container
```

- **Localização no Host Linux (VPS)**: `/var/lib/docker/volumes/makishub_mysql_data/_data`
- **Validação de Persistência**: Testado que ao executar `docker compose down`, os dados do banco e uploads de mídia permanecem intactos.

---

## 💾 3. Estratégia de Backup, RPO/RTO e Teste de Restauração (Restore)

> [!IMPORTANT]
> **Metas Operacionais de Recuperação**:
> - **RPO (Recovery Point Objective)**: **24 horas** (Perda máxima tolerável de dados = dados das últimas 24h).
> - **RTO (Recovery Time Objective)**: **30 minutos** (Tempo máximo para restabelecer a operação completa).

### Rotina de Backup Automático
- **Frequência**: Diário (às 03:00 UTC).
- **Retenção**: 30 dias de histórico armazenados localmente e sincronizados para storage remoto seguro.
- **Script de Backup (`/opt/scripts/backup_makis.sh`)**:
  ```bash
  #!/bin/bash
  set -e
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  BACKUP_DIR="/var/backups/makisjeanty"
  mkdir -p "$BACKUP_DIR"

  # Dump do Banco MySQL
  docker exec makis_mysql mysqldump -u root -p"${DB_ROOT_PASSWORD}" base_central | gzip > "$BACKUP_DIR/db_$TIMESTAMP.sql.gz"

  # Backup dos arquivos de mídia
  tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" -C /var/lib/docker/volumes/makishub_media_data/_data .

  # Limpeza de backups mais antigos que 30 dias
  find "$BACKUP_DIR" -type f -mtime +30 -delete
  ```

### Procedimento Passo a Passo de Teste de Restauração (Restore)
Executar a cada 90 dias em um ambiente isolado (staging) para homologação:

1. **Restaurar Banco de Dados**:
   ```bash
   # Descomprimir o dump
   gunzip -c /var/backups/makisjeanty/db_YYYYMMDD_HHMMSS.sql.gz > restore.sql

   # Importar para o container de teste ou produção
   docker exec -i makis_mysql mysql -u root -p"${DB_ROOT_PASSWORD}" base_central < restore.sql
   rm restore.sql
   ```
2. **Restaurar Mídia**:
   ```bash
   tar -xzf /var/backups/makisjeanty/media_YYYYMMDD_HHMMSS.tar.gz -C /var/lib/docker/volumes/makishub_media_data/_data
   ```
3. **Validação**:
   - Rodar `python manage.py check`.
   - Acessar a aplicação e validar a rota `/health/` e imagens de portfólio.

---

## 📜 4. Logs, Rotação e Proibição de Comandos Perigosos

### 1. Rotação de Logs no Docker (`docker-compose.yml`)
Adicionado limite rígido de rotação para cada serviço:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "5"
```

### 2. Proibição de Comandos Destrutivos no Redis
> [!CAUTION]
> **PROIBIDO EM PRODUÇÃO**: Nunca executar `redis-cli FLUSHALL` em produção.
> Esse comando apaga todas as sessões ativas de usuários, filas do Celery/Channels, limites de rate-limit e dados em cache. Para invalidar cache específico, utilize chaves com TTL ou limpe via Django `cache.delete()`.

---

## 🔄 5. Fluxo de Deploy e Rollback Seguro por Releases

### Deploy Seguro e Eficiente (Aproveitando Cache de Build)
```bash
# 1. Acessar a pasta da aplicação na VPS
cd /home/makishub/makis-home

# 2. Obter o código atualizado
git pull origin main

# 3. Baixar imagens base e buildar aproveitando camadas em cache
docker compose pull
docker compose build
docker compose up -d

# 4. Executar as migrações de banco (se houver)
docker exec makis_web python manage.py migrate --noinput

# 5. Coletar arquivos estáticos atualizados
docker exec makis_web python manage.py collectstatic --noinput
```

### Plano de Rollback Baseado em Tags de Release
Em vez de comandos destrutivos no histórico do Git (`git reset`), as compilações de produção utilizam **Tags Semânticas de Versão** (ex: `v1.0.0`, `v1.0.1`).

**Procedimento de Rollback de Emergência**:
```bash
# 1. Listar as últimas tags de versão estável
git tag -l

# 2. Alternar para a tag da versão anterior conhecida como estável (ex: v1.0.0)
git checkout v1.0.0

# 3. Re-subir os containers na versão estável
docker compose build
docker compose up -d
```

---

## 📊 6. Observabilidade e Endpoint de Saúde Embutido

### Endpoint de Saúde Enriquecido (`/health/`)
O endpoint `/health/` em [core/urls.py](file:///d:/makis-home/makis-home/core/urls.py#L46-L68) testa as conexões de banco de dados e Redis em tempo real, retornando HTTP 200 (OK) ou HTTP 503 (Degraded) no formato JSON sem expor segredos ou versões:

```json
{
  "status": "ok",
  "database": "ok",
  "redis": "ok",
  "storage": "ok"
}
```

### Métricas Críticas de Monitoramento
- **Métricas de Servidor**: CPU (>85%), RAM (>800MB por container), Uso de Disco na VPS (>80%), Espaço nos Volumes Docker.
- **Métricas de Aplicação**: Tempo de resposta médio (>1s), Taxa de erros HTTP 404 e 500.
- **Certificados e Domínio**: Validade do Certificado SSL Cloudflare (alerta com 30 dias de antecedência) e renovação do domínio `makisjeanty.com`.

---

## ✅ 7. Checklist Final de Go-Live (Checkboxes Operacionais)

- [ ] Registro A e CNAME apontados na Cloudflare com proxy ativo (Orange Cloud).
- [ ] Modo SSL/TLS ajustado para **Full (strict)** na Cloudflare.
- [ ] Redirecionamento de `http://` para `https://` verificado no navegador.
- [ ] Redirecionamento de `https://www.makisjeanty.com` para `https://makisjeanty.com` (301) verificado.
- [ ] Firewall UFW na VPS permitindo apenas portas 22 (SSH), 80 (HTTP) e 443 (HTTPS).
- [ ] Portas 3306 (MySQL) e 6379 (Redis) fechadas para a internet externa.
- [ ] `DEBUG=False` no arquivo `.env`.
- [ ] `SECRET_KEY` gerada e exclusiva de produção configurada.
- [ ] `ALLOWED_HOSTS=makisjeanty.com,www.makisjeanty.com` configurado no `.env`.
- [ ] `CSRF_TRUSTED_ORIGINS=https://makisjeanty.com,https://www.makisjeanty.com` ativo.
- [ ] Executado `python manage.py check --deploy` sem nenhum alerta ou erro.
- [ ] Executado `python manage.py collectstatic --noinput` sem falhas.
- [ ] Container `makis_web` rodando sob usuário não-root `appuser`.
- [ ] Todos os serviços configurados com `restart: unless-stopped`.
- [ ] Endpoint `/health/` respondendo `200 {"status": "ok", "database": "ok", "redis": "ok", "storage": "ok"}`.
- [ ] Script de backup diário do MySQL e Mídia instalado na CRON da VPS (RPO=24h, RTO=30min).
- [ ] Teste de restauração (*Restore*) simulado e homologado com sucesso.
- [ ] Rotação de logs do Docker (`max-size: 10m`) ativada no `docker-compose.yml`.

---

> 🔒 **Status do Código & Infraestrutura**: CONGELADO (Code Freeze). A infraestrutura está **adequada para o estágio atual do produto**. Foco redirecionado para o Go-Live e geração de ativos de negócio conforme [ADR-BUSINESS-001](file:///d:/makis-home/makis-home/docs/adr/ADR-BUSINESS-001.md).
