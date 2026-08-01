# ADR-BUSINESS-001: Geração Obrigatória de Ativos Permanentes por Projeto

- **Status**: Aprovado
- **Data**: 2026-08-01
- **Contexto**: O ecossistema de engenharia e infraestrutura atingiu maturidade **adequada para o estágio atual do produto** (nota 9,5/10). O gargalo principal do negócio passou a ser a **construção de audiência, autoridade, comunidade e validação de mercado** (nota 3/10).
- **Decisão**: A partir deste marco, nenhum projeto, módulo ou código novo será iniciado sem a garantia de criação de pelo menos um **ativo permanente de negócio**.

---

## 📌 Principais Regras da ADR

### 1. Multiplicação de Ativos por Esforço
Todo desenvolvimento técnico deve produzir desdobramentos em ativos reutilizáveis e rastreáveis de conteúdo/negócio:
- 📝 **Artigo Técnico / Estudo de Caso** (Arquitetura, Django, IA, Engenharia).
- 📧 **Edição de Newsletter / Conteúdo para Redes**.
- 🛠️ **Ferramenta Gratuita / Template / Calculator / API Pública**.
- 📚 **Documentação & Exemplos Reutilizáveis de Código**.

### 2. O Gatekeeper Pré-Projeto (5 Perguntas Obrigatórias)
Nenhum projeto ou repositório será iniciado sem responder formalmente a estas 5 perguntas:

1. **Qual ativo permanente de negócio será criado?**
2. **Qual hipótese de mercado ou usuário será validada?**
3. **Qual métrica quantitativa decidirá se continuamos ou encerramos?**
4. **Qual é o custo máximo aceitável (tempo e recursos)?**
5. **Qual é o critério explícito de encerramento/abandono?**

---

## 🎯 Impacto e Consequências

- **Positivas**:
  - Elimina o desenvolvimento de "código fantasma" que não gera audiência ou receita.
  - A tecnologia passa a servir 100% ao crescimento do negócio e construção de autoridade.
  - Reduz drasticamente o tempo gasto em ajustes finos invisíveis na infraestrutura (VPS).
- **Compromisso**:
  - A infraestrutura atual é tratada como **invisível e funcional**. Alterações de infraestrutura só serão permitidas se houver bloqueio real de operação.

---

> 🧠 **Visão de Longo Prazo**: Esta ADR é o primeiro pilar de decisão do **Makis Operating System (MOS)**, garantindo que cada novo ciclo de desenvolvimento alimente o ecossistema central de valor da empresa.
