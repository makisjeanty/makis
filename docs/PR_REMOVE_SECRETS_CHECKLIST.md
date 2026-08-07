# Checklist detalhado: Purga de histórico e Rotação de Segredos

Use este checklist para coordenar a operação de remoção de segredos do repositório.

Pre-atividade
- [ ] Notificar equipe e agendar janela de manutenção
- [ ] Criar backup (mirror) do repositório
- [ ] Verificar acesso SSH e tokens de CI

Passos (execução)
- [ ] Remover arquivos sensíveis do índice (`scripts/remove_secrets.ps1`)
- [ ] Criar PR com mudanças não sensíveis e obter aprovação (`.github/PULL_REQUEST_TEMPLATE/remove-secrets.md`)
- [ ] Clonar mirror e aplicar `git-filter-repo` (veja `scripts/purge_history.ps1`)
- [ ] Executar `git reflog expire --expire=now --all` e `git gc --prune=now --aggressive`
- [ ] Force-push para o repositório remoto

Pós-atividade
- [ ] Rotacionar `SECRET_KEY`, DB passwords, API keys, tokens de terceiros
- [ ] Revogar/renovar certificados comprometidos
- [ ] Atualizar secrets em CI/CD
- [ ] Validar deploy em staging e production
- [ ] Comunicar conclusão e registrar mudanças no RUNBOOK

Observações
- A purga altera o histórico; branches locais dos colaboradores precisarão ser rebaseadas/realinhadas.
- Recomenda-se rodar uma varredura de segredos (truffleHog, detect-secrets) após a purga.
