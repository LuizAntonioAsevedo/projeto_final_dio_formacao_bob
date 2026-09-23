"""
test_certificado.py
-------------------
Testes unitários para o comando /certificado.
Cobre: cálculo de carga horária, geração de código de validação,
formato do certificado, salvamento de arquivo e integração com Java.
"""

import unittest
import os
import sys
import re
import datetime
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trilha_engine import (
    load_trilhas,
    buscar_trilha,
    calcular_carga_horaria,
    gerar_codigo_validacao,
    gerar_certificado,
    nome_arquivo_certificado,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trilhas_dio.json")

# Data fixa para testes determinísticos
DATA_FIXA = datetime.date(2025, 10, 22)
NOME_ALUNO = "Luiz Antonio"
TECNOLOGIA = "Java"


class TestCalculoCargaHoraria(unittest.TestCase):
    """Testa o cálculo de carga horária (módulos × 10)."""

    def test_java_11_modulos(self):
        """Java tem 11 módulos → 110 horas."""
        self.assertEqual(calcular_carga_horaria(11), 110)

    def test_zero_modulos(self):
        self.assertEqual(calcular_carga_horaria(0), 0)

    def test_um_modulo(self):
        self.assertEqual(calcular_carga_horaria(1), 10)

    def test_15_modulos(self):
        self.assertEqual(calcular_carga_horaria(15), 150)

    def test_retorna_inteiro(self):
        resultado = calcular_carga_horaria(11)
        self.assertIsInstance(resultado, int)


class TestCodigoValidacao(unittest.TestCase):
    """Testa a geração do código de validação do certificado."""

    def setUp(self):
        self.codigo = gerar_codigo_validacao(TECNOLOGIA, DATA_FIXA)

    def test_codigo_comeca_com_dio(self):
        self.assertTrue(self.codigo.startswith("DIO-"))

    def test_codigo_formato_regex(self):
        """Formato esperado: DIO-YYYYMM-XXXX-0000"""
        padrao = r"^DIO-\d{6}-[A-Z]{4}-\d{4}$"
        self.assertRegex(self.codigo, padrao)

    def test_codigo_contem_ano_mes(self):
        self.assertIn("202510", self.codigo)

    def test_codigo_contem_sigla_java(self):
        """Os 4 primeiros caracteres alfabéticos de 'Java' são 'JAVA'."""
        self.assertIn("JAVA", self.codigo)

    def test_codigo_e_string(self):
        self.assertIsInstance(self.codigo, str)

    def test_codigo_python_sigla(self):
        codigo = gerar_codigo_validacao("Python", DATA_FIXA)
        self.assertIn("PYTH", codigo)

    def test_codigo_ibm_bob_sigla(self):
        codigo = gerar_codigo_validacao("IBM Bob", DATA_FIXA)
        # Remove não-letras → "IBMBob" → 4 primeiras → "IBMB"
        self.assertIn("IBMB", codigo)

    def test_codigos_diferentes_por_aleatoriedade(self):
        """Dois códigos gerados devem (geralmente) ter dígitos finais diferentes."""
        codigos = {gerar_codigo_validacao(TECNOLOGIA, DATA_FIXA) for _ in range(20)}
        # Com 10.000 possibilidades, é muito improvável que 20 sejam idênticos
        self.assertGreater(len(codigos), 1)


class TestGerarCertificado(unittest.TestCase):
    """Testa a geração do texto Markdown do certificado para Java."""

    def setUp(self):
        trilhas = load_trilhas(DATA_PATH)
        self.trilha_java = buscar_trilha(trilhas, TECNOLOGIA)
        self.cert = gerar_certificado(NOME_ALUNO, self.trilha_java, DATA_FIXA)

    def test_cert_contem_nome_aluno(self):
        self.assertIn(NOME_ALUNO, self.cert)

    def test_cert_contem_nome_trilha(self):
        self.assertIn("Formação Java Developer", self.cert)

    def test_cert_contem_carga_horaria(self):
        """Java: 11 módulos × 10 = 110 horas."""
        self.assertIn("110", self.cert)

    def test_cert_contem_modulos(self):
        self.assertIn("11", self.cert)

    def test_cert_contem_xp(self):
        self.assertIn("17000", self.cert)

    def test_cert_contem_data_emissao(self):
        self.assertIn("22/10/2025", self.cert)

    def test_cert_contem_codigo_validacao(self):
        self.assertIn("DIO-", self.cert)

    def test_cert_contem_url_validacao(self):
        self.assertIn("https://web.dio.me/certificate/", self.cert)

    def test_cert_contem_badges(self):
        self.assertIn("Java Starter", self.cert)
        self.assertIn("Spring Boot Developer", self.cert)
        self.assertIn("Java Expert", self.cert)

    def test_cert_contem_aviso_ficticio(self):
        self.assertIn("fictício", self.cert)

    def test_cert_e_string_nao_vazia(self):
        self.assertIsInstance(self.cert, str)
        self.assertGreater(len(self.cert), 200)


class TestNomeArquivoCertificado(unittest.TestCase):
    """Testa a geração do nome de arquivo do certificado."""

    def test_nome_sem_espacos(self):
        nome = nome_arquivo_certificado(NOME_ALUNO, TECNOLOGIA, DATA_FIXA)
        self.assertNotIn(" ", nome)

    def test_nome_contem_tecnologia(self):
        nome = nome_arquivo_certificado(NOME_ALUNO, TECNOLOGIA, DATA_FIXA)
        self.assertIn(TECNOLOGIA, nome)

    def test_nome_contem_data(self):
        nome = nome_arquivo_certificado(NOME_ALUNO, TECNOLOGIA, DATA_FIXA)
        self.assertIn("20251022", nome)

    def test_nome_termina_em_md(self):
        nome = nome_arquivo_certificado(NOME_ALUNO, TECNOLOGIA, DATA_FIXA)
        self.assertTrue(nome.endswith(".md"))

    def test_nome_formato_esperado(self):
        nome = nome_arquivo_certificado(NOME_ALUNO, TECNOLOGIA, DATA_FIXA)
        self.assertEqual(nome, "LuizAntonio_Java_20251022.md")


class TestSalvamentoCertificado(unittest.TestCase):
    """Testa que o conteúdo do certificado pode ser gravado em arquivo."""

    def test_salvar_certificado_em_arquivo_temporario(self):
        trilhas = load_trilhas(DATA_PATH)
        trilha_java = buscar_trilha(trilhas, TECNOLOGIA)
        conteudo = gerar_certificado(NOME_ALUNO, trilha_java, DATA_FIXA)

        with tempfile.TemporaryDirectory() as tmpdir:
            arquivo = os.path.join(tmpdir, nome_arquivo_certificado(NOME_ALUNO, TECNOLOGIA, DATA_FIXA))
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
            self.assertTrue(os.path.exists(arquivo))
            with open(arquivo, encoding="utf-8") as f:
                lido = f.read()
            self.assertEqual(lido, conteudo)

    def test_certificado_salvo_tem_tamanho_minimo(self):
        trilhas = load_trilhas(DATA_PATH)
        trilha_java = buscar_trilha(trilhas, TECNOLOGIA)
        conteudo = gerar_certificado(NOME_ALUNO, trilha_java, DATA_FIXA)
        self.assertGreater(len(conteudo.encode("utf-8")), 500)


if __name__ == "__main__":
    unittest.main()
