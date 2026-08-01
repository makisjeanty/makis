# 🧪 Registro de Experimentos & Validação de Hipóteses

Conforme a [ADR-BUSINESS-001](file:///d:/makis-home/makis-home/docs/adr/ADR-BUSINESS-001.md), todo experimento deve validar uma hipótese clara com métricas quantitativas e custo delimitado.

---

## 📋 Modelo de Registro de Experimento

```markdown
### Experimento 001: [Nome do Experimento]
- **Hipótese**: Se criarmos [Ativo], obteremos [Resultado] porque [Justificativa].
- **Ativo Criado**: [Link / Descrição do ativo permanente]
- **Métrica de Sucesso**: [Ex: 100 inscritos em 14 dias]
- **Custo Máximo Aceitável**: [Ex: 10 horas de trabalho / R$ 0 em tráfego pago]
- **Critério de Encerramento**: [Data ou Limite]
- **Resultado**: [Aprovado / Reprovado / Pivotado]
- **Aprendizado**: [O que descobrimos com os dados reais]
```

---

## 🧪 Experimentos em Andamento

### Experimento 001: Publicação da Landing Page e Validação de Tráfego Orgânico
- **Hipótese**: O site pessoal no domínio `makisjeanty.com` publicado com boas práticas de SEO atrai os primeiros 200 visitantes únicos no primeiro mês sem anúncios pagos.
- **Ativo Criado**: Site [makisjeanty.com](file:///d:/makis-home/makis-home/GO_LIVE_CHECKLIST.md) no ar.
- **Métrica de Sucesso**: 200 visitantes únicos no Google Analytics / Plausible nos primeiros 30 dias pós-deploy.
- **Custo Máximo Aceitável**: 2 horas para configuração final de Go-Live.
- **Critério de Encerramento**: 30 dias após o deploy na VPS.
