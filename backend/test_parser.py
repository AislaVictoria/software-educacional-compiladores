import unittest

from parser import parse_tokens
from scanner import tokenize


def analisar(codigo):
    tokens, erros_lexicos = tokenize(codigo)
    ast, erros_sintaticos = parse_tokens(tokens) if not erros_lexicos else (None, [])
    return tokens, erros_lexicos, ast, erros_sintaticos


class ParserTestCase(unittest.TestCase):
    def test_atribuicao_produz_ast(self):
        _, lexicos, ast, sintaticos = analisar('resultado = 10 + 5 * 2')
        self.assertEqual(lexicos, [])
        self.assertEqual(sintaticos, [])
        self.assertEqual(ast['tipo'], 'PROGRAMA')
        expressao = ast['filhos'][0]['filhos'][0]
        self.assertEqual(expressao['tipo'], 'OPERACAO_BINARIA')
        self.assertEqual(expressao['atributos']['operador'], '+')
        self.assertEqual(expressao['filhos'][1]['atributos']['operador'], '*')

    def test_associatividade_da_subtracao(self):
        _, _, ast, erros = analisar('valor = 20 - 5 - 3')
        self.assertEqual(erros, [])
        raiz = ast['filhos'][0]['filhos'][0]
        self.assertEqual(raiz['atributos']['operador'], '-')
        self.assertEqual(raiz['filhos'][0]['atributos']['operador'], '-')

    def test_parenteses_alteram_a_estrutura(self):
        _, _, ast, erros = analisar('valor = (10 + 5) * 2')
        self.assertEqual(erros, [])
        raiz = ast['filhos'][0]['filhos'][0]
        self.assertEqual(raiz['atributos']['operador'], '*')
        self.assertEqual(raiz['filhos'][0]['tipo'], 'AGRUPAMENTO')

    def test_print_condicional_e_else(self):
        codigo = 'nota = 8\nif nota >= 6:\n    print("Aprovada")\nelse:\n    print("Reprovada")'
        _, lexicos, ast, sintaticos = analisar(codigo)
        self.assertEqual(lexicos, [])
        self.assertEqual(sintaticos, [])
        self.assertEqual([no['tipo'] for no in ast['filhos']], ['ATRIBUICAO', 'CONDICIONAL'])
        self.assertEqual(len(ast['filhos'][1]['filhos']), 3)

    def test_erro_de_expressao_incompleta(self):
        _, lexicos, ast, erros = analisar('resultado = 10 +')
        self.assertEqual(lexicos, [])
        self.assertIsNone(ast)
        self.assertEqual(len(erros), 1)
        self.assertIn('expressão', erros[0]['mensagem'])
        self.assertEqual(erros[0]['linha'], 1)

    def test_erro_de_parentese_e_localizacao(self):
        _, _, ast, erros = analisar('print(resultado')
        self.assertIsNone(ast)
        self.assertEqual(len(erros), 1)
        self.assertIn("')'", erros[0]['esperado'][0])
        self.assertEqual(erros[0]['coluna'], 16)

    def test_erro_lexico_impede_parser(self):
        tokens, lexicos, ast, erros = analisar('valor = @')
        self.assertEqual(tokens[0]['lexema'], 'valor')
        self.assertTrue(lexicos)
        self.assertIsNone(ast)
        self.assertEqual(erros, [])


if __name__ == '__main__':
    unittest.main()
