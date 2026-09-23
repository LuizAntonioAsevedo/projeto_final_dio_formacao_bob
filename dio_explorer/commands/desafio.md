# Slash Command: /desafio

## Descrição
Gera um desafio de código aleatório baseado no nível e tecnologia escolhidos pelo usuário.

## Uso
```
/desafio <tecnologia> <nivel>
```

## Exemplos
```
/desafio Python Básico
/desafio JavaScript Intermediário
/desafio Java Avançado
```

## Níveis disponíveis
- `Básico` — Desafios simples, focados em sintaxe e lógica fundamental
- `Intermediário` — Desafios com estruturas de dados, algoritmos e boas práticas
- `Avançado` — Desafios complexos com performance, design patterns e arquitetura

## Template de resposta

```markdown
# 🏆 Desafio DIO — {tecnologia} ({nivel})

**Dificuldade:** {nivel}
**Tecnologia:** {tecnologia}
**XP ao completar:** {xp}
**Tempo estimado:** {tempo}

---

## 📋 Enunciado

{enunciado}

---

## 📥 Entrada esperada
{entrada}

## 📤 Saída esperada
{saida}

---

## 💡 Dicas
- {dica_1}
- {dica_2}
- {dica_3}

---

## 🧪 Casos de Teste

| Entrada | Saída esperada |
|---------|---------------|
| {caso_1_entrada} | {caso_1_saida} |
| {caso_2_entrada} | {caso_2_saida} |
| {caso_3_entrada} | {caso_3_saida} |

---

> 💬 Quando terminar, compartilhe sua solução e eu farei um code review!
```

## Instruções para o agente

### Nível Básico
- Gere desafios como: FizzBuzz, inversão de string, soma de array, palíndromo, calculadora simples
- XP: entre 500 e 1.000
- Tempo estimado: 15–30 minutos

### Nível Intermediário
- Gere desafios como: manipulação de listas/dicionários, algoritmos de ordenação, consumo de API, CRUD simples, recursão
- XP: entre 1.500 e 3.000
- Tempo estimado: 30–60 minutos

### Nível Avançado
- Gere desafios como: implementação de design patterns, otimização de algoritmos O(n), sistema de cache, concorrência, parser de expressões
- XP: entre 3.500 e 6.000
- Tempo estimado: 1–3 horas

### Regras gerais
- O desafio deve ser **coerente com a tecnologia** informada (use sintaxe e conceitos da linguagem)
- Gere **3 casos de teste** válidos incluindo edge cases
- As dicas devem ser úteis mas não entregar a solução
- Varie os desafios a cada chamada (use criatividade para não repetir)
- Se a tecnologia não for reconhecida, sugira as disponíveis em `data/trilhas_dio.json`
