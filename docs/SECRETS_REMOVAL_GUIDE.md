# Guia: Remoção de Segredos do Repositório e Rotação de Credenciais

Aviso: siga estas etapas com cuidado — estas operações podem exigir força de push e coordenação com a equipe.

## 1) Objetivo
Remover arquivos sensíveis do índice Git, purgar o histórico caso tenham sido commitados, e rotacionar credenciais/certificados comprometidos.

## 2) Passo rápido (remover do índice e adicionar ao .gitignore)
Execute localmente no diretório do repositório (opcional: use `scripts/remove_secrets.ps1`):

```powershell
# Remover do índice (mantém cópia local)
git rm --cached .env .env.backup nginx/ssl/makisjeanty.key
git commit -m "chore: remove sensitive files from repo index"

# Adicionar ao .gitignore
# (garanta que .gitignore contenha .env, .env.*, nginx/ssl/*)
```

Após isso, faça push para o repositório remoto:

```bash
git push origin <branch>
```

> Importante: isto NÃO remove os arquivos do histórico commits antigos.

## 3) Purgar histórico Git (quando segredos já foram commitados)
Escolha uma ferramenta: `git-filter-repo` (recomendado) ou `BFG Repo-Cleaner`.

### Usando `git-filter-repo` (recomendado)
Instale:

```bash
pip install git-filter-repo
```

Purgar arquivos:

```bash
# Faça backup do repositório antes
git clone --mirror <repo.git> repo-mirror.git
cd repo-mirror.git
git-filter-repo --invert-paths --paths .env --paths .env.backup --paths nginx/ssl/makisjeanty.key
# Depois force push
git push --force
```

### Usando BFG (alternativa)
Baixe BFG jar e rode:

```bash
# Crie um mirror
git clone --mirror <repo.git> repo-mirror.git
java -jar bfg.jar --delete-files .env --delete-files ".env.backup" --delete-files "nginx/ssl/makisjeanty.key" repo-mirror.git
cd repo-mirror.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

## 4) Rotacionar credenciais e certificados
- Gerar novo `SECRET_KEY` do Django e atualizar em ambiente seguro (ex.: vault, CI secrets). Exemplo Python minimal:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
- Trocar senhas de banco de dados, tokens de e-mail, API keys, e atualizar configurações no servidor e CI.
- Revogar e renovar o certificado cuja chave privada foi comprometida (contate a CA ou provedor SSL).
- Atualizar variáveis de ambiente no servidor e nos pipelines CI/CD (GitHub Actions, GitLab CI, etc.).

## 5) Verificar e validar
- Rodar `git log --all --full-history -- '**/.env'` para confirmar que não há referências. Use também `git grep` ou ferramentas de scanning (truffleHog, detect-secrets).
- Testar deploy em staging antes de atualizar produção.
- Rodar testes automatizados (unit/integration/e2e).

## 6) Comunicação e PR
- Notificar equipe/ops sobre a rotação de credenciais.
- Abrir uma PR com as mudanças não sensíveis (ex.: `.gitignore`), e um PR separado (ou ticket) para a purga do histórico — coordene para push forçado.

## 7) Checklist rápido
- [ ] Removido do índice e .gitignore atualizado
- [ ] Repositório mirror criado (backup)
- [ ] Histórico purgado com `git-filter-repo` ou BFG
- [ ] Forçar push e atualizar remotos
- [ ] Rotacionar SECRET_KEY, DB_PASSWORD, EMAIL creds, API keys
- [ ] Revogar/renovar certificados
- [ ] Atualizar CI/servers
- [ ] Executar testes e validar deploy

---

Se quiser, eu posso gerar um PR template e um script adicional para executar `git-filter-repo` com parâmetros seguros (apenas gerar — não executar).