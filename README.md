# 🤖 DIO Explorer — Projeto Final · Formação IBM Bob

> Projeto final da **Formação IBM Bob AI Developer** na [DIO](https://web.dio.me).
> Um agente interativo construído com **IBM Bob** que explora trilhas de aprendizado, gera desafios de código e emite certificados fictícios — usando **Slash Commands**, **Skills** e um **MCP Server customizado** em TypeScript.

---

## 📑 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
  - [Slash Commands](#slash-commands)
  - [Skills](#skills)
  - [MCP Server](#mcp-server)
- [Catálogo de Trilhas](#catálogo-de-trilhas)
- [Como Usar](#como-usar)
- [Prompts Usados Durante o Desenvolvimento](#prompts-usados-durante-o-desenvolvimento)
- [Dicas e Insights para Futuros Desenvolvedores](#dicas-e-insights-para-futuros-desenvolvedores)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Autor](#autor)

---

## Visão Geral

O **DIO Explorer** demonstra na prática o poder do **IBM Bob** como plataforma de desenvolvimento de agentes de IA. O projeto combina três camadas de extensibilidade do Bob:

| Camada | Mecanismo | Onde fica |
|---|---|---|
| Comandos rápidos | Slash Commands | `.bob/commands/` |
| Comportamento enriquecido | Skills | `.bob/skills/` |
| Integração externa | MCP Server (TypeScript) | `dio_explorer/mcp/` |

Com essas três camadas, o agente consegue listar trilhas, gerar desafios de código sob medida e emitir certificados fictícios formatados — tudo sem sair do chat do Bob.

---

## Estrutura do Projeto

```
projeto_final_dio_formacao_bob/
├── .bob/
│   ├── mcp.json                    # Registro do MCP Server no Bob
│   ├── commands/                   # Slash commands do Bob
│   │   ├── trilha.md               # /trilha — plano de estudos
│   │   ├── desafio.md              # /desafio — desafio de código
│   │   └── certificado.md          # /certificado — emissão de certificado
│   └── skills/                     # Skills com frontmatter YAML
│       ├── trilha/SKILL.md
│       ├── desafio/SKILL.md
│       └── certificado/SKILL.md
├── dio_explorer/
│   ├── commands/                   # Documentação de referência dos comandos
│   │   ├── trilha.md
│   │   ├── desafio.md
│   │   └── certificado.md
│   ├── data/
│   │   └── trilhas_dio.json        # Catálogo com 30 trilhas DIO
│   ├── docs/
│   │   └── certificados-emitidos/  # Certificados .md gerados pelo agente
│   │       └── LuizAntonio_Java_20260923.md
│   └── mcp/                        # MCP Server em TypeScript
│       ├── src/
│       │   ├── index.ts            # Entry point (stdio + HTTP)
│       │   ├── tools.ts            # 4 tools MCP registradas
│       │   └── data.ts             # Acesso ao trilhas_dio.json
│       ├── build/                  # Saída compilada (JS)
│       │   ├── index.js
│       │   ├── tools.js
│       │   └── data.js
│       ├── package.json
│       ├── tsconfig.json
│       └── README.md
└── README.md
```

---

## Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│                      IBM Bob (chat)                       │
│                                                          │
│  /trilha Python    →  Slash Command (.bob/commands/)     │
│  /desafio Java Avançado  →  Skill (.bob/skills/)         │
│  "liste as trilhas" →  MCP Tool (dio-explorer server)    │
└────────────────────────┬─────────────────────────────────┘
                         │ stdio (processo filho)
                         ▼
              ┌─────────────────────┐
              │  dio-explorer MCP   │
              │  Server (Node.js)   │
              │                     │
              │  • listar_trilhas   │
              │  • buscar_trilha    │
              │  • gerar_desafio    │
              │  • emitir_certif.   │
              └──────────┬──────────┘
                         │ readFileSync / writeFileSync
                         ▼
              ┌─────────────────────┐
              │  trilhas_dio.json   │
              │  certificados-      │
              │  emitidos/*.md      │
              └─────────────────────┘
```

O Bob registra o MCP Server em [`.bob/mcp.json`](.bob/mcp.json) e o spawna automaticamente como processo filho via **stdio transport**. O servidor também suporta **HTTP transport** para uso remoto/API.

---

## Funcionalidades

### Slash Commands

Arquivos Markdown em `.bob/commands/` que definem a instrução executada quando o usuário digita `/nome-do-comando`. O Bob lê o conteúdo do arquivo e o usa como contexto de execução para aquela invocação.

#### `/trilha <tecnologia>`

Busca a trilha pelo campo `tecnologia` no JSON (case-insensitive) e exibe o plano de estudos completo.

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
- Promoção ativa (com desconto e validade)

**Prompt do comando** (`.bob/commands/trilha.md`):
```markdown
Leia o arquivo `dio_explorer/data/trilhas_dio.json` e busque a trilha cujo campo
`tecnologia` corresponda (de forma case-insensitive) ao argumento fornecido pelo usuário.

Se encontrada, exiba o plano de estudos com o seguinte formato:
...
Se a tecnologia não for encontrada, informe o usuário e liste todas as tecnologias disponíveis.
```

---

#### `/desafio <tecnologia> <nivel>`

Gera um desafio de código criativo e inédito para a tecnologia e nível informados.

**Níveis disponíveis:** `Básico` · `Intermediário` · `Avançado`

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
- Convite para code review após envio da solução

**XP por nível:**
| Nível | XP | Tempo estimado |
|---|---|---|
| Básico | 500–1.000 XP | 15–30 min |
| Intermediário | 1.500–3.000 XP | 30–60 min |
| Avançado | 3.500–6.000 XP | 1–3 horas |

**Regras de geração embutidas no prompt:**
- **Básico:** sintaxe, lógica simples, strings, arrays (ex: FizzBuzz, palíndromo, soma de lista)
- **Intermediário:** algoritmos, estruturas de dados, recursão (ex: ordenação customizada, parser simples)
- **Avançado:** design patterns, otimização, concorrência (ex: cache LRU, mini-interpretador, sistema de eventos)
- Varia o desafio a cada invocação — nunca repete o mesmo problema

---

#### `/certificado <nome_do_aluno> <tecnologia>`

Gera e salva um certificado fictício de conclusão em Markdown.

```
/certificado "Luiz Antonio" Java
/certificado "Maria Silva" Python
/certificado "João Costa" React
```

**O que retorna:**
- Certificado formatado no chat
- Arquivo `.md` salvo em `dio_explorer/docs/certificados-emitidos/`
- Código de validação único: `DIO-{ANOMÊS}-{SIGLA}-{4 dígitos}`
- Carga horária calculada (`módulos × 10 horas`)
- 5 competências desenvolvidas relevantes à tecnologia
- Badges conquistadas da trilha

---

### Skills

Skills são instruções persistentes carregadas automaticamente pelo Bob quando o contexto da conversa corresponde à `description` do frontmatter YAML.

**Estrutura do frontmatter:**
```yaml
---
name: trilha
description: >-
  Leia o arquivo `dio_explorer/data/trilhas_dio.json` e busque a trilha cujo
  campo `tecnologia` corresponda (de forma case-insensitive) ao argumento
  fornecido pelo usuário.
metadata:
  user-invocable: true           # Permite ativação manual
  disable-model-invocation: true # Bob executa diretamente, sem chamar outro modelo
---
```

| Skill | Arquivo | Gatilho |
|---|---|---|
| `trilha` | `.bob/skills/trilha/SKILL.md` | Usuário pede plano de estudos de uma tecnologia |
| `desafio` | `.bob/skills/desafio/SKILL.md` | Usuário pede desafio de código |
| `certificado` | `.bob/skills/certificado/SKILL.md` | Usuário pede certificado fictício |

> **Dica:** A `description` da skill funciona como um **gatilho semântico** — o Bob a usa para decidir quando carregar automaticamente a skill, sem que o usuário precise digitar nenhum comando especial.

---

### MCP Server

O coração do projeto. Um servidor **Model Context Protocol** escrito em **TypeScript + Node.js**, registrado no Bob via [`.bob/mcp.json`](.bob/mcp.json).

**Registro em `.bob/mcp.json`:**
```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": [
        "C:\\...\\dio_explorer\\mcp\\build\\index.js"
      ],
      "env": {}
    }
  }
}
```

#### Tools MCP

| Tool | Parâmetros | Descrição |
|---|---|---|
| `listar_trilhas` | `nivel?` (Básico/Intermediário/Avançado/todos) | Lista o catálogo completo ou filtrado por nível |
| `buscar_trilha` | `tecnologia` (string) | Plano de estudos completo de uma tecnologia |
| `gerar_desafio` | `tecnologia`, `nivel` | Template de desafio com XP e casos de teste |
| `emitir_certificado` | `nome_aluno`, `tecnologia` | Gera e salva certificado fictício em Markdown |

#### Transportes suportados

**stdio (padrão — usado pelo Bob):**
```bash
node build/index.js
```
O Bob spawna o servidor automaticamente como processo filho.

**HTTP (acesso remoto / API):**
```bash
node build/index.js --http              # porta 3100 (padrão)
node build/index.js --http --port 8080  # porta customizada
```

| Endpoint | Método | Descrição |
|---|---|---|
| `/` | GET | Info do servidor e tools disponíveis |
| `/mcp` | POST (sem `x-session-id`) | Inicia nova sessão MCP |
| `/mcp` | POST (com `x-session-id`) | Envia mensagem na sessão |
| `/mcp` | GET (com `x-session-id`) | SSE stream da sessão |
| `/mcp` | DELETE | Encerra a sessão |
| `/health` | GET | Health check (JSON) |

#### Estrutura do código-fonte

```
dio_explorer/mcp/src/
├── index.ts   # Entry point — detecta --http e despacha para startStdio() ou startHttp()
├── tools.ts   # Registra as 4 tools com registerTool() + schemas Zod
└── data.ts    # getTrilhas() e buscarTrilha() com cache em memória
```

**Variáveis de ambiente:**
| Variável | Padrão | Descrição |
|---|---|---|
| `MCP_HTTP_PORT` | `3100` | Porta do servidor HTTP |

#### Desenvolvimento e build

```bash
# Entrar na pasta do MCP
cd dio_explorer/mcp

# Instalar dependências
npm install

# Compilar TypeScript → JavaScript
npm run build

# Rodar em modo stdio (para testes locais)
npm run start:stdio

# Rodar em modo HTTP
npm run start:http

# Compilar em modo watch (desenvolvimento)
npm run dev
```

---

## Catálogo de Trilhas

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

## Como Usar

### Pré-requisitos

- [IBM Bob](https://marketplace.visualstudio.com/items?itemName=IBM.ibm-developer) instalado no VS Code
- Node.js 18+ instalado

### 1. Clone o repositório

```bash
git clone https://github.com/LuizAntonioAsevedo/projeto_final_dio_formacao_bob.git
cd projeto_final_dio_formacao_bob
```

### 2. Compile o MCP Server

```bash
cd dio_explorer/mcp
npm install
npm run build
cd ../..
```

### 3. Abra no IBM Bob

Abra a pasta do projeto no VS Code com o Bob ativo. O Bob detecta automaticamente o `.bob/mcp.json` e inicia o servidor `dio-explorer` como processo filho.

### 4. Use no chat

**Via Slash Commands:**
```
/trilha Python
/desafio Java Avançado
/certificado "Seu Nome" Python
```

**Via linguagem natural (MCP Tools):**
```
Liste todas as trilhas disponíveis
Liste só as trilhas de nível Avançado
Busque a trilha de React
Gere um desafio de JavaScript no nível Intermediário
Emita um certificado para "Maria Silva" na trilha de Machine Learning
```

---

## Prompts Usados Durante o Desenvolvimento

Esta seção documenta os principais prompts utilizados para construir o projeto com o Bob — úteis como referência para quem quer aprender a desenvolver com IBM Bob.

### Criação dos Slash Commands

```
Crie um slash command chamado /trilha que leia o arquivo
dio_explorer/data/trilhas_dio.json, busque a trilha pelo campo
tecnologia (case-insensitive) e exiba o plano de estudos formatado
em Markdown com módulos, badges, lives e promoção ativa.
```

```
Crie um slash command /desafio que receba tecnologia e nível
(Básico, Intermediário ou Avançado) e gere um desafio de código
criativo com enunciado, dicas, casos de teste e convite para code review.
Varie o desafio a cada invocação.
```

```
Crie um slash command /certificado que receba nome do aluno e tecnologia,
busque a trilha no JSON, calcule a carga horária (módulos × 10h),
gere um código de validação único DIO-{ANO}{MES}-{SIGLA}-{0000},
salve o certificado em dio_explorer/docs/certificados-emitidos/ e exiba
o certificado formatado no chat.
```

### Criação das Skills

```
Crie uma skill chamada "trilha" com description que descreva que o usuário
quer ver o plano de estudos de uma tecnologia. Defina user-invocable: true
e disable-model-invocation: true no frontmatter YAML.
```

```
Crie skills para "desafio" e "certificado" seguindo o mesmo padrão da
skill trilha, adaptando a description para o gatilho semântico correto.
```

### Criação do MCP Server

```
Crie um MCP Server em TypeScript usando o @modelcontextprotocol/sdk.
O servidor deve expor 4 tools: listar_trilhas, buscar_trilha,
gerar_desafio e emitir_certificado. Use Zod para os schemas de input.
Suporte dois transportes: stdio (padrão) e HTTP via --http flag.
```

```
Registre o MCP Server no Bob criando o arquivo .bob/mcp.json com
o comando node apontando para o build/index.js compilado.
```

```
A tool emitir_certificado deve salvar o certificado em Markdown em
dio_explorer/docs/certificados-emitidos/{NomeSemEspacos}_{Tecnologia}_{AAAAMMDD}.md
usando fs.writeFileSync.
```

```
Adicione um endpoint HTTP /health ao servidor MCP que retorne JSON
com status, nome do servidor, versão, número de sessões ativas e timestamp.
```

### Testes e validação

```
Quero saber se o MCP Server foi criado com sucesso.
```

```
Emita um certificado para Luiz Antonio na trilha de Java.
```

```
Liste todas as trilhas disponíveis no catálogo.
```

---

## Dicas e Insights para Futuros Desenvolvedores

### Sobre o IBM Bob

**1. Slash Commands são o jeito mais simples de começar**
Crie um arquivo `.md` em `.bob/commands/` e você já tem um comando funcionando. O conteúdo do arquivo é literalmente o prompt que o Bob vai executar — não há código, não há compilação. Perfeito para prototipar rapidamente.

**2. Skills são mais poderosas que Slash Commands**
Skills têm um `description` que funciona como gatilho semântico — o Bob as carrega automaticamente quando detecta que o contexto se encaixa. Com `disable-model-invocation: true`, o Bob executa a instrução diretamente sem chamar outro modelo, o que torna a resposta mais rápida e previsível.

**3. A `description` da skill define tudo**
Invista tempo na `description` da skill. Ela é o que o Bob usa para decidir quando ativá-la automaticamente. Seja específico o suficiente para evitar falsos positivos, mas genérico o suficiente para cobrir variações naturais do pedido do usuário.

**4. MCP Server eleva o projeto ao próximo nível**
Se Slash Commands e Skills são o "Bob como configuração", um MCP Server é o "Bob como plataforma". Com MCP você tem:
- Validação de input (schemas Zod)
- Lógica real em TypeScript (loops, datas, filesystem)
- Transporte alternativo via HTTP para expor como API
- Reutilização — qualquer cliente MCP pode usar o mesmo servidor

**5. stdio vs HTTP transport**
Use **stdio** para uso local com o Bob (é como o Bob espera — spawna o processo filho automaticamente). Use **HTTP** quando quiser expor o servidor para outros clientes, fazer testes com curl, ou colocar atrás de um proxy reverso com TLS.

**6. Valide o MCP Server com um prompt simples**
Depois de registrar o servidor no `mcp.json`, teste com uma pergunta natural como _"Liste as trilhas disponíveis"_. Se o Bob chamar a tool `listar_trilhas` automaticamente, o servidor está funcionando.

**7. Cache de dados em memória**
A função `getTrilhas()` em `data.ts` usa uma variável `_cache` para evitar leituras repetidas do JSON em disco a cada invocação da tool. Para catálogos estáticos isso é suficiente — para dados dinâmicos, considere invalidar o cache ou usar um banco de dados.

**8. Caminhos absolutos no `mcp.json`**
O Bob precisa de um caminho absoluto para o executável do MCP Server no `mcp.json`. Ao compartilhar o projeto, lembre-se de que este caminho precisa ser ajustado para o ambiente de cada desenvolvedor, ou use um script wrapper que resolva o caminho dinamicamente.

**9. O prompt é o código**
Em projetos com IBM Bob, a qualidade do output depende diretamente da qualidade do prompt. Seja descritivo nos formatos esperados, forneça exemplos concretos e defina claramente o comportamento para casos de erro (tecnologia não encontrada, etc.).

**10. Iteração rápida**
O ciclo de desenvolvimento com Bob é muito rápido: edite o arquivo `.md` do command ou skill → salve → já funciona no próximo prompt. Para o MCP Server, o ciclo é: edite o `.ts` → `npm run build` → teste no chat.

### Sobre o projeto em si

**Separação de responsabilidades:**
- **JSON** → dados estáticos (catálogo de trilhas)
- **Slash Commands / Skills** → lógica de apresentação (como formatar a resposta)
- **MCP Server** → lógica de negócio (cálculos, filesystem, validação)

**Por que duplicar commands e skills?**
Os arquivos em `.bob/commands/` e `.bob/skills/` têm propósitos diferentes: o command é ativado explicitamente pelo usuário com `/trilha`, enquanto a skill é ativada semanticamente pelo Bob quando o contexto se encaixa. Ter os dois garante que o agente responde tanto ao comando explícito quanto à intenção expressa em linguagem natural.

---

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **IBM Bob** | Plataforma de agente de IA (VS Code extension) |
| **Model Context Protocol (MCP)** | Protocolo de integração agente ↔ servidor |
| **TypeScript** | Linguagem do MCP Server |
| **Node.js** | Runtime do MCP Server |
| **Zod** | Validação de schema dos inputs das tools |
| **@modelcontextprotocol/sdk** | SDK oficial do MCP para TypeScript |
| **Markdown** | Formato dos comandos, skills e certificados |
| **JSON** | Catálogo de trilhas DIO |

---

## 🎓 Sobre o Projeto

Este projeto foi desenvolvido como **trabalho final** da Formação IBM Bob AI Developer na DIO.
O objetivo é demonstrar na prática o uso de:

- ✅ Slash Commands customizados no IBM Bob
- ✅ Skills com frontmatter YAML e gatilho semântico
- ✅ Leitura e processamento de dados JSON pelo agente
- ✅ MCP Server em TypeScript com 4 tools e dois modos de transporte
- ✅ Geração dinâmica de conteúdo (planos de estudo, desafios, certificados)
- ✅ Salvamento de arquivos gerados pelo agente via filesystem
- ✅ Validação de input com Zod
- ✅ Health check endpoint para monitoramento

---

## 👨‍💻 Autor

**Luiz Antonio Asevedo**
[GitHub](https://github.com/LuizAntonioAsevedo) · [DIO](https://web.dio.me)

---

_Projeto educacional — certificados gerados são fictícios._
_Para certificados oficiais, acesse [web.dio.me](https://web.dio.me)._
