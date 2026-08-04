# ✍️ Pipeline de Conteúdo & Estratégia Editorial

> Frequência calibrada para **2h/dia** com faculdade + trabalho noturno.
> Regra: melhor 1 post consistente por semana do que 5 posts em explosão e silêncio por 3 semanas.

---

## Frequência real por canal

| Canal | Frequência | Tempo/semana | Fase |
|---|---|---|---|
| LinkedIn "Build in Public" | 1x/semana | 30-60min | P1 — AGORA |
| Blog (artigo profundo) | 1x/mês | 8-12h distribuídas | P1 |
| Newsletter | Quinzenal (NÃO semanal) | 3-4h/edição | P2 |
| X/Twitter | Oportunístico (não forçar) | — | P2+ |

---

## Série prioritária: "Build in Public" (LinkedIn)

Formato: 5-10 linhas + 1 imagem/screenshot quando possível.
- **O que construí essa semana**
- **O que quebrou e o que aprendi**
- **Próximo passo**

Não precisa ser viral. Precisa ser consistente por 8 semanas.

Exemplos de pauta:
- "Essa semana movi as views do `core` pra um único `views.py` — parecia simples, achei 2 imports desnecessários herdados."
- "Corrigido: sitemap estava gerando URLs com `example.com`. Aqui está como o `django.contrib.sites` funciona na prática."
- "Trabalhei 6h hoje na armazenagem, voltei às 2h e fiz 1 commit. Progresso é progresso."

---

## Calendário de artigos (Fase P1)

| Mês | Título | Público |
|---|---|---|
| 2 | Do Zero à Produção: Django + Docker em VPS de Baixo Custo | PT-BR |
| 3 | RUNBOOK que funciona às 3h da manhã: Arquitetura de Resposta a Incidentes | PT-BR |
| 4 | Construindo SaaS sendo júnior, trabalhando à noite, com R$ 0 de marketing | PT-BR |
| 5 | (opcional FR) Comment j'ai déployé Django en production avec 2h par jour | FR |

---

## Fluxo de publicação (1 artigo → múltiplos canais)

```
Artigo no Blog
    ├── Resumo para Newsletter (quando existir)
    ├── 3-5 posts LinkedIn extraídos dos principais pontos
    └── Repo GitHub com código de exemplo (quando aplicável)
```

---

## O que NÃO fazer (anti-patterns de conteúdo)

- ❌ Publicar tutorial genérico que já existe no YouTube em inglês
- ❌ Forçar frequência maior do que o tempo real permite (leva ao burnout e abandono)
- ❌ Começar newsletter antes de ter 8 semanas de posts LinkedIn no histórico
- ❌ Escrever 2 artigos no mesmo mês pra "compensar" o mês anterior — distribui o esforço
