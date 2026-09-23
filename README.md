# 🤖 DIO Explorer — Projeto Final · Formação IBM Bob

> Projeto final da **Formação IBM Bob AI Developer** na [DIO](https://web.dio.me).  
> Um agente interativo construído com **IBM Bob** que explora trilhas de aprendizado, gera desafios de código e emite certificados fictícios com base no catálogo da DIO.

---

## 📁 Estrutura do Projeto

```
projeto_final_dio_formacao_bob/
├── .bob/
│   ├── commands/               # Slash commands registrados no Bob
│   │   ├── trilha.md           # /trilha — plano de estudos
│   │   ├── desafio.md          # /desafio — desafio de código
│   │   └── certificado.md      # /certificado — emissão de certificado
│   └── skills/                 # Skills (instruções avançadas) do Bob
│       ├── trilha/SKILL.md
│       ├── desafio/SKILL.md
│       └── certificado/SKILL.md
├── dio_explorer/
│   ├── commands/               # Documentação dos comandos (referência)
│   │   ├── trilha.md
│   │   ├── desafio.md
│   │   └── certificado.md
│   ├── data/
│   │   └── trilhas_dio.json    # Catálogo com 30 trilhas DIO
│   ├── docs/
│   │   └── certificados-emitidos/  # Certificados gerados pelo agente
│   ├── mcp/                    # (reservado para integrações MCP futuras)
│   └── src/                    # (reservado para código-fonte futuro)
└── README.md
```

---

## ⚡ Comandos Disponíveis

### `/trilha <tecnologia>`

Recebe o nome de uma tecnologia e retorna o plano de estudos completo da trilha correspondente, buscando os dados em `dio_explorer/data/trilhas_dio.json`.

**Exemplos:**
```
/trilha Python
/trilha React
/trilha AWS
/trilha IBM Bob
```

**O que retorna:**
- Nome e nível da trilha
- Total de módulos e XP
- Lista de módulos gerados criativamente (do básico ao Projeto Final Integrador)
- Badges disponíveis
- Lives ao vivo agendadas
- Informação de promoção ativa (com desconto e validade)

---

### `/desafio <tecnologia> <nivel>`

Gera um desafio de código único, criativo e coerente com a tecnologia e nível escolhidos.

**Níveis disponíveis:** `Básico` · `Intermediário` · `Avançado`

**Exemplos:**
```
/desafio Python Básico
/desafio JavaScript Intermediário
/desafio Java Avançado
```

**O que retorna:**
- Enunciado detalhado do problema
- Formato de entrada e saída esperados
- 3 dicas úteis (sem entregar a solução)
- 3 casos de teste com edge cases
- Convite para code review após a solução

**XP por nível:**
| Nível | XP | Tempo estimado |
|---|---|---|
| Básico | 500–1.000 XP | 15–30 min |
| Intermediário | 1.500–3.000 XP | 30–60 min |
| Avançado | 3.500–6.000 XP | 1–3 horas |

---

### `/certificado <nome_do_aluno> <tecnologia>`

Gera e salva um certificado fictício de conclusão de trilha em Markdown.

**Exemplos:**
```
/certificado "Luiz Antonio" Python
/certificado "Maria Silva" React
/certificado "João Costa" AWS
```

**O que retorna:**
- Certificado formatado exibido no chat
- Arquivo `.md` salvo em `dio_explorer/docs/certificados-emitidos/`
- Código de validação único no formato `DIO-{ANOMÊS}-{TECN}-{0000}`
- Carga horária calculada (`módulos × 10h`)
- 5 competências desenvolvidas relevantes à tecnologia
- Lista de badges conquistadas da trilha

---

## 📊 Catálogo de Trilhas

O arquivo [`dio_explorer/data/trilhas_dio.json`](dio_explorer/data/trilhas_dio.json) contém **30 trilhas** cobrindo as principais tecnologias do mercado:

| # | Tecnologia | Nível | Módulos | XP Total |
|---|---|---|---|---|
| 1 | IBM Bob | Intermediário | 8 | 12.500 |
| 2 | Python | Básico | 10 | 15.000 |
| 3 | JavaScript | Básico | 12 | 18.000 |
| 4 | React | Intermediário | 9 | 14.000 |
| 5 | Node.js | Intermediário | 11 | 16.500 |
| 6 | AWS | Básico | 7 | 10.000 |
| 7 | Microsoft Azure | Intermediário | 10 | 15.500 |
| 8 | Google Cloud | Avançado | 13 | 20.000 |
| 9 | DevOps | Intermediário | 8 | 13.000 |
| 10 | Machine Learning | Avançado | 15 | 25.000 |
| 11 | TensorFlow | Avançado | 14 | 22.000 |
| 12 | Apache Spark | Avançado | 12 | 19.000 |
| 13 | SQL | Básico | 6 | 9.000 |
| 14 | Java | Intermediário | 11 | 17.000 |
| 15 | C# | Intermediário | 10 | 15.000 |
| 16 | TypeScript | Intermediário | 9 | 13.500 |
| 17 | Flutter | Básico | 8 | 11.000 |
| 18 | Kotlin | Intermediário | 10 | 16.000 |
| 19 | Swift | Intermediário | 9 | 14.500 |
| 20 | Segurança | Básico | 7 | 10.500 |
| 21 | DevOps (Avançado) | Avançado | 13 | 20.500 |
| 22 | Solidity | Avançado | 11 | 18.500 |
| 23 | Figma | Básico | 8 | 11.500 |
| 24 | Unity | Intermediário | 12 | 17.500 |
| 25 | GenAI | Avançado | 10 | 16.000 |
| 26 | Power BI | Básico | 6 | 9.500 |
| 27 | Go | Intermediário | 9 | 13.000 |
| 28 | Rust | Avançado | 11 | 19.000 |
| 29 | Testes | Básico | 7 | 10.000 |
| 30 | Arquitetura | Avançado | 14 | 23.000 |

---

## 🧠 Como Funciona (Arquitetura Bob)

Este projeto utiliza dois mecanismos do IBM Bob para estender o comportamento do agente:

### Slash Commands (`.bob/commands/`)
Arquivos Markdown que definem a instrução executada quando o usuário digita `/nome-do-comando`. O Bob lê o arquivo e usa seu conteúdo como contexto de execução para aquela invocação.

### Skills (`.bob/skills/`)
Skills são instruções persistentes carregadas automaticamente pelo Bob quando o contexto da conversa se encaixa na `description` do frontmatter YAML. Cada skill possui:
- `name` — identificador único
- `description` — gatilho semântico para ativação automática
- `metadata.user-invocable: true` — permite ativação manual pelo usuário
- `metadata.disable-model-invocation: true` — Bob executa diretamente, sem chamar outro modelo

---

## 🚀 Como Usar

1. Abra este repositório no **IBM Bob**
2. Use qualquer um dos três comandos no chat:
   ```
   /trilha Python
   /desafio Python Intermediário
   /certificado "Seu Nome" Python
   ```
3. O agente lê o catálogo em `dio_explorer/data/trilhas_dio.json` e responde de acordo

---

## 🎓 Sobre o Projeto

Este projeto foi desenvolvido como **trabalho final** da Formação IBM Bob AI Developer na DIO.  
O objetivo é demonstrar na prática o uso de:

- ✅ Slash Commands customizados no IBM Bob
- ✅ Skills com frontmatter YAML e instruções de comportamento
- ✅ Leitura e processamento de dados JSON pelo agente
- ✅ Geração dinâmica de conteúdo (planos de estudo, desafios, certificados)
- ✅ Salvamento de arquivos gerados pelo agente

---

## 👨‍💻 Autor

**Luiz Antonio Asevedo**  
[GitHub](https://github.com/LuizAntonioAsevedo) · [DIO](https://web.dio.me)

---

_Projeto educacional — certificados gerados são fictícios._  
_Para certificados oficiais, acesse [web.dio.me](https://web.dio.me)._
