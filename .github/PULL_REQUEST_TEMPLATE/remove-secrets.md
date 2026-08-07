# PR: Remoção de segredos / Purga de histórico

## Descrição
Este PR contém alterações não sensíveis relacionadas à remoção de segredos do repositório (ex.: atualização de `.gitignore`, scripts auxiliares, documentação). A purga completa do histórico será executada separadamente e exigirá push forçado a partir de um mirror.

## Alterações incluídas
- Atualização de `.gitignore` para ignorar `.env` e `nginx/ssl/`
- Scripts em `scripts/` para auxiliar a remoção e purga do histórico
- Documentação em `docs/SECRETS_REMOVAL_GUIDE.md`

## Checklist (necessário antes de merge)
- [ ] Confirmar que este PR NÃO contém segredos nem arquivos sensíveis
- [ ] Validar que a purga do histórico será feita por uma branch/PR/worker separada
- [ ] Comunicar equipe/ops sobre janela de manutenção para forçar push
- [ ] Garantir backup do repositório (mirror)

## Instruções pós-merge
1. Abrir procedimento controlado para rodar `scripts/purge_history.ps1` (ou equivalente) em servidor/ambiente controlado.
2. Coordenar rotação de credenciais e certificados conforme `docs/SECRETS_REMOVAL_GUIDE.md`.
3. Atualizar secrets em CI e servidores.

Solicite aprovação de um mantenedor e do time de infra/ops antes de prosseguir com a purga de histórico.