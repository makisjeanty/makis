# 📦 Ideia: Micro-SaaS de Logística/Inventário

> Status: **Rascunho plantado — NÃO ativar antes da Fase P4.**
> Registrado agora para não perder a ideia. Não abrir essa frente enquanto P1/P2/P3 não tiverem execução real.

---

## Por que esta ideia existe

Trabalho em armazenagem/logística. Conheço o domínio de dentro: WMS, controle de estoque, fluxo de pedidos, diferença entre o que o sistema registra e o que acontece no chão de galpão. Esse conhecimento de domínio é raro em devs Django.

99% dos devs que constroem SaaS de logística aprendem o domínio do zero. Eu já tenho o domínio — me falta só o produto.

---

## Problema a resolver

Pequeno comerciante / loja física / depósito:
- Controla estoque em planilha Excel ou WhatsApp.
- Não tem verba pra ERP (Totvs, SAP, OMIE = R$ 500-2.000/mês).
- Precisa de: controle de entrada/saída, alerta de estoque baixo, pedido pra fornecedor, histórico simples.

---

## ICP (Cliente ideal)

- Pequeno comerciante com 1-3 funcionários.
- Fatura R$ 10.000-100.000/mês.
- Usa WhatsApp como sistema de gestão hoje.
- Já conhece pelo menos 1 pessoa do meu círculo profissional.

---

## MVP (mínimo viável)

- Cadastro de produtos + movimentação (entrada/saída)
- Alerta de estoque mínimo (e-mail ou WhatsApp)
- Relatório semanal simples (PDF ou CSV)
- Sem app mobile no início — só web responsiva
- Tech: Django + MySQL + Celery (alertas) + WhiteNoise

---

## Modelo de receita

- R$ 49/mês (até 500 SKUs)
- R$ 97/mês (até 2.000 SKUs + suporte por WhatsApp)
- Sem freemium — trial de 14 dias, depois paga.

---

## Cronograma de validação (antes de construir qualquer linha)

| Fase | Mês | Ação | Critério de avanço |
|---|---|---|---|
| Conversas informais | Mês 6 | 1 conversa com 1 pessoa do círculo de trabalho sobre a dor real | Ela confirma que o problema existe e é frequente |
| Mais conversas | Mês 7-8 | +2 conversas com o framework de perguntas abaixo | 2 de 3 descrevem o mesmo problema sem você induzir |
| Pré-venda | Mês 9 | Oferta: R$ 49 × 3 meses = R$ 147 à vista, com garantia de devolução | **1+ pessoa paga** → ativa P4. 0 pessoas pagam → documenta e decide |

### Framework de perguntas (conversas de validação)
1. "Como você controla o estoque hoje?"
2. "O que acontece quando o estoque acaba sem você perceber?"
3. "Já perdeu venda por isso? Quanto mais ou menos?"
4. "O que você faz quando precisa fazer pedido pro fornecedor?"
5. "Quanto você pagaria por mês pra isso não acontecer mais?"
*Não mencionar o produto até a pergunta 5. Deixar eles descreverem o problema.*

---

## Riscos

- Suporte de pequeno comerciante é intenso em tempo — pode consumir mais do que o produto gera.
- Churn alto se o produto não for simples o suficiente.
- Regulatório: NF-e/NFC-e seria feature futura, não MVP.

---

## Quando ativar P4 (construir)

- Mês 10+ (nunca antes)
- 1+ pessoa pagou na pré-venda
- R$ 1.000/mês de outra receita (não depender do SaaS pra pagar a VPS)
- Pelo menos 1 conversa de validação documentada com transcrição/notas
