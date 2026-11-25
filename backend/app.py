from flask import Flask, jsonify, request

from scanner import tokenize
from parser import parse_tokens

app = Flask(__name__)

LIMITE_CARACTERES = 10000
app.config["MAX_CONTENT_LENGTH"] = 128 * 1024


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

    if len(codigo) > LIMITE_CARACTERES:
        return jsonify({
            "success": False,
            "message": (
                f"O código excede o limite de "
                f"{LIMITE_CARACTERES} caracteres."
            )
        }), 413


    tokens, erros = tokenize(codigo)
    ast = None
    erros_sintaticos = []
    if not erros:
        ast, erros_sintaticos = parse_tokens(tokens)
    sucesso = not erros
    sucesso_geral = sucesso and not erros_sintaticos
    return jsonify({
        # "success" preserva o contrato da etapa anterior; "sucesso" é o
        # nome em português usado na documentação desta etapa.
        "success": sucesso_geral,
        "sucesso": sucesso_geral,
        "message": (
            "Análise léxica e sintática concluídas com sucesso."
            if sucesso and not erros_sintaticos else
            f"Análise léxica concluída com {len(erros)} erro(s). Confira as mensagens abaixo."
            if erros else
            f"Análise sintática concluída com {len(erros_sintaticos)} erro(s). Confira as mensagens abaixo."
        ),
        "recebido": True,
        "estatisticas": {
            "caracteres": len(codigo),
            "linhas": len(codigo.splitlines())
        },
        "tokens": tokens,
        "erros": erros,
        "lexico": {"sucesso": not erros, "tokens": tokens, "erros": erros},
        "sintatico": {"sucesso": not erros and not erros_sintaticos, "ast": ast, "erros": erros_sintaticos},
        "ast": ast,
        "erros_sintaticos": erros_sintaticos,
    }), 200


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({
        "success": False,
        "message": "A requisição excede o tamanho permitido."
    }), 413

@app.errorhandler(500)
def internal_error(_error):
    return jsonify({
        "success": False,
        "message": "Ocorreu um erro inesperado no servidor. Tente novamente."
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
