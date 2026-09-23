/**
 * tools.ts
 * Define e registra todas as tools MCP do DIO Explorer:
 *   - listar_trilhas
 *   - buscar_trilha
 *   - gerar_desafio
 *   - emitir_certificado
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { getTrilhas, buscarTrilha, type Trilha } from "./data.js";
import { writeFileSync, mkdirSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Diretório onde os certificados emitidos serão salvos
const CERT_DIR = resolve(
  __dirname,
  "..",
  "..",
  "docs",
  "certificados-emitidos"
);

// ---------------------------------------------------------------------------
// Helpers de formatação
// ---------------------------------------------------------------------------

function formatVitalicio(v: boolean): string {
  return v ? "♾️ Sim" : "📅 Não";
}

function formatPromocao(p: Trilha["promocao"]): string {
  if (p.ativa) {
    return `🔥 ${p.desconto} de desconto — válido até ${p.validade}`;
  }
  return "Sem promoção ativa no momento.";
}

function calcularCargaHoraria(modulos: number): number {
  return modulos * 10;
}

function gerarCodigoValidacao(tecnologia: string, data: Date): string {
  const anoMes = `${data.getFullYear()}${String(data.getMonth() + 1).padStart(2, "0")}`;
  const sigla = tecnologia
    .replace(/[^A-Za-z]/g, "")
    .toUpperCase()
    .slice(0, 4)
    .padEnd(4, "X");
  const digitos = String(Math.floor(Math.random() * 10000)).padStart(4, "0");
  return `DIO-${anoMes}-${sigla}-${digitos}`;
}

// ---------------------------------------------------------------------------
// Tool: listar_trilhas
// ---------------------------------------------------------------------------

export function registerListarTrilhas(server: McpServer): void {
  server.registerTool(
    "listar_trilhas",
    {
      description:
        "Lista todas as trilhas disponíveis no catálogo DIO Explorer com tecnologia, nível e XP total.",
      inputSchema: z.object({
        nivel: z
          .enum(["Básico", "Intermediário", "Avançado", "todos"])
          .optional()
          .describe(
            'Filtra por nível. Use "todos" ou omita para retornar todas.'
          ),
      }),
    },
    async ({ nivel }) => {
      let trilhas = getTrilhas();
      if (nivel && nivel !== "todos") {
        trilhas = trilhas.filter((t) => t.nivel === nivel);
      }

      const linhas = trilhas.map(
        (t) =>
          `• [${t.id}] ${t.tecnologia} — ${t.nome} | Nível: ${t.nivel} | ${t.modulos} módulos | ${t.xp_total} XP`
      );

      const texto =
        `# 📚 Catálogo DIO Explorer (${trilhas.length} trilhas)\n\n` +
        linhas.join("\n");

      return { content: [{ type: "text", text: texto }] };
    }
  );
}

// ---------------------------------------------------------------------------
// Tool: buscar_trilha
// ---------------------------------------------------------------------------

export function registerBuscarTrilha(server: McpServer): void {
  server.registerTool(
    "buscar_trilha",
    {
      description:
        "Busca uma trilha pelo nome da tecnologia e retorna o plano de estudos completo com módulos, badges, lives e promoção.",
      inputSchema: z.object({
        tecnologia: z
          .string()
          .min(1)
          .describe(
            'Nome da tecnologia (ex: "Java", "Python", "React", "IBM Bob")'
          ),
      }),
    },
    async ({ tecnologia }) => {
      const trilha = buscarTrilha(tecnologia);

      if (!trilha) {
        const disponiveis = getTrilhas()
          .map((t) => t.tecnologia)
          .join(", ");
        return {
          content: [
            {
              type: "text",
              text: `❌ Tecnologia "${tecnologia}" não encontrada.\n\nTecnologias disponíveis:\n${disponiveis}`,
            },
          ],
          isError: true,
        };
      }

      const badgesFmt = trilha.badges.map((b) => `🏅 ${b}`).join("\n");
      const livesFmt = trilha.lives_ao_vivo.map((l) => `🎥 ${l}`).join("\n");

      const texto =
        `# 📚 Plano de Estudos — ${trilha.nome}\n\n` +
        `**Tecnologia:** ${trilha.tecnologia}\n` +
        `**Nível:** ${trilha.nivel}\n` +
        `**Total de Módulos:** ${trilha.modulos}\n` +
        `**XP Total:** ${trilha.xp_total} XP\n` +
        `**Vitalício:** ${formatVitalicio(trilha.vitalicio)}\n\n` +
        `---\n\n` +
        `## 🏅 Badges Disponíveis\n${badgesFmt}\n\n` +
        `## 🎥 Lives ao Vivo\n${livesFmt}\n\n` +
        `## 🏷️ Promoção\n${formatPromocao(trilha.promocao)}\n`;

      return { content: [{ type: "text", text: texto }] };
    }
  );
}

// ---------------------------------------------------------------------------
// Tool: gerar_desafio
// ---------------------------------------------------------------------------

const XP_MAP: Record<string, [number, number]> = {
  "Básico": [500, 1000],
  "Intermediário": [1500, 3000],
  "Avançado": [3500, 6000],
};

const TEMPO_MAP: Record<string, string> = {
  "Básico": "15–30 minutos",
  "Intermediário": "30–60 minutos",
  "Avançado": "1–3 horas",
};

export function registerGerarDesafio(server: McpServer): void {
  server.registerTool(
    "gerar_desafio",
    {
      description:
        "Gera o template de um desafio de código para uma tecnologia e nível escolhidos, com XP, tempo estimado e estrutura de cases de teste.",
      inputSchema: z.object({
        tecnologia: z
          .string()
          .min(1)
          .describe('Tecnologia do desafio (ex: "Java", "Python")'),
        nivel: z
          .enum(["Básico", "Intermediário", "Avançado"])
          .describe("Nível de dificuldade do desafio"),
      }),
    },
    async ({ tecnologia, nivel }) => {
      const trilha = buscarTrilha(tecnologia);
      if (!trilha) {
        const disponiveis = getTrilhas()
          .map((t) => t.tecnologia)
          .join(", ");
        return {
          content: [
            {
              type: "text",
              text: `❌ Tecnologia "${tecnologia}" não encontrada no catálogo.\n\nDisponíveis: ${disponiveis}`,
            },
          ],
          isError: true,
        };
      }

      const [xpMin, xpMax] = XP_MAP[nivel];
      const xp = Math.floor(Math.random() * (xpMax - xpMin + 1)) + xpMin;
      const tempo = TEMPO_MAP[nivel];

      const texto =
        `# 🏆 Desafio DIO — ${tecnologia} · ${nivel}\n\n` +
        `**Dificuldade:** ${nivel}\n` +
        `**Tecnologia:** ${tecnologia}\n` +
        `**XP ao completar:** ${xp} XP\n` +
        `**Tempo estimado:** ${tempo}\n\n` +
        `---\n\n` +
        `## 📋 Enunciado\n\n` +
        `_(O agente DIO Explorer irá gerar um enunciado criativo e coerente com ${tecnologia} no nível ${nivel})_\n\n` +
        `---\n\n` +
        `## 📥 Entrada esperada\n` +
        `_(Descrever o formato e tipo de dado de entrada)_\n\n` +
        `## 📤 Saída esperada\n` +
        `_(Descrever o formato e tipo de dado de saída)_\n\n` +
        `---\n\n` +
        `## 💡 Dicas\n` +
        `- Dica 1: conceito fundamental de ${tecnologia}\n` +
        `- Dica 2: estrutura ou padrão relevante para o nível ${nivel}\n` +
        `- Dica 3: boas práticas da linguagem\n\n` +
        `---\n\n` +
        `## 🧪 Casos de Teste\n\n` +
        `| Entrada | Saída esperada |\n` +
        `|---------|----------------|\n` +
        `| caso 1  | resultado 1    |\n` +
        `| caso 2  | resultado 2    |\n` +
        `| caso 3 (edge case) | resultado 3 |\n\n` +
        `---\n\n` +
        `> 💬 Quando terminar, compartilhe sua solução e receba um code review!\n`;

      return { content: [{ type: "text", text: texto }] };
    }
  );
}

// ---------------------------------------------------------------------------
// Tool: emitir_certificado
// ---------------------------------------------------------------------------

export function registerEmitirCertificado(server: McpServer): void {
  server.registerTool(
    "emitir_certificado",
    {
      description:
        "Gera e salva um certificado fictício de conclusão de trilha para um aluno. Retorna o conteúdo Markdown do certificado e o caminho do arquivo salvo.",
      inputSchema: z.object({
        nome_aluno: z
          .string()
          .min(2)
          .describe("Nome completo do aluno (ex: Luiz Antonio)"),
        tecnologia: z
          .string()
          .min(1)
          .describe('Tecnologia da trilha concluída (ex: "Java")'),
      }),
    },
    async ({ nome_aluno, tecnologia }) => {
      const trilha = buscarTrilha(tecnologia);

      if (!trilha) {
        const disponiveis = getTrilhas()
          .map((t) => t.tecnologia)
          .join(", ");
        return {
          content: [
            {
              type: "text",
              text: `❌ Tecnologia "${tecnologia}" não encontrada.\n\nDisponíveis: ${disponiveis}`,
            },
          ],
          isError: true,
        };
      }

      const hoje = new Date();
      const carga = calcularCargaHoraria(trilha.modulos);
      const codigo = gerarCodigoValidacao(trilha.tecnologia, hoje);
      const dataFmt = hoje.toLocaleDateString("pt-BR");
      const badgesFmt = trilha.badges.map((b) => `🏅 ${b}`).join("\n");

      const conteudo =
        `# 🎓 Certificado de Conclusão\n\n` +
        `## DIO — Digital Innovation One\n\n` +
        `### Certificamos que\n\n` +
        `# ${nome_aluno}\n\n` +
        `concluiu com êxito a\n\n` +
        `## ${trilha.nome}\n\n` +
        `com carga horária de **${carga} horas**, abrangendo **${trilha.modulos} módulos**\n` +
        `e conquistando **${trilha.xp_total} XP** na plataforma DIO.\n\n` +
        `---\n\n` +
        `📅 **Data de Emissão:** ${dataFmt}\n` +
        `🔐 **Código de Validação:** ${codigo}\n` +
        `🌐 **Validar em:** https://web.dio.me/certificate/${codigo}\n\n` +
        `---\n\n` +
        `### 🏅 Badges Conquistadas\n\n${badgesFmt}\n\n` +
        `---\n\n` +
        `_Este certificado é fictício e foi gerado para fins educacionais pelo IBM Bob MCP Server._\n` +
        `_Acesse [web.dio.me](https://web.dio.me) para certificados oficiais._\n`;

      // Salva o arquivo
      const nomeLimpo = nome_aluno.replace(/\s+/g, "");
      const dataStr = hoje.toISOString().slice(0, 10).replace(/-/g, "");
      const nomeArquivo = `${nomeLimpo}_${trilha.tecnologia}_${dataStr}.md`;

      try {
        mkdirSync(CERT_DIR, { recursive: true });
        writeFileSync(resolve(CERT_DIR, nomeArquivo), conteudo, "utf-8");
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: `⚠️ Certificado gerado mas não foi possível salvar o arquivo: ${String(err)}\n\n${conteudo}`,
            },
          ],
        };
      }

      return {
        content: [
          {
            type: "text",
            text:
              conteudo +
              `\n---\n\n📁 **Arquivo salvo em:** \`docs/certificados-emitidos/${nomeArquivo}\`\n`,
          },
        ],
      };
    }
  );
}
