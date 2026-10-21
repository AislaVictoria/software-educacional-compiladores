from pathlib import Path
import unittest


ROOT = Path(__file__).parent


class InterfaceContractTestCase(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.script = (ROOT / 'app.js').read_text(encoding='utf-8')

    def test_tela_apresenta_identificacao_e_linguagem(self):
        self.assertIn('Laboratório de Linguagens', self.html)
        self.assertIn('Python', self.html)
        self.assertIn('Software educacional', self.html)

    def test_tela_possui_entrada_selecao_botao_e_resultado(self):
        for elemento in ['code-input', 'example-select', 'analyze-button', 'result-area']:
            self.assertIn(f'id="{elemento}"', self.html)

    def test_interface_envia_json_para_endpoint_de_analise(self):
        self.assertIn("fetch('/api/analyze'", self.script)
        self.assertIn("method: 'POST'", self.script)
        self.assertIn("JSON.stringify({ codigo: codeInput.value })", self.script)

    def test_interface_trata_falha_de_comunicacao(self):
        self.assertIn('Falha de comunicação', self.script)
        self.assertIn('Não foi possível comunicar com o servidor', self.script)


if __name__ == '__main__':
    unittest.main()
