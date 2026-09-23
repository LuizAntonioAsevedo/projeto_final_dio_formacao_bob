# 🤖 DIO Explorer — Projeto Final · Formação IBM Bob

> Projeto final da **Formação IBM Bob AI Developer** na [DIO](https://web.dio.me).
> Um agente interativo construído com **IBM Bob** que explora trilhas de aprendizado, gera desafios de código e emite certificados fictícios — usando **Slash Commands**, **Skills** e um **MCP Server customizado** em TypeScript.

---

## 📑 Índice

- [O que é o DIO Explorer](#o-que-é-o-dio-explorer)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura](#arquitetura)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Como Usar os Comandos](#como-usar-os-comandos)
  - [Slash Commands](#slash-commands)
  - [Skills](#skills)
  - [MCP Server](#mcp-server)
- [Como Executar os Testes](#como-executar-os-testes)
- [Catálogo de Trilhas](#catálogo-de-trilhas)
- [Melhorias Realizadas](#melhorias-realizadas)
- [O que Aprendi Durante o Desafio](#o-que-aprendi-durante-o-desafio)
- [Prompts Usados Durante o Desenvolvimento](#prompts-usados-durante-o-desenvolvimento)
- [Dicas e Insights para Futuros Desenvolvedores](#dicas-e-insights-para-futuros-desenvolvedores)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Autor](#autor)

---

## O que é o DIO Explorer

O **DIO Explorer** é um agente interativo construído com **IBM Bob** para a plataforma [DIO (Digital Innovation One)](https://web.dio.me). Ele permite que qualquer pessoa:

- 📚 **Explore trilhas de aprendizado** — consulte o plano de estudos completo de 30 tecnologias, com módulos, badges, lives e promoções ativas
- 🏆 **Receba desafios de código** — desafios únicos, criativos e calibrados por nível (Básico, Intermediário, Avançado) com casos de teste e code review
- 🎓 **Emita certificados fictícios** — certificados formatados em Markdown, salvos automaticamente em disco, com código de validação único

O projeto demonstra na prática o poder do IBM Bob como plataforma de desenvolvimento de agentes de IA, combinando três camadas de extensibilidade:

| Camada | Mecanismo | Onde fica |
|---|---|---|
| Comandos rápidos | Slash Commands | `.bob/commands/` |
| Comportamento enriquecido | Skills | `.bob/skills/` |
| Integração externa | MCP Server (TypeScript) | `dio_explorer/mcp/` |

Tudo isso acontece diretamente no chat do Bob, sem precisar sair do VS Code.

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

## Como Executar o Projeto

### Pré-requisitos

- [IBM Bob](https://marketplace.visualstudio.com/items?itemName=IBM.ibm-developer) instalado no VS Code
- Node.js 18+ instalado
- Python 3.8+ instalado (apenas para rodar os testes unitários)

### 1. Clone o repositório

```bash
git clone https://github.com/LuizAntonioAsevedo/projeto_final_dio_formacao_bob.git
cd projeto_final_dio_formacao_bob
```

### 2. Instale e compile o MCP Server

```bash
cd dio_explorer/mcp
npm install
npm run build
cd ../..
```

### 3. Abra no IBM Bob

Abra a pasta do projeto no VS Code com o Bob ativo. O Bob detecta automaticamente o [`.bob/mcp.json`](.bob/mcp.json) e inicia o servidor `dio-explorer` como processo filho via stdio.

> **Atenção:** O caminho no `mcp.json` aponta para o `build/index.js` com caminho absoluto. Ao clonar em outra máquina, atualize esse caminho para o seu ambiente.

---

## Como Usar os Comandos

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

## Como Executar os Testes

O projeto possui uma suíte de **90 testes unitários** escritos em Python, cobrindo os três comandos principais. Os testes validam a lógica de busca no catálogo, geração de desafios e emissão de certificados de forma completamente isolada do Bob.

### Estrutura dos testes

```
dio_explorer/tests/
├── run_tests.py          # Runner principal — executa tudo e grava relatório
├── test_trilha.py        # 30 testes — consulta de trilhas (case-insensitive, dados, promoção)
├── test_desafio.py       # 29 testes — geração de desafios (XP, tempo, campos obrigatórios)
└── test_certificado.py   # 31 testes — emissão de certificado (carga horária, código, arquivo)
```

### Como executar

Execute a partir da raiz do projeto:

```bash
python dio_explorer/tests/run_tests.py
```

O runner executa as três suítes, exibe o resultado no console e grava um relatório detalhado em:

```
dio_explorer/docs/resultado_testes.txt
```

### Resultado esperado

```
======================================================================
  DIO EXPLORER — RELATÓRIO DE TESTES UNITÁRIOS
======================================================================
  Total executados : 90
  Aprovados        : 90
  Falhas           : 0
  Taxa de aprovação: 100.0%
  Meta (≥ 70%)     : ✅ META ATINGIDA
======================================================================
```

### O que cada suíte testa

| Suíte | Testes | O que valida |
|---|---|---|
| `test_trilha.py` | 30 | Busca case-insensitive, dados do JSON (módulos, XP, badges, lives), promoção, vitalício |
| `test_desafio.py` | 29 | Nível aceito, intervalo de XP, tempo estimado, campos obrigatórios no header |
| `test_certificado.py` | 31 | Cálculo de carga horária (`módulos × 10`), formato do código de validação, salvamento do arquivo |

---

## Melhorias Realizadas

Durante o desenvolvimento do projeto, diversas melhorias foram implementadas em relação à concepção inicial:

### 1. MCP Server em TypeScript (upgrade principal)
O projeto começou apenas com Slash Commands e Skills (arquivos Markdown). A principal melhoria foi a implementação de um **MCP Server real em TypeScript**, elevando o projeto de "configuração do Bob" para "extensão do Bob via protocolo padronizado". Isso traz validação de input, lógica de negócio real e reutilização por qualquer cliente MCP.

### 2. Dual transport: stdio + HTTP
O MCP Server foi construído com suporte a **dois modos de transporte**:
- **stdio** — para uso direto pelo Bob (processo filho)
- **HTTP com Streamable HTTP transport** — para uso como API remota, exposta via `--http`

Isso vai além do requisito mínimo e permite integrar o servidor em pipelines externos, fazer testes com curl, ou colocar atrás de um proxy reverso HTTPS.

### 3. Health check endpoint
Adição de um endpoint `GET /health` no modo HTTP que retorna JSON com status, versão, número de sessões ativas e timestamp — útil para monitoramento, load balancers e probes de disponibilidade.

### 4. Cache de dados em memória
A função `getTrilhas()` usa uma variável `_cache` para evitar releituras do arquivo JSON a cada chamada de tool. Em uso intenso (múltiplas invocações em sequência), isso elimina I/O desnecessário.

### 5. Suíte de 90 testes unitários em Python
Foram criados 90 testes unitários em Python cobrindo os três comandos, com um runner que gera relatório detalhado em `resultado_testes.txt`. Isso garante que a lógica de negócio (cálculos, busca, geração de código) funciona corretamente de forma independente do Bob.

### 6. Gestão de sessões HTTP isoladas
No modo HTTP, cada cliente recebe um `sessionId` UUID único. O servidor mantém um mapa de sessões ativas e limpa automaticamente quando o cliente desconecta — prevenindo vazamento de recursos.

### 7. Documentação completa e orientada ao desenvolvedor
O README foi expandido com prompts reais usados no desenvolvimento, diagrama de arquitetura, 10 dicas práticas e seção de aprendizados — pensando em futuros desenvolvedores que usarão o projeto como referência.

---

## O que Aprendi Durante o Desafio

### Sobre o IBM Bob e agentes de IA

**O Bob é uma plataforma, não só uma ferramenta**
Comecei o projeto enxergando o Bob como um assistente de código. Ao longo do desenvolvimento, percebi que ele é uma plataforma extensível: Slash Commands e Skills são formas de "programar" o comportamento do agente sem escrever código, e o MCP Server é a forma de integrar lógica real e persistente.

**Prompt engineering é uma habilidade técnica**
A qualidade da resposta do Bob depende diretamente da qualidade do prompt. Aprendi que um bom prompt precisa: definir o formato de saída com exemplos concretos, especificar o comportamento para casos de erro, e dar ao modelo informação suficiente sem ser ambíguo. A `description` de uma skill, por exemplo, precisa ser precisa o suficiente para disparar no contexto certo e genérica o suficiente para cobrir variações naturais da linguagem.

**Skills vs Slash Commands: dois gatilhos, uma função**
A distinção entre ativar um comportamento por comando explícito (`/trilha`) versus por intenção semântica (o Bob detectando que o usuário quer uma trilha) foi um dos aprendizados mais práticos. Manter os dois mecanismos em paralelo garante uma experiência mais fluida.

### Sobre o Model Context Protocol (MCP)

**MCP é o futuro da integração de agentes**
Antes deste projeto, eu não conhecia o MCP. Aprendi que ele é um protocolo padronizado que permite qualquer agente (não só o Bob) chamar ferramentas externas de forma segura, com schemas validados e múltiplos transportes. É como uma "API para agentes de IA".

**stdio é mais simples do que parece**
O transporte stdio — onde o agente spawna o servidor como processo filho e se comunica via stdin/stdout — é elegante e funciona sem configuração de rede. Implementar os dois transportes (stdio e HTTP) no mesmo servidor foi um exercício valioso de arquitetura.

**Zod torna os schemas de tools muito mais seguros**
Usar Zod para validar os inputs das tools MCP garantiu que erros de tipo fossem capturados antes de chegar à lógica de negócio. O erro retornado pelo schema é descritivo e já indica ao cliente o que corrigir.

### Sobre desenvolvimento de software

**Separar dados, lógica e apresentação funciona em qualquer paradigma**
Mesmo num projeto "sem código" (do ponto de vista tradicional), a separação entre JSON (dados), Skills/Commands (apresentação) e MCP Server (lógica) tornou tudo mais fácil de manter e testar.

**Testes unitários têm valor mesmo em projetos de IA**
Embora a resposta final do agente seja gerada por um modelo de linguagem (não testável unitariamente), a lógica de negócio — cálculo de carga horária, geração de código de validação, busca case-insensitive — é determinística e perfeitamente testável. Criar os 90 testes Python revelou edge cases que precisaram de correção.

**A documentação é parte do produto**
Um projeto bem documentado tem mais valor do que um projeto funcional sem documentação. Escrever os prompts, as dicas e os aprendizados transformou este repositório em um recurso de referência, não só em um projeto de portfólio.

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
