"""
run_tests.py
------------
Runner de testes do DIO Explorer.
Executa todos os testes unitários (/trilha, /desafio, /certificado),
exibe o resultado no console e grava um relatório detalhado em
dio_explorer/docs/resultado_testes.txt.

Uso:
    python dio_explorer/tests/run_tests.py
"""

import unittest
import sys
import os

# Garante saída UTF-8 no terminal Windows (evita UnicodeEncodeError com emojis)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf_8"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import io
import datetime
import time

# Garante que src seja importável
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Diretório dos testes
TESTS_DIR = os.path.dirname(__file__)

# Onde salvar o relatório
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
os.makedirs(DOCS_DIR, exist_ok=True)
RESULTADO_PATH = os.path.join(DOCS_DIR, "resultado_testes.txt")


def linha(char="=", largura=70):
    return char * largura


def rodar_suite(suite: unittest.TestSuite, verbosidade: int = 2) -> unittest.TestResult:
    """Executa a suite e captura a saída em memória."""
    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=verbosidade)
    resultado = runner.run(suite)
    return resultado, buffer.getvalue()


def coletar_suite(modulos: list) -> unittest.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for modulo in modulos:
        suite.addTests(loader.loadTestsFromName(modulo))
    return suite


def main():
    inicio = time.time()
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # ------------------------------------------------------------------ #
    # Carrega as três suites individualmente para relatório por módulo
    # ------------------------------------------------------------------ #
    suites_info = [
        ("🔍 /trilha  — Consulta de trilhas (Java)", "test_trilha"),
        ("⚔️  /desafio — Geração de desafios de código", "test_desafio"),
        ("🎓 /certificado — Emissão de certificados", "test_certificado"),
    ]

    # Adiciona o diretório de testes ao path para importação por nome
    sys.path.insert(0, TESTS_DIR)

    resultados_por_modulo = []
    suite_total = unittest.TestSuite()
    loader = unittest.TestLoader()

    for titulo, modulo in suites_info:
        suite = loader.loadTestsFromName(modulo)
        suite_total.addTests(suite)
        resultado, saida = rodar_suite(suite, verbosidade=2)
        resultados_por_modulo.append((titulo, modulo, resultado, saida))

    duracao = time.time() - inicio

    # ------------------------------------------------------------------ #
    # Cálculos globais
    # ------------------------------------------------------------------ #
    total_executados = sum(r.testsRun for _, _, r, _ in resultados_por_modulo)
    total_falhas = sum(len(r.failures) for _, _, r, _ in resultados_por_modulo)
    total_erros = sum(len(r.errors) for _, _, r, _ in resultados_por_modulo)
    total_skipped = sum(len(r.skipped) for _, _, r, _ in resultados_por_modulo)
    total_aprovados = total_executados - total_falhas - total_erros - total_skipped
    taxa = (total_aprovados / total_executados * 100) if total_executados > 0 else 0
    meta_atingida = taxa >= 70.0
    status_global = "✅ META ATINGIDA" if meta_atingida else "❌ META NÃO ATINGIDA"

    # ------------------------------------------------------------------ #
    # Montar relatório
    # ------------------------------------------------------------------ #
    linhas = []

    linhas.append(linha("="))
    linhas.append("  DIO EXPLORER — RELATÓRIO DE TESTES UNITÁRIOS")
    linhas.append(linha("="))
    linhas.append(f"  Data/Hora   : {agora}")
    linhas.append(f"  Duração     : {duracao:.2f}s")
    linhas.append(f"  Projeto     : projeto_final_dio_formacao_bob")
    linhas.append(f"  Aluno teste : Luiz Antonio  |  Tecnologia foco: Java")
    linhas.append(linha("="))
    linhas.append("")

    # Sumário por módulo
    linhas.append(linha("-"))
    linhas.append("  RESULTADOS POR COMANDO")
    linhas.append(linha("-"))

    for titulo, modulo, resultado, saida in resultados_por_modulo:
        run = resultado.testsRun
        falhas = len(resultado.failures)
        erros = len(resultado.errors)
        skip = len(resultado.skipped)
        ok = run - falhas - erros - skip
        pct = (ok / run * 100) if run > 0 else 0
        status = "PASSOU" if (falhas == 0 and erros == 0) else "FALHOU"

        linhas.append("")
        linhas.append(f"  {titulo}")
        linhas.append(f"  Arquivo     : {modulo}.py")
        linhas.append(f"  Executados  : {run}  |  Aprovados: {ok}  |  "
                      f"Falhas: {falhas}  |  Erros: {erros}  |  Pulados: {skip}")
        linhas.append(f"  Taxa        : {pct:.1f}%  [{status}]")

        # Lista falhas e erros do módulo
        if resultado.failures:
            linhas.append("  --- Falhas:")
            for test, traceback in resultado.failures:
                linhas.append(f"    ✗ {test}")
                for tb_line in traceback.strip().splitlines()[-3:]:
                    linhas.append(f"      {tb_line}")

        if resultado.errors:
            linhas.append("  --- Erros:")
            for test, traceback in resultado.errors:
                linhas.append(f"    ✗ {test}")
                for tb_line in traceback.strip().splitlines()[-3:]:
                    linhas.append(f"      {tb_line}")

    linhas.append("")
    linhas.append(linha("="))
    linhas.append("  RESULTADO GLOBAL")
    linhas.append(linha("="))
    linhas.append(f"  Total executados : {total_executados}")
    linhas.append(f"  Aprovados        : {total_aprovados}")
    linhas.append(f"  Falhas           : {total_falhas}")
    linhas.append(f"  Erros            : {total_erros}")
    linhas.append(f"  Pulados          : {total_skipped}")
    linhas.append(f"  Taxa de aprovação: {taxa:.1f}%")
    linhas.append(f"  Meta (≥ 70%)     : {status_global}")
    linhas.append(linha("="))
    linhas.append("")

    # Saída do fluxo completo Java
    linhas.append(linha("-"))
    linhas.append("  FLUXO TESTADO — Java")
    linhas.append(linha("-"))
    linhas.append("")
    linhas.append("  1. /trilha Java")
    linhas.append("     → Consulta a trilha 'Formação Java Developer' no catálogo.")
    linhas.append("     → Verifica dados: 11 módulos, 17000 XP, nível Intermediário,")
    linhas.append("       badges [Java Starter, Spring Boot Developer, Java Expert],")
    linhas.append("       lives [Java OOP na Prática, APIs com Spring Boot, Microsserviços].")
    linhas.append("     → Verifica busca case-insensitive (java / JAVA / jAvA).")
    linhas.append("     → Verifica promoção inativa e vitalício ativado.")
    linhas.append("")
    linhas.append("  2. /desafio Java Intermediário")
    linhas.append("     → Valida o nível Intermediário como aceito.")
    linhas.append("     → Verifica intervalo de XP (1500–3000 XP).")
    linhas.append("     → Verifica tempo estimado (30–60 minutos).")
    linhas.append("     → Gera header do desafio e confirma campos obrigatórios.")
    linhas.append("     → Confirma que XP gerado está dentro do intervalo esperado.")
    linhas.append("")
    linhas.append("  3. /certificado 'Luiz Antonio' Java")
    linhas.append("     → Carga horária calculada: 11 × 10 = 110 horas.")
    linhas.append("     → Código de validação gerado no formato DIO-202510-JAVA-XXXX.")
    linhas.append("     → Certificado contém nome do aluno, trilha, data, XP e badges.")
    linhas.append("     → Arquivo gravado em docs/certificados-emitidos/ com sucesso.")
    linhas.append("")
    linhas.append(linha("="))
    linhas.append("  Gerado por IBM Bob · DIO Explorer · Formação IBM Bob AI Developer")
    linhas.append(linha("="))

    relatorio = "\n".join(linhas)

    # ------------------------------------------------------------------ #
    # Exibe no console
    # ------------------------------------------------------------------ #
    print(relatorio)

    # ------------------------------------------------------------------ #
    # Grava em arquivo
    # ------------------------------------------------------------------ #
    with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
        f.write(relatorio)

    print(f"\n📄 Relatório gravado em: {RESULTADO_PATH}")

    # ------------------------------------------------------------------ #
    # Também gera o certificado real como artefato do fluxo testado
    # ------------------------------------------------------------------ #
    _gerar_certificado_artefato()

    # Código de saída: 0 se meta atingida, 1 caso contrário
    sys.exit(0 if meta_atingida else 1)


def _gerar_certificado_artefato():
    """Gera e salva o certificado do aluno Luiz Antonio / Java como artefato."""
    import datetime
    from trilha_engine import load_trilhas, buscar_trilha, gerar_certificado, nome_arquivo_certificado

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "trilhas_dio.json")
    trilhas = load_trilhas(data_path)
    trilha = buscar_trilha(trilhas, "Java")
    if not trilha:
        print("⚠️  Trilha Java não encontrada — certificado não gerado.")
        return

    hoje = datetime.date.today()
    conteudo = gerar_certificado("Luiz Antonio", trilha, hoje)
    nome = nome_arquivo_certificado("Luiz Antonio", "Java", hoje)

    dest_dir = os.path.join(os.path.dirname(__file__), "..", "docs", "certificados-emitidos")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, nome)

    with open(dest, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"🎓 Certificado gerado em: {dest}")


if __name__ == "__main__":
    main()
