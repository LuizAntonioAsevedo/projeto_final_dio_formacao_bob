"""
test_desafio.py
---------------
Testes unitários para o comando /desafio.
Cobre: validação de nível, intervalos de XP, tempo estimado,
geração de header, e consistência para a trilha Java/Intermediário.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trilha_engine import (
    validar_nivel,
    xp_para_nivel,
    tempo_para_nivel,
    gerar_header_desafio,
    buscar_trilha,
    load_trilhas,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trilhas_dio.json")


class TestValidacaoNivel(unittest.TestCase):
    """Testa a validação dos níveis aceitos pelo comando /desafio."""

    def test_nivel_basico_valido(self):
        self.assertTrue(validar_nivel("Básico"))

    def test_nivel_basico_minusculo(self):
        self.assertTrue(validar_nivel("básico"))

    def test_nivel_intermediario_valido(self):
        self.assertTrue(validar_nivel("Intermediário"))

    def test_nivel_intermediario_sem_acento(self):
        """Intermediario sem acento NÃO deve ser válido (campo exato do template)."""
        self.assertFalse(validar_nivel("Intermediario"))

    def test_nivel_avancado_valido(self):
        self.assertTrue(validar_nivel("Avançado"))

    def test_nivel_invalido(self):
        self.assertFalse(validar_nivel("Expert"))

    def test_nivel_vazio(self):
        self.assertFalse(validar_nivel(""))

    def test_nivel_numero(self):
        self.assertFalse(validar_nivel("1"))


class TestXpPorNivel(unittest.TestCase):
    """Testa os intervalos de XP retornados por nível."""

    def test_xp_basico_intervalo(self):
        xp_min, xp_max = xp_para_nivel("Básico")
        self.assertEqual(xp_min, 500)
        self.assertEqual(xp_max, 1000)

    def test_xp_intermediario_intervalo(self):
        xp_min, xp_max = xp_para_nivel("Intermediário")
        self.assertEqual(xp_min, 1500)
        self.assertEqual(xp_max, 3000)

    def test_xp_avancado_intervalo(self):
        xp_min, xp_max = xp_para_nivel("Avançado")
        self.assertEqual(xp_min, 3500)
        self.assertEqual(xp_max, 6000)

    def test_xp_nivel_invalido_retorna_zero(self):
        xp_min, xp_max = xp_para_nivel("Inexistente")
        self.assertEqual(xp_min, 0)
        self.assertEqual(xp_max, 0)

    def test_xp_case_insensitive(self):
        """A função deve aceitar a busca em minúsculas."""
        xp_min, xp_max = xp_para_nivel("básico")
        self.assertEqual(xp_min, 500)


class TestTempoPorNivel(unittest.TestCase):
    """Testa os tempos estimados retornados por nível."""

    def test_tempo_basico(self):
        tempo = tempo_para_nivel("Básico")
        self.assertIn("15", tempo)
        self.assertIn("30", tempo)

    def test_tempo_intermediario(self):
        tempo = tempo_para_nivel("Intermediário")
        self.assertIn("30", tempo)
        self.assertIn("60", tempo)

    def test_tempo_avancado(self):
        tempo = tempo_para_nivel("Avançado")
        self.assertIn("1", tempo)
        self.assertIn("3", tempo)

    def test_tempo_nivel_invalido(self):
        tempo = tempo_para_nivel("Inexistente")
        self.assertEqual(tempo, "Indefinido")


class TestGerarHeaderDesafio(unittest.TestCase):
    """Testa a geração do cabeçalho de desafio para Java/Intermediário."""

    def setUp(self):
        self.header = gerar_header_desafio("Java", "Intermediário")

    def test_header_contem_tecnologia(self):
        self.assertIn("Java", self.header)

    def test_header_contem_nivel(self):
        self.assertIn("Intermediário", self.header)

    def test_header_contem_xp(self):
        self.assertIn("XP", self.header)

    def test_header_contem_tempo(self):
        self.assertIn("Tempo estimado", self.header)

    def test_header_contem_emoji_trofeu(self):
        self.assertIn("🏆", self.header)

    def test_header_e_string(self):
        self.assertIsInstance(self.header, str)

    def test_header_nao_vazio(self):
        self.assertGreater(len(self.header), 50)

    def test_xp_dentro_do_intervalo(self):
        """O XP gerado no header deve estar dentro do intervalo para Intermediário."""
        import re
        match = re.search(r"\*\*XP ao completar:\*\* (\d+) XP", self.header)
        self.assertIsNotNone(match, "XP não encontrado no header")
        xp = int(match.group(1))
        self.assertGreaterEqual(xp, 1500)
        self.assertLessEqual(xp, 3000)


class TestDesafioComTrilhaJava(unittest.TestCase):
    """Testa integração entre /desafio e os dados da trilha Java."""

    def setUp(self):
        trilhas = load_trilhas(DATA_PATH)
        self.trilha_java = buscar_trilha(trilhas, "Java")

    def test_trilha_java_encontrada(self):
        self.assertIsNotNone(self.trilha_java)

    def test_nivel_java_e_intermediario(self):
        """A trilha Java é de nível Intermediário, compatível com desafios desse nível."""
        self.assertEqual(self.trilha_java["nivel"], "Intermediário")

    def test_desafio_intermediario_valido_para_java(self):
        nivel = self.trilha_java["nivel"]
        self.assertTrue(validar_nivel(nivel))

    def test_xp_intermediario_coerente(self):
        xp_min, xp_max = xp_para_nivel(self.trilha_java["nivel"])
        self.assertGreater(xp_max, xp_min)
        self.assertGreaterEqual(xp_min, 1000)


if __name__ == "__main__":
    unittest.main()
