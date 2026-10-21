import unittest

from app import app


class BackendApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_hello_world_da_primeira_etapa_continua_funcionando(self):
        response = self.client.get('/api/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Hello, World!')

    def test_healthcheck_retorna_status_ok(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'ok'})

    def test_analyze_recebe_codigo_valido(self):
        response = self.client.post('/api/analyze', json={'codigo': 'numero = 10\nprint(numero)'})
        body = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertTrue(body['recebido'])
        self.assertEqual(body['estatisticas']['linhas'], 2)

    def test_analyze_rejeita_codigo_vazio(self):
        response = self.client.post('/api/analyze', json={'codigo': '   \n  '})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.get_json()['message'], 'Informe um código-fonte antes de solicitar a análise.')

    def test_analyze_rejeita_campo_codigo_ausente(self):
        response = self.client.post('/api/analyze', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("campo 'codigo'", response.get_json()['message'])

    def test_analyze_rejeita_requisicao_sem_json(self):
        response = self.client.post('/api/analyze', data='codigo = 10')
        self.assertEqual(response.status_code, 400)
        self.assertIn('formato JSON', response.get_json()['message'])

    def test_analyze_aceita_caracteres_especiais(self):
        codigo = 'mensagem = "Olá, mundo! \n <Python>"'
        response = self.client.post('/api/analyze', json={'codigo': codigo})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['estatisticas']['caracteres'], len(codigo))


if __name__ == '__main__':
    unittest.main()
