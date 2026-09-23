# DIO Explorer — MCP Server

Servidor MCP do projeto **DIO Explorer**, construído com **TypeScript + Node.js** usando o [Model Context Protocol SDK](https://github.com/modelcontextprotocol/typescript-sdk).

Expõe as funcionalidades do DIO Explorer como **tools MCP**, permitindo que o IBM Bob (e qualquer cliente MCP) consulte trilhas, gere desafios e emita certificados diretamente via protocolo padronizado.

---

## 🛠️ Tools disponíveis

| Tool | Descrição |
|---|---|
| `listar_trilhas` | Lista o catálogo completo (30 trilhas) ou filtrado por nível |
| `buscar_trilha` | Retorna o plano de estudos completo de uma tecnologia (ex: Java) |
| `gerar_desafio` | Gera o template de desafio de código por tecnologia e nível |
| `emitir_certificado` | Gera e salva certificado fictício de conclusão em Markdown |

---

## 🚀 Modos de transporte

### stdio (padrão — usado pelo IBM Bob)
O Bob spawna o servidor como processo filho via `mcp.json`:
```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": ["<caminho>/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

### HTTP (acesso remoto via API/HTTPS)
Sobe um servidor HTTP com **Streamable HTTP transport** na porta `3100` (configurável):
```bash
node build/index.js --http
node build/index.js --http --port 8080
```

**Endpoints disponíveis:**

| Método | Path | Descrição |
|---|---|---|
| `GET` | `/` | Info do servidor e tools disponíveis |
| `POST` | `/mcp` | Inicia sessão MCP (sem `x-session-id`) |
| `POST` | `/mcp` | Envia mensagem MCP (com `x-session-id`) |
| `GET` | `/mcp` | SSE stream da sessão (com `x-session-id`) |
| `DELETE` | `/mcp` | Encerra a sessão |
| `GET` | `/health` | Health check (JSON) |

#### Exemplo de uso via HTTP (curl)
```bash
# Info
curl http://localhost:3100/

# Health check
curl http://localhost:3100/health
```

#### Atrás de HTTPS (nginx / Cloudflare / ngrok)
O servidor HTTP pode ser colocado atrás de um proxy reverso com TLS:
```bash
# Exemplo com ngrok (túnel HTTPS temporário para testes)
ngrok http 3100
```
A URL gerada pelo ngrok pode ser registrada como servidor MCP remoto:
```json
{
  "mcpServers": {
    "dio-explorer-remote": {
      "url": "https://<seu-subdominio>.ngrok.io/mcp"
    }
  }
}
```

---

## 📦 Estrutura

```
dio_explorer/mcp/
├── src/
│   ├── index.ts      # Entry point — stdio e HTTP transport
│   ├── tools.ts      # Registro das 4 tools MCP
│   └── data.ts       # Acesso ao catálogo trilhas_dio.json
├── build/            # Saída compilada (TypeScript → JavaScript)
│   ├── index.js
│   ├── tools.js
│   └── data.js
├── package.json
└── tsconfig.json
```

---

## 🔧 Desenvolvimento

```bash
# Instalar dependências
npm install

# Compilar
npm run build

# Rodar em modo stdio (para Bob)
npm run start:stdio

# Rodar em modo HTTP
npm run start:http

# Compilar em modo watch
npm run dev
```

### Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `MCP_HTTP_PORT` | `3100` | Porta do servidor HTTP |

---

## 🔒 Segurança e acesso remoto

- O servidor **não exige autenticação** por padrão — adequado para uso local ou em redes fechadas.
- Para expor publicamente, adicione um proxy reverso (nginx, Caddy) com **TLS + autenticação** (API key no header ou OAuth).
- O endpoint `/health` pode ser usado por load balancers e probes de HTTPS.
- Cada sessão HTTP é isolada por `x-session-id` (UUID v4 gerado automaticamente).

---

## 📋 Exemplo de invocação no Bob

Após registrar o servidor no `mcp.json`, use no chat do Bob:

```
Liste todas as trilhas disponíveis
Busque a trilha de Java
Gere um desafio de Python no nível Intermediário
Emita um certificado para "Maria Silva" na trilha Java
```

O Bob chamará automaticamente as tools MCP correspondentes.
