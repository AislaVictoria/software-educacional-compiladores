import unittest

from scanner import Scanner, tokenize


class ScannerTestCase(unittest.TestCase):
    def test_reconhece_palavras_identificadores_numeros_e_delimitadores(self):
        tokens, erros = tokenize('if nota >= 6:\n    print("ok")')
        self.assertEqual(erros, [])
        self.assertEqual([token['tipo'] for token in tokens], [
            'PALAVRA_RESERVADA', 'IDENTIFICADOR', 'OPERADOR',
            'LITERAL_INTEIRO', 'DELIMITADOR', 'PALAVRA_RESERVADA',
            'DELIMITADOR', 'LITERAL_TEXTO', 'DELIMITADOR',
        ])
        self.assertEqual(tokens[0]['lexema'], 'if')
        self.assertEqual(tokens[0]['linha'], 1)
        self.assertEqual(tokens[0]['coluna'], 1)
        self.assertEqual(tokens[5]['linha'], 2)
        self.assertEqual(tokens[5]['coluna'], 5)

    def test_reconhece_operadores_compostos_por_maior_manchester(self):
        tokens, erros = tokenize('a == b != c <= 2 and d **= 3')
        self.assertEqual(erros, [])
        self.assertEqual([token['lexema'] for token in tokens], ['a', '==', 'b', '!=', 'c', '<=', '2', 'and', 'd', '**=', '3'])

    def test_ignora_espacos_e_comentarios(self):
        tokens, erros = tokenize('  # comentário\nnumero = 10  # fim')
        self.assertEqual(erros, [])
        self.assertEqual([token['lexema'] for token in tokens], ['numero', '=', '10'])

    def test_reconhece_reais_strings_e_escapes(self):
        tokens, erros = tokenize('nota = 8.5\ntexto = "linha\\n2"')
        self.assertEqual(erros, [])
        self.assertEqual([token['tipo'] for token in tokens], ['IDENTIFICADOR', 'OPERADOR', 'LITERAL_REAL', 'IDENTIFICADOR', 'OPERADOR', 'LITERAL_TEXTO'])

    def test_acumula_caractere_invalido_e_litera_malformado(self):
        tokens, erros = tokenize('valor = @\noutro = "sem fim')
        self.assertEqual([token['lexema'] for token in tokens], ['valor', '=', 'outro', '='])
        self.assertEqual(len(erros), 2)
        self.assertIn('@', erros[0]['mensagem'])
        self.assertEqual((erros[0]['linha'], erros[0]['coluna']), (1, 9))
        self.assertIn('não fechado', erros[1]['mensagem'])

    def test_casos_de_borda(self):
        self.assertEqual(Scanner('   # apenas comentário').scan(), ([], []))
        tokens, erros = tokenize('x=1')
        self.assertEqual(erros, [])
        self.assertEqual(tokens[-1]['lexema'], '1')


if __name__ == '__main__':
    unittest.main()
