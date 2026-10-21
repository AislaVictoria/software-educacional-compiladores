const EXEMPLOS = {
  variaveis: {
    titulo: 'Variáveis e tipos básicos',
    descricao: 'Demonstra atribuição de valores numéricos, texto e booleano.',
    codigo: 'nome = "Ana"\nidade = 20\nestudante = True\nprint(nome)'
  },
  operadores: {
    titulo: 'Operações aritméticas',
    descricao: 'Demonstra operadores aritméticos e o armazenamento do resultado.',
    codigo: 'primeiro = 10\nsegundo = 5\nresultado = primeiro + segundo * 2\nprint(resultado)'
  },
  condicional: {
    titulo: 'Estrutura condicional',
    descricao: 'Demonstra uma decisão usando if e else.',
    codigo: 'nota = 8\n\nif nota >= 6:\n    situacao = "Aprovada"\nelse:\n    situacao = "Em recuperação"\n\nprint(situacao)'
  }
};

function validarCodigo(codigo) {
  if (typeof codigo !== 'string' || !codigo.trim()) {
    return 'Informe um código-fonte antes de solicitar a análise.';
  }
  return '';
}

if (typeof window !== 'undefined') {
  window.AppCore = { EXEMPLOS, validarCodigo };
}

if (typeof module !== 'undefined') {
  module.exports = { EXEMPLOS, validarCodigo };
}
