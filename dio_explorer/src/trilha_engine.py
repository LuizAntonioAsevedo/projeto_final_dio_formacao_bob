"""
trilha_engine.py
----------------
Módulo de lógica core do DIO Explorer.
Contém as funções puras usadas pelos comandos /trilha, /desafio e /certificado.
Todas as funções são testáveis de forma isolada (sem efeitos colaterais de I/O,
exceto load_trilhas que recebe o caminho como parâmetro).
"""

import json
import os
import re
import random
import datetime
from typing import Optional


# ---------------------------------------------------------------------------
# Carregamento de dados
# ---------------------------------------------------------------------------

def load_trilhas(json_path: str) -> list:
    """Carrega e retorna a lista de trilhas do arquivo JSON."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["trilhas"]


# ---------------------------------------------------------------------------
# /trilha
# ---------------------------------------------------------------------------

def buscar_trilha(trilhas: list, tecnologia: str) -> Optional[dict]:
    """
    Busca uma trilha pelo campo `tecnologia` de forma case-insensitive.
    Retorna o dict da trilha ou None se não encontrada.
    """
    termo = tecnologia.strip().lower()
    for t in trilhas:
        if t["tecnologia"].lower() == termo:
            return t
    return None


def tecnologias_disponiveis(trilhas: list) -> list:
    """Retorna a lista de tecnologias disponíveis no catálogo."""
    return [t["tecnologia"] for t in trilhas]


def formatar_vitalicio(vitalicio: bool) -> str:
    """Formata o campo vitalício conforme o template."""
    return "♾️ Sim" if vitalicio else "📅 Não"


def formatar_promocao(promocao: dict) -> str:
    """Formata o bloco de promoção conforme o template."""
    if promocao.get("ativa"):
        return f"🔥 {promocao['desconto']} de desconto — válido até {promocao['validade']}"
    return "Sem promoção ativa no momento."


def gerar_plano_estudos(trilha: dict) -> str:
    """
    Gera o texto do plano de estudos a partir dos dados da trilha.
    Retorna string Markdown formatada.
    """
    nome = trilha["nome"]
    tecnologia = trilha["tecnologia"]
    nivel = trilha["nivel"]
    modulos = trilha["modulos"]
    xp_total = trilha["xp_total"]
    badges = trilha["badges"]
    lives = trilha["lives_ao_vivo"]
    promocao = trilha["promocao"]
    vitalicio = trilha["vitalicio"]

    badges_fmt = "\n".join(f"🏅 {b}" for b in badges)
    lives_fmt = "\n".join(f"🎥 {l}" for l in lives)

    return (
        f"# 📚 Plano de Estudos — {nome}\n\n"
        f"**Tecnologia:** {tecnologia}\n"
        f"**Nível:** {nivel}\n"
        f"**Total de Módulos:** {modulos}\n"
        f"**XP Total:** {xp_total} XP\n"
        f"**Vitalício:** {formatar_vitalicio(vitalicio)}\n\n"
        f"## 🏅 Badges Disponíveis\n{badges_fmt}\n\n"
        f"## 🎥 Lives ao Vivo\n{lives_fmt}\n\n"
        f"## 🏷️ Promoção\n{formatar_promocao(promocao)}\n"
    )


# ---------------------------------------------------------------------------
# /desafio
# ---------------------------------------------------------------------------

XP_POR_NIVEL = {
    "básico": (500, 1000),
    "intermediário": (1500, 3000),
    "avançado": (3500, 6000),
}

TEMPO_POR_NIVEL = {
    "básico": "15–30 minutos",
    "intermediário": "30–60 minutos",
    "avançado": "1–3 horas",
}


def validar_nivel(nivel: str) -> bool:
    """Valida se o nível é um dos aceitos."""
    return nivel.strip().lower() in XP_POR_NIVEL


def xp_para_nivel(nivel: str) -> tuple:
    """Retorna o intervalo (min, max) de XP para o nível."""
    return XP_POR_NIVEL.get(nivel.strip().lower(), (0, 0))


def tempo_para_nivel(nivel: str) -> str:
    """Retorna o tempo estimado para o nível."""
    return TEMPO_POR_NIVEL.get(nivel.strip().lower(), "Indefinido")


def gerar_header_desafio(tecnologia: str, nivel: str) -> str:
    """Gera o cabeçalho do desafio com XP e tempo estimado."""
    xp_min, xp_max = xp_para_nivel(nivel)
    xp = random.randint(xp_min, xp_max)
    tempo = tempo_para_nivel(nivel)
    return (
        f"# 🏆 Desafio DIO — {tecnologia} · {nivel}\n\n"
        f"**Dificuldade:** {nivel}\n"
        f"**Tecnologia:** {tecnologia}\n"
        f"**XP ao completar:** {xp} XP\n"
        f"**Tempo estimado:** {tempo}\n"
    )


# ---------------------------------------------------------------------------
# /certificado
# ---------------------------------------------------------------------------

def calcular_carga_horaria(modulos: int) -> int:
    """Calcula a carga horária como módulos × 10."""
    return modulos * 10


def gerar_codigo_validacao(tecnologia: str, data: datetime.date = None) -> str:
    """
    Gera o código de validação no formato:
    DIO-{ANO}{MÊS}-{4 letras da tecnologia em maiúsculas}-{4 dígitos aleatórios}
    """
    if data is None:
        data = datetime.date.today()
    ano_mes = data.strftime("%Y%m")
    sigla = re.sub(r"[^A-Za-z]", "", tecnologia).upper()[:4].ljust(4, "X")
    digitos = f"{random.randint(0, 9999):04d}"
    return f"DIO-{ano_mes}-{sigla}-{digitos}"


def gerar_certificado(nome_aluno: str, trilha: dict, data: datetime.date = None) -> str:
    """
    Gera o texto Markdown do certificado fictício.
    """
    if data is None:
        data = datetime.date.today()

    carga = calcular_carga_horaria(trilha["modulos"])
    codigo = gerar_codigo_validacao(trilha["tecnologia"], data)
    data_fmt = data.strftime("%d/%m/%Y")
    badges_fmt = "\n".join(f"🏅 {b}" for b in trilha["badges"])

    return (
        f"# 🎓 Certificado de Conclusão\n\n"
        f"## DIO — Digital Innovation One\n\n"
        f"### Certificamos que\n\n"
        f"# {nome_aluno}\n\n"
        f"concluiu com êxito a\n\n"
        f"## {trilha['nome']}\n\n"
        f"com carga horária de **{carga} horas**, abrangendo **{trilha['modulos']} módulos**\n"
        f"e conquistando **{trilha['xp_total']} XP** na plataforma DIO.\n\n"
        f"---\n\n"
        f"📅 **Data de Emissão:** {data_fmt}\n"
        f"🔐 **Código de Validação:** {codigo}\n"
        f"🌐 **Validar em:** https://web.dio.me/certificate/{codigo}\n\n"
        f"---\n\n"
        f"### 🏅 Badges Conquistadas\n\n{badges_fmt}\n\n"
        f"---\n\n"
        f"_Este certificado é fictício e foi gerado para fins educacionais._\n"
    )


def nome_arquivo_certificado(nome_aluno: str, tecnologia: str, data: datetime.date = None) -> str:
    """Gera o nome de arquivo para o certificado."""
    if data is None:
        data = datetime.date.today()
    nome_limpo = nome_aluno.replace(" ", "")
    data_str = data.strftime("%Y%m%d")
    return f"{nome_limpo}_{tecnologia}_{data_str}.md"
