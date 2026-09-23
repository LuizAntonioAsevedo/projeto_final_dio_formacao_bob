---
name: desafio
description: >-
  O usuário quer um desafio de código. Ele fornecerá uma tecnologia e um nível
  (Básico, Intermediário ou Avançado).
metadata:
  user-invocable: true
  disable-model-invocation: true
---

O usuário quer um desafio de código. Ele fornecerá uma tecnologia e um nível (Básico, Intermediário ou Avançado).

Gere um desafio de código criativo, inédito e coerente com a tecnologia e nível informados, usando o seguinte formato:

---

# 🏆 Desafio DIO — {{tecnologia}} · {{nivel}}

**Dificuldade:** {{nivel}}
**Tecnologia:** {{tecnologia}}
**XP ao completar:** (500–1000 para Básico | 1500–3000 para Intermediário | 3500–6000 para Avançado)
**Tempo estimado:** (15–30min para Básico | 30–60min para Intermediário | 1–3h para Avançado)

---

## 📋 Enunciado

Descreva aqui o problema de forma clara, com contexto e objetivo.

---

## 📥 Entrada esperada
Descreva o formato e tipo de dado de entrada.

## 📤 Saída esperada
Descreva o formato e tipo de dado de saída.

---

## 💡 Dicas
- Dica 1 útil mas que não entrega a solução
- Dica 2 relacionada a um conceito da tecnologia
- Dica 3 sobre boas práticas

---

## 🧪 Casos de Teste

| Entrada | Saída esperada |
|---------|----------------|
| caso 1  | resultado 1    |
| caso 2  | resultado 2    |
| caso 3 (edge case) | resultado 3 |

---

> 💬 Quando terminar, compartilhe sua solução aqui no chat e farei um code review detalhado!

---

## Regras para geração:
- Nível Básico: foco em sintaxe, lógica simples, strings, arrays (ex: FizzBuzz, palíndromo, soma de lista)
- Nível Intermediário: algoritmos, estruturas de dados, recursão, consumo de dados (ex: ordenação customizada, parser simples, agrupamento)
- Nível Avançado: design patterns, otimização, concorrência, sistemas (ex: implementar um cache LRU, mini-interpretador, sistema de eventos)
- Varie o desafio a cada invocação — nunca repita o mesmo problema
- Use exemplos de código coerentes com a sintaxe da tecnologia escolhida nos casos de teste quando aplicável
