from flask import Flask, jsonify, request

from scanner import tokenize

app = Flask(__name__)


@app.get("/api/hello")
def hello():
    return jsonify({
        "message": "Hello, World!",
        "project": "Analisador Educacional de Linguagens"
    })


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/analyze")
def analyze():
    """Tokeniza o código e retorna tokens e erros léxicos didáticos."""
    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "A requisição precisa enviar dados no formato JSON."
        }), 400

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "message": "O corpo da requisição deve ser um objeto JSON."
        }), 400

    codigo = payload.get("codigo")
    if not isinstance(codigo, str):
        return jsonify({
            "success": False,
            "message": "O campo 'codigo' é obrigatório e deve ser um texto."
        }), 400

    if not codigo.strip():
        return jsonify({
            "success": False,
            "message": "Informe um código-fonte antes de solicitar a análise."
        }), 422

    tokens, erros = tokenize(codigo)
    sucesso = not erros
    return jsonify({
        # "success" preserva o contrato da etapa anterior; "sucesso" é o
        # nome em português usado na documentação desta etapa.
        "success": sucesso,
        "sucesso": sucesso,
        "message": (
            "Análise léxica concluída: todos os lexemas foram reconhecidos."
            if sucesso else
            f"Análise léxica concluída com {len(erros)} erro(s). Confira as mensagens abaixo."
        ),
        "recebido": True,
        "estatisticas": {
            "caracteres": len(codigo),
            "linhas": len(codigo.splitlines())
        },
        "tokens": tokens,
        "erros": erros,
    }), 200


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({
        "success": False,
        "message": "Ocorreu um erro inesperado no servidor. Tente novamente."
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
