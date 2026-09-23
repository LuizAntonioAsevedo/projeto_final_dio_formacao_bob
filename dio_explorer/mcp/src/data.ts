/**
 * data.ts
 * Carrega e fornece acesso ao catálogo de trilhas do DIO Explorer.
 * Resolve o caminho do JSON de forma relativa ao próprio arquivo compilado.
 */

import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";

export interface Promocao {
  ativa: boolean;
  desconto: string | null;
  validade: string | null;
}

export interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  nivel: string;
  modulos: number;
  xp_total: number;
  badges: string[];
  promocao: Promocao;
  vitalicio: boolean;
  lives_ao_vivo: string[];
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Sobe dois níveis: build/ → mcp/ → dio_explorer/ → data/
const DATA_PATH = resolve(__dirname, "..", "..", "data", "trilhas_dio.json");

let _cache: Trilha[] | null = null;

export function getTrilhas(): Trilha[] {
  if (_cache) return _cache;
  const raw = readFileSync(DATA_PATH, "utf-8");
  const parsed = JSON.parse(raw) as { trilhas: Trilha[] };
  _cache = parsed.trilhas;
  return _cache;
}

export function buscarTrilha(tecnologia: string): Trilha | undefined {
  const termo = tecnologia.trim().toLowerCase();
  return getTrilhas().find((t) => t.tecnologia.toLowerCase() === termo);
}
