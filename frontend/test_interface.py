from pathlib import Path
import unittest


ROOT = Path(__file__).parent


class InterfaceContractTestCase(unittest.TestCase):

    def setUp(self):
        self.html = (ROOT / 'index.html').read_text(
            encoding='utf-8-sig'
        )
        self.script = (ROOT / 'app.js').read_text(
            encoding='utf-8-sig'
        )
        self.css = (ROOT / 'styles.css').read_text(
            encoding='utf-8-sig'
        )

    def test_tela_apresenta_identificacao_e_linguagem(self):
        self.assertIn('Laboratório de Linguagens', self.html)
        self.assertIn('Python', self.html)
        self.assertIn('Software educacional', self.html)

    def test_tela_possui_entrada_selecao_botao_e_resultado(self):
        elementos = [
            'code-input',
            'example-select',
            'analyze-button',
            'result-area',
            'token-panel',
            'token-table-body',
            'lexical-errors',
            'ast-panel',
            'ast-tree',
            'syntax-errors'
        ]

        for elemento in elementos:
            self.assertIn(f'id="{elemento}"', self.html)

    def test_interface_envia_json_para_endpoint_de_analise(self):
        self.assertIn("fetch('/api/analyze'", self.script)
        self.assertIn("method: 'POST'", self.script)
        self.assertIn(
            "JSON.stringify({ codigo: codeInput.value })",
            self.script
        )

    def test_interface_trata_falha_de_comunicacao(self):
        self.assertIn('Falha de comunicação', self.script)
        self.assertIn(
            'Não foi possível comunicar com o servidor',
            self.script
        )

    def test_interface_renderiza_tokens_e_erros_sem_inserir_html_do_usuario(self):
        self.assertIn('mostrarAnalise', self.script)
        self.assertIn('tokenTableBody.appendChild', self.script)
        self.assertIn(
            'item.textContent = erro.mensagem',
            self.script
        )

    def test_interface_renderiza_ast_e_permite_recolher_arvore(self):
        self.assertIn('criarNoAst', self.script)
        self.assertIn('astTree.replaceChildren', self.script)
        self.assertIn('Expandir árvore', self.script)

    def test_interface_diferencia_resultados(self):
        self.assertIn('Erro na análise léxica', self.script)
        self.assertIn('Erro na análise sintática', self.script)
        self.assertIn(
            'Análises léxica e sintática concluídas',
            self.script
        )

    def test_interface_exibe_posicoes_finais_da_ast(self):
        self.assertIn('no.linhaFinal', self.script)
        self.assertIn('no.colunaFinal', self.script)

    def test_interface_exibe_regras_gramaticais(self):
        self.assertIn('atributos.regra', self.script)
        self.assertIn('ast-rule', self.script)

    def test_interface_possui_exemplos_invalidos(self):
        self.assertIn('value="erro_lexico"', self.html)
        self.assertIn('value="erro_sintatico"', self.html)

    def test_interface_possui_controle_acessivel_da_ast(self):
        self.assertIn('aria-controls="ast-tree"', self.html)
        self.assertIn('aria-expanded', self.script)

    def test_interface_possui_estilos_da_ast(self):
        self.assertIn('.ast-rule', self.css)
        self.assertIn('.ast-help', self.css)
        self.assertIn('[hidden]', self.css)


if __name__ == '__main__':
    unittest.main()
