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

## MVP (mínimo viável para validar)

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

## Validação necessária antes de construir

1. [ ] 3 conversas com pessoas do meu círculo de trabalho sobre a dor real.
2. [ ] 1 pessoa disposta a pagar R$ 49/mês antes de eu construir (pré-venda).
3. [ ] Verificar se existe concorrente direto acessível no Brasil nesse ticket.

---

## Riscos

- Suporte de pequeno comerciante é intenso em tempo — pode consumir mais do que o produto gera.
- Churn alto se o produto não for simples o suficiente.
- Regulatório: NF-e/NFC-e seria feature futura, não MVP.

---

## Quando ativar

- Fase P4 (Mês 10+)
- Após ter ao menos 1 cliente piloto do círculo profissional concordando em testar
- Com pelo menos R$ 1.000/mês de outra receita (pra não depender do SaaS antes de validar)
