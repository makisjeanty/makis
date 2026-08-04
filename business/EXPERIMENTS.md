# 🧪 Registro de Experimentos & Validação de Hipóteses

Conforme a [ADR-BUSINESS-001](../docs/adr/ADR-BUSINESS-001.md), todo experimento deve validar uma hipótese clara com métricas quantitativas e custo delimitado.

---

## 📋 Modelo de Registro

```markdown
### Experimento NNN: [Nome]
- **Hipótese**: Se criarmos [Ativo], obteremos [Resultado] porque [Justificativa].
- **Ativo Criado**: [Link / Descrição]
- **Métrica de Sucesso**: [Número concreto]
- **Custo Máximo Aceitável**: [Horas / R$]
- **Critério de Encerramento**: [Data ou Limite]
- **Resultado**: Aprovado / Reprovado / Pivotado
- **Aprendizado**: [O que os dados mostraram]
```

---

## 🟡 Experimentos em Andamento

### Experimento 001: Validação de Tráfego Orgânico — Site no Ar
- **Hipótese**: `makisjeanty.com` com SEO básico atrai 200 visitantes únicos no primeiro mês sem anúncios.
- **Ativo Criado**: Site no ar com sitemap, RSS, robots.txt, meta tags.
- **Métrica de Sucesso**: 200 visitantes únicos nos primeiros 30 dias pós-deploy.
- **Custo Máximo Aceitável**: 2h para configuração final de Go-Live.
- **Critério de Encerramento**: 30 dias após o deploy na VPS.
- **Resultado**: ⏳ Em andamento
- **Aprendizado**: —

---

### Experimento 002: Build in Public — LinkedIn 8 Semanas
- **Hipótese**: Publicar 1 post/semana no LinkedIn sobre o processo de construção real (não tutorial) por 8 semanas gera seguidores qualificados e 1 contato de mentoria ou oportunidade de trabalho.
- **Ativo Criado**: Série de posts "O que construí/quebrei essa semana".
- **Métrica de Sucesso**:
  - Mínimo: 8 posts publicados sem interrupção.
  - Desejado: 50+ seguidores novos + 1 DM de oportunidade (trabalho, mentoria, parceria).
- **Custo Máximo Aceitável**: 30-60min/semana (máximo 8h totais no período).
- **Critério de Encerramento**: 8 semanas a partir do primeiro post.
- **Resultado**: ⏳ Não iniciado
- **Aprendizado**: —

---

## ✅ Experimentos Concluídos

*(nenhum ainda)*

---

## 🚫 Experimentos Descartados

*(nenhum ainda)*
