"""
test_trilha.py
--------------
Testes unitários para o comando /trilha.
Cobre: busca de trilha, case-insensitive, trilha não encontrada,
formatação de plano, promoção ativa/inativa, vitalício, badges e lives.
"""

import unittest
import os
import sys

# Garante que o módulo src seja encontrado independente de onde os testes rodam
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trilha_engine import (
    load_trilhas,
    buscar_trilha,
    tecnologias_disponiveis,
    formatar_vitalicio,
    formatar_promocao,
    gerar_plano_estudos,
)

# Caminho absoluto para o JSON de dados
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trilhas_dio.json")


class TestCarregamentoDados(unittest.TestCase):
    """Testa o carregamento do arquivo JSON de trilhas."""

    def test_arquivo_existe(self):
        """O arquivo trilhas_dio.json deve existir no caminho esperado."""
        self.assertTrue(os.path.exists(DATA_PATH), f"Arquivo não encontrado: {DATA_PATH}")

    def test_load_retorna_lista(self):
        """load_trilhas deve retornar uma lista."""
        trilhas = load_trilhas(DATA_PATH)
        self.assertIsInstance(trilhas, list)

    def test_load_tem_30_trilhas(self):
        """O catálogo deve conter exatamente 30 trilhas."""
        trilhas = load_trilhas(DATA_PATH)
        self.assertEqual(len(trilhas), 30)

    def test_trilha_tem_campos_obrigatorios(self):
        """Cada trilha deve ter os campos obrigatórios do schema."""
        trilhas = load_trilhas(DATA_PATH)
        campos = {"id", "nome", "tecnologia", "nivel", "modulos", "xp_total",
                  "badges", "promocao", "vitalicio", "lives_ao_vivo"}
        for t in trilhas:
            for campo in campos:
                self.assertIn(campo, t, f"Campo '{campo}' ausente em: {t.get('nome')}")


class TestBuscaTrilha(unittest.TestCase):
    """Testa a função buscar_trilha."""

    def setUp(self):
        self.trilhas = load_trilhas(DATA_PATH)

    def test_busca_java_exato(self):
        """Deve encontrar a trilha Java com a grafia exata."""
        resultado = buscar_trilha(self.trilhas, "Java")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_busca_java_minusculo(self):
        """Busca de 'java' em minúsculas deve retornar a trilha Java."""
        resultado = buscar_trilha(self.trilhas, "java")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_busca_java_maiusculo(self):
        """Busca de 'JAVA' em maiúsculas deve retornar a trilha Java."""
        resultado = buscar_trilha(self.trilhas, "JAVA")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["tecnologia"], "Java")

    def test_busca_java_misto(self):
        """Busca de 'jAvA' deve retornar a trilha Java."""
        resultado = buscar_trilha(self.trilhas, "jAvA")
        self.assertIsNotNone(resultado)

    def test_busca_tecnologia_inexistente(self):
        """Tecnologia inexistente deve retornar None."""
        resultado = buscar_trilha(self.trilhas, "COBOL")
        self.assertIsNone(resultado)

    def test_busca_string_vazia(self):
        """String vazia não deve bater em nenhuma trilha."""
        resultado = buscar_trilha(self.trilhas, "")
        self.assertIsNone(resultado)

    def test_dados_java_corretos(self):
        """Os dados da trilha Java devem corresponder ao JSON."""
        trilha = buscar_trilha(self.trilhas, "Java")
        self.assertEqual(trilha["id"], 14)
        self.assertEqual(trilha["nome"], "Formação Java Developer")
        self.assertEqual(trilha["nivel"], "Intermediário")
        self.assertEqual(trilha["modulos"], 11)
        self.assertEqual(trilha["xp_total"], 17000)
        self.assertFalse(trilha["promocao"]["ativa"])
        self.assertTrue(trilha["vitalicio"])


class TestTecnologiasDisponiveis(unittest.TestCase):
    """Testa a função tecnologias_disponiveis."""

    def setUp(self):
        self.trilhas = load_trilhas(DATA_PATH)

    def test_retorna_lista(self):
        techs = tecnologias_disponiveis(self.trilhas)
        self.assertIsInstance(techs, list)

    def test_java_esta_na_lista(self):
        techs = tecnologias_disponiveis(self.trilhas)
        self.assertIn("Java", techs)

    def test_quantidade_igual_ao_catalogo(self):
        techs = tecnologias_disponiveis(self.trilhas)
        self.assertEqual(len(techs), 30)


class TestFormatadores(unittest.TestCase):
    """Testa as funções de formatação de texto."""

    def test_vitalicio_true(self):
        self.assertEqual(formatar_vitalicio(True), "♾️ Sim")

    def test_vitalicio_false(self):
        self.assertEqual(formatar_vitalicio(False), "📅 Não")

    def test_promocao_ativa(self):
        promo = {"ativa": True, "desconto": "30%", "validade": "2025-12-31"}
        resultado = formatar_promocao(promo)
        self.assertIn("30%", resultado)
        self.assertIn("2025-12-31", resultado)
        self.assertIn("🔥", resultado)

    def test_promocao_inativa(self):
        promo = {"ativa": False, "desconto": None, "validade": None}
        resultado = formatar_promocao(promo)
        self.assertIn("Sem promoção", resultado)

    def test_promocao_java_inativa(self):
        """A trilha Java não tem promoção ativa."""
        trilhas = load_trilhas(DATA_PATH)
        trilha = buscar_trilha(trilhas, "Java")
        resultado = formatar_promocao(trilha["promocao"])
        self.assertIn("Sem promoção", resultado)


class TestGerarPlanoEstudos(unittest.TestCase):
    """Testa a geração do plano de estudos para Java."""

    def setUp(self):
        trilhas = load_trilhas(DATA_PATH)
        self.trilha_java = buscar_trilha(trilhas, "Java")
        self.plano = gerar_plano_estudos(self.trilha_java)

    def test_plano_contem_nome_trilha(self):
        self.assertIn("Formação Java Developer", self.plano)

    def test_plano_contem_tecnologia(self):
        self.assertIn("Java", self.plano)

    def test_plano_contem_nivel(self):
        self.assertIn("Intermediário", self.plano)

    def test_plano_contem_modulos(self):
        self.assertIn("11", self.plano)

    def test_plano_contem_xp(self):
        self.assertIn("17000", self.plano)

    def test_plano_contem_badges(self):
        self.assertIn("Java Starter", self.plano)
        self.assertIn("Spring Boot Developer", self.plano)
        self.assertIn("Java Expert", self.plano)

    def test_plano_contem_lives(self):
        self.assertIn("Java OOP na Prática", self.plano)

    def test_plano_contem_sem_promocao(self):
        self.assertIn("Sem promoção", self.plano)

    def test_plano_contem_vitalicio(self):
        self.assertIn("♾️ Sim", self.plano)

    def test_plano_e_string(self):
        self.assertIsInstance(self.plano, str)

    def test_plano_nao_vazio(self):
        self.assertGreater(len(self.plano), 100)


if __name__ == "__main__":
    unittest.main()
