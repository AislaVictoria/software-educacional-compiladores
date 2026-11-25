
import unittest

from scanner import tokenize
from parser import parse_tokens
from app import app


class RobustezTestCase(unittest.TestCase):

    def analisar(self, codigo):
        tokens, erros_lexicos = tokenize(codigo)

        if erros_lexicos:
            return None, erros_lexicos

        return parse_tokens(tokens)

    def verificar_valido(self, codigo):
        ast, erros = self.analisar(codigo)
        self.assertIsNotNone(ast)
        self.assertEqual(erros, [])

    def verificar_invalido(self, codigo):
        ast, erros = self.analisar(codigo)
        self.assertIsNone(ast)
        self.assertTrue(erros)

    def test_tabulacao_na_indentacao(self):
        self.verificar_invalido(
            "if x > 0:\n\tx = 1"
        )

    def test_tabulacao_entre_tokens(self):
        self.verificar_valido("x\t=\t1")

    def test_virgula_em_outra_linha(self):
        self.verificar_invalido("print(1\n, 2)")

    def test_print_com_varios_argumentos(self):
        self.verificar_valido("print(1, 2, 3)")

    def test_return_fora_de_funcao(self):
        self.verificar_invalido("return 10")

    def test_return_em_duas_linhas(self):
        self.verificar_invalido("return\n10")

    def test_return_dentro_de_if(self):
        self.verificar_invalido(
            "if x > 0:\n    return 10"
        )

    def test_comentario_dentro_do_bloco(self):
        self.verificar_valido(
            "if x > 0:\n    # comentario\n    x = 1"
        )

    def test_linhas_vazias(self):
        self.verificar_valido("x = 1\n\n\ny = 2")

    def test_dez_parenteses(self):
        codigo = "x = " + "(" * 10 + "1" + ")" * 10
        self.verificar_valido(codigo)

    def test_cem_parenteses(self):
        codigo = "x = " + "(" * 100 + "1" + ")" * 100
        self.verificar_invalido(codigo)

    def test_quinhentos_parenteses(self):
        codigo = "x = " + "(" * 500 + "1" + ")" * 500
        self.verificar_invalido(codigo)

    def test_quinhentas_adicoes(self):
        codigo = "x = " + " + ".join(["1"] * 500)
        self.verificar_invalido(codigo)

    def test_limite_de_tokens(self):
        self.verificar_invalido("1\n" * 2001)

    def test_string_multilinha(self):
        codigo = 'x = "abc' + chr(92) + '\ndef"'
        self.verificar_invalido(codigo)

    def test_apenas_comentarios(self):
        self.verificar_valido("# comentario")


class LimitesApiTestCase(unittest.TestCase):

    def setUp(self):
        self.cliente = app.test_client()

    def analisar(self, codigo):
        return self.cliente.post(
            "/api/analyze",
            json={"codigo": codigo}
        )

    def test_api_codigo_valido(self):
        resposta = self.analisar("x = 10 + 5")

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.get_json()["success"])

    def test_limite_de_caracteres(self):
        resposta = self.analisar("x" * 10001)

        self.assertEqual(resposta.status_code, 413)
        self.assertTrue(resposta.is_json)

    def test_limite_da_requisicao_http(self):
        resposta = self.analisar("x" * 150000)

        self.assertEqual(resposta.status_code, 413)
        self.assertTrue(resposta.is_json)

    def test_complexidade_tratada_pela_api(self):
        codigo = "x = " + "(" * 500 + "1" + ")" * 500
        resposta = self.analisar(codigo)

        self.assertEqual(resposta.status_code, 200)

        dados = resposta.get_json()

        self.assertFalse(dados["success"])
        self.assertTrue(dados["erros_sintaticos"])
        self.assertIsNone(dados["ast"])

    def test_return_rejeitado_pela_api(self):
        resposta = self.analisar("return 10")

        self.assertEqual(resposta.status_code, 200)

        dados = resposta.get_json()

        self.assertFalse(dados["success"])
        self.assertTrue(dados["erros_sintaticos"])


if __name__ == "__main__":
    unittest.main()
