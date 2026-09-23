#!/usr/bin/env node
/**
 * index.ts — DIO Explorer MCP Server
 * ------------------------------------
 * Suporta dois modos de transporte:
 *
 *   stdio (padrão)  → usado pelo Bob como processo filho
 *     node build/index.js
 *
 *   HTTP            → servidor HTTP local/remoto acessível via API/HTTPS
 *     node build/index.js --http [--port 3100]
 *
 * Tools expostas:
 *   • listar_trilhas    — lista o catálogo completo ou filtrado por nível
 *   • buscar_trilha     — plano de estudos de uma tecnologia (ex: Java)
 *   • gerar_desafio     — template de desafio de código por tecnologia e nível
 *   • emitir_certificado — gera e salva certificado fictício em Markdown
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { createServer, type IncomingMessage, type ServerResponse } from "http";
import { randomUUID } from "crypto";

import {
  registerListarTrilhas,
  registerBuscarTrilha,
  registerGerarDesafio,
  registerEmitirCertificado,
} from "./tools.js";

// ---------------------------------------------------------------------------
// Configuração
// ---------------------------------------------------------------------------

const SERVER_NAME = "dio-explorer-mcp";
const SERVER_VERSION = "1.0.0";
const DEFAULT_HTTP_PORT = Number(process.env.MCP_HTTP_PORT ?? 3100);

const args = process.argv.slice(2);
const useHttp = args.includes("--http");
const portArg = args.indexOf("--port");
const httpPort =
  portArg !== -1 ? Number(args[portArg + 1]) : DEFAULT_HTTP_PORT;

// ---------------------------------------------------------------------------
// Cria o servidor MCP e registra todas as tools
// ---------------------------------------------------------------------------

function createMcpServer(): McpServer {
  const server = new McpServer({
    name: SERVER_NAME,
    version: SERVER_VERSION,
  });

  registerListarTrilhas(server);
  registerBuscarTrilha(server);
  registerGerarDesafio(server);
  registerEmitirCertificado(server);

  return server;
}

// ---------------------------------------------------------------------------
// Modo stdio — usado pelo IBM Bob como processo filho
// ---------------------------------------------------------------------------

async function startStdio(): Promise<void> {
  const server = createMcpServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`[${SERVER_NAME}] running on stdio (version ${SERVER_VERSION})`);
}

// ---------------------------------------------------------------------------
// Modo HTTP — Streamable HTTP transport
// Cada requisição POST a /mcp cria uma sessão isolada.
// GET /health retorna status do servidor (útil para load balancers e HTTPS probes).
// ---------------------------------------------------------------------------

async function startHttp(): Promise<void> {
  // Mapa de sessões ativas: sessionId → transport
  const sessions = new Map<string, StreamableHTTPServerTransport>();

  const httpServer = createServer(
    async (req: IncomingMessage, res: ServerResponse) => {
      const url = new URL(req.url ?? "/", `http://${req.headers.host}`);

      // ── Health check ──────────────────────────────────────────────────────
      if (url.pathname === "/health" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(
          JSON.stringify({
            status: "ok",
            server: SERVER_NAME,
            version: SERVER_VERSION,
            sessions: sessions.size,
            timestamp: new Date().toISOString(),
          })
        );
        return;
      }

      // ── MCP endpoint ──────────────────────────────────────────────────────
      if (url.pathname === "/mcp") {
        // Inicialização de nova sessão (POST sem x-session-id)
        if (req.method === "POST") {
          const sessionId = req.headers["x-session-id"] as string | undefined;

          if (!sessionId) {
            // Nova sessão
            const newSessionId = randomUUID();
            const transport = new StreamableHTTPServerTransport({
              sessionIdGenerator: () => newSessionId,
            });

            const server = createMcpServer();
            await server.connect(transport);
            sessions.set(newSessionId, transport);

            // Limpa a sessão quando o cliente desconectar
            transport.onclose = () => {
              sessions.delete(newSessionId);
              console.error(`[${SERVER_NAME}] session closed: ${newSessionId}`);
            };

            console.error(`[${SERVER_NAME}] new session: ${newSessionId}`);
            await transport.handleRequest(req, res);
            return;
          }

          // Sessão existente
          const transport = sessions.get(sessionId);
          if (!transport) {
            res.writeHead(404, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ error: "Session not found", sessionId }));
            return;
          }
          await transport.handleRequest(req, res);
          return;
        }

        // GET — SSE stream de uma sessão existente
        if (req.method === "GET") {
          const sessionId = req.headers["x-session-id"] as string | undefined;
          if (!sessionId) {
            res.writeHead(400, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ error: "x-session-id header required" }));
            return;
          }
          const transport = sessions.get(sessionId);
          if (!transport) {
            res.writeHead(404, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ error: "Session not found", sessionId }));
            return;
          }
          await transport.handleRequest(req, res);
          return;
        }

        // DELETE — encerra sessão
        if (req.method === "DELETE") {
          const sessionId = req.headers["x-session-id"] as string | undefined;
          if (sessionId) {
            const transport = sessions.get(sessionId);
            await transport?.close();
            sessions.delete(sessionId);
          }
          res.writeHead(204);
          res.end();
          return;
        }

        res.writeHead(405, { Allow: "GET, POST, DELETE" });
        res.end("Method Not Allowed");
        return;
      }

      // ── Info / root ───────────────────────────────────────────────────────
      if (url.pathname === "/" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(
          JSON.stringify({
            name: SERVER_NAME,
            version: SERVER_VERSION,
            description: "DIO Explorer MCP Server",
            endpoints: {
              mcp: "POST /mcp  — inicia sessão MCP (Streamable HTTP)",
              health: "GET  /health — health check",
            },
            tools: [
              "listar_trilhas",
              "buscar_trilha",
              "gerar_desafio",
              "emitir_certificado",
            ],
          })
        );
        return;
      }

      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Not found", path: url.pathname }));
    }
  );

  await new Promise<void>((resolve, reject) => {
    httpServer.on("error", reject);
    httpServer.listen(httpPort, () => {
      console.error(
        `[${SERVER_NAME}] HTTP server running on http://0.0.0.0:${httpPort}`
      );
      console.error(`  MCP endpoint : POST http://localhost:${httpPort}/mcp`);
      console.error(`  Health check : GET  http://localhost:${httpPort}/health`);
      console.error(`  Info         : GET  http://localhost:${httpPort}/`);
      resolve();
    });
  });
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  if (useHttp) {
    await startHttp();
  } else {
    await startStdio();
  }
}

main().catch((err) => {
  console.error(`[${SERVER_NAME}] Fatal error:`, err);
  process.exit(1);
});
