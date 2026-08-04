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
- **Hipótese**: `makisjeanty.com` com SEO básico começa a ser indexado e atrai tráfego crescente sem anúncios.
- **Ativo Criado**: Site no ar com sitemap, RSS, robots.txt, meta tags, sitemaps via `reverse()`.
- **Métricas escalonadas** (SEO de nicho técnico leva 3-6 meses pra aparecer — 200/Mês 1 era otimismo):
  - Mês 1: **50 visitantes** — confirma que o Google está indexando. Abaixo disso = revisar sitemap/robots.
  - Mês 3: **200-500 visitantes** — SEO começando a pegar.
  - Mês 6: **1.000+ visitantes** — validação real de tráfego orgânico.
- **Custo Máximo Aceitável**: 2h para configuração final de Go-Live (já gasto).
- **Critério de Encerramento**: Mês 6 pós-deploy.
- **Resultado**: ⏳ Em andamento
- **Aprendizado**: —

---

### Experimento 002: Build in Public — LinkedIn 8 Semanas
- **Hipótese**: 1 post/semana no LinkedIn sobre o processo de construção real por 8 semanas gera seguidores qualificados e 1 contato de oportunidade (mentoria, trabalho, parceria).
- **Ativo Criado**: Série de posts "O que construí/quebrei essa semana".
- **Métrica de Sucesso**:
  - Mínimo: 8 posts publicados sem interrupção.
  - Desejado: 50+ seguidores novos + 1 DM de oportunidade.
- **Custo Máximo Aceitável**: 30-60min/semana (máximo 8h totais).
- **Critério de Encerramento**: 8 semanas a partir do primeiro post.
- **Resultado**: ⏳ Não iniciado
- **Aprendizado**: —

---

### Experimento 003: Artigo 1 — Django + Docker em VPS
*(Registrar antes de escrever — não depois.)*
- **Hipótese**: Um tutorial prático de Django+Docker em VPS, publicado no blog + Dev.to + resumo LinkedIn, atinge 300 views em 60 dias porque é o principal pain point de Persona A.
- **Ativo Criado**: — (a criar no Mês 2)
- **Canais**: Blog `makisjeanty.com` + Dev.to + post LinkedIn resumo
- **Métrica de Sucesso**: 300 views em 60 dias pós-publicação.
- **Custo Máximo Aceitável**: 12h (pesquisa + escrita + formatação + publicação).
- **Critério de Encerramento**: 60 dias pós-publicação.
- **Resultado**: ⏳ Não iniciado
- **Aprendizado**: —

---

## ✅ Experimentos Concluídos

*(nenhum ainda)*

---

## 🚫 Experimentos Descartados

*(nenhum ainda)*
