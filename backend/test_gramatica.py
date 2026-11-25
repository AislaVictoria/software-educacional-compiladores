import unittest

from scanner import tokenize
from parser import parse_tokens


class GramaticaTestCase(unittest.TestCase):

    def analisar(self, codigo):
        tokens, erros = tokenize(codigo)
        self.assertEqual(erros, [])
        return parse_tokens(tokens)

    def verificar_valido(self, codigo):
        ast, erros = self.analisar(codigo)
        self.assertEqual(erros, [])
        self.assertIsNotNone(ast)
        return ast

    def verificar_invalido(self, codigo):
        ast, erros = self.analisar(codigo)
        self.assertIsNone(ast)
        self.assertTrue(erros)
        return erros

    def expressao(self, codigo):
        ast = self.verificar_valido(codigo)
        return ast["filhos"][0]["filhos"][0]

    def test_dois_comandos_na_mesma_linha(self):
        self.verificar_invalido("x = 1 y = 2")

    def test_expressao_sem_operador(self):
        self.verificar_invalido("x = 1 2")

    def test_if_sem_indentacao(self):
        self.verificar_invalido("if x > 0:\ny = 2")

    def test_indentacao_no_nivel_principal(self):
        self.verificar_invalido("    x = 1")

    def test_if_valido(self):
        ast = self.verificar_valido(
            "if x > 0:\n    y = 2"
        )
        self.assertEqual(
            ast["filhos"][0]["tipo"],
            "CONDICIONAL"
        )

    def test_comando_fora_do_if(self):
        ast = self.verificar_valido(
            "if x > 0:\n    y = 2\nprint(y)"
        )
        self.assertEqual(
            [no["tipo"] for no in ast["filhos"]],
            ["CONDICIONAL", "CHAMADA_FUNCAO"]
        )

    def test_comando_fora_do_if_else(self):
        codigo = (
            "if x > 0:\n"
            "    y = 2\n"
            "else:\n"
            "    y = 3\n"
            "print(y)"
        )
        ast = self.verificar_valido(codigo)
        self.assertEqual(
            [no["tipo"] for no in ast["filhos"]],
            ["CONDICIONAL", "CHAMADA_FUNCAO"]
        )

    def test_condicional_aninhado(self):
        codigo = (
            "if x > 0:\n"
            "    if y > 0:\n"
            "        z = 1\n"
            "print(z)"
        )
        ast = self.verificar_valido(codigo)
        externo = ast["filhos"][0]
        bloco = externo["filhos"][1]
        self.assertEqual(
            bloco["filhos"][0]["tipo"],
            "CONDICIONAL"
        )

    def test_else_isolado(self):
        self.verificar_invalido(
            "else:\n    x = 1"
        )

    def test_indentacao_inconsistente(self):
        self.verificar_invalido(
            "if x > 0:\n    y = 1\n      z = 2"
        )

    def test_atribuicao_em_duas_linhas(self):
        self.verificar_invalido("x =\n10")

    def test_operador_na_linha_seguinte(self):
        self.verificar_invalido("x = 10\n+ 5")

    def test_expressao_incompleta_antes_de_comando(self):
        self.verificar_invalido("x = 10 +\ny = 2")

    def test_parentese_fechado_em_outra_linha(self):
        self.verificar_invalido("x = (10 + 5\n)")

    def test_comparacao_encadeada_nao_suportada(self):
        self.verificar_invalido("x = 1 < 2 < 3")

    def test_comparacao_simples(self):
        no = self.expressao("x = 1 < 2")
        self.assertEqual(no["atributos"]["operador"], "<")

    def test_comparacoes_com_operador_logico(self):
        no = self.expressao("x = 1 < 2 and 3 < 4")
        self.assertEqual(no["atributos"]["operador"], "and")

    def test_associatividade_da_potencia(self):
        no = self.expressao("x = 2 ** 3 ** 2")
        self.assertEqual(no["atributos"]["operador"], "**")
        direita = no["filhos"][1]
        self.assertEqual(
            direita["tipo"],
            "OPERACAO_BINARIA"
        )
        self.assertEqual(
            direita["atributos"]["operador"],
            "**"
        )

    def test_precedencia_aritmetica(self):
        no = self.expressao("x = 10 + 5 * 2")
        self.assertEqual(no["atributos"]["operador"], "+")
        self.assertEqual(
            no["filhos"][1]["atributos"]["operador"],
            "*"
        )

    def test_comandos_em_linhas_separadas(self):
        ast = self.verificar_valido("x = 1\ny = 2")
        self.assertEqual(len(ast["filhos"]), 2)

    def test_literal_nulo(self):
        no = self.expressao("x = None")
        self.assertEqual(no["tipo"], "LITERAL_NULO")

    def test_literal_booleano(self):
        no = self.expressao("x = True")
        self.assertEqual(no["tipo"], "LITERAL_BOOLEANO")

    def test_agrupamento(self):
        no = self.expressao("x = (1 + 2)")
        self.assertEqual(no["tipo"], "AGRUPAMENTO")

    def test_posicao_inicial_e_final_da_operacao(self):
        no = self.expressao("x = 10 + 5 * 2")
        self.assertEqual(no["linha"], 1)
        self.assertEqual(no["coluna"], 5)
        self.assertEqual(no["linhaFinal"], 1)
        self.assertEqual(no["colunaFinal"], 14)

    def test_posicao_inicial_e_final_do_agrupamento(self):
        no = self.expressao("x = (1 + 2)")
        self.assertEqual(no["coluna"], 5)
        self.assertEqual(no["colunaFinal"], 11)

    def test_regra_gramatical_do_operador(self):
        no = self.expressao("x = 10 + 5")
        self.assertIn("soma", no["atributos"]["regra"])
        self.assertIn("+", no["atributos"]["regra"])


if __name__ == "__main__":
    unittest.main()
