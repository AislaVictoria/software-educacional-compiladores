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
  },

  erro_lexico: {
    titulo: 'Exemplo com erro léxico',
    descricao: 'Demonstra um caractere não reconhecido pelo scanner.',
    codigo: 'numero = 10 @ 2\nprint(numero)'
  },

  erro_sintatico: {
    titulo: 'Exemplo com erro sintático',
    descricao: 'Demonstra uma expressão aritmética incompleta.',
    codigo: 'resultado = 10 +'
  }
};

function validarCodigo(codigo) {
  if (typeof codigo !== 'string' || !codigo.trim()) {
    return 'Informe um código-fonte antes de solicitar a análise.';
  }

  if (Array.from(codigo).length > 10000) {
    return 'O código excede o limite de 10000 caracteres.';
  }

  return '';
}

if (typeof window !== 'undefined') {
  window.AppCore = { EXEMPLOS, validarCodigo };
}

if (typeof module !== 'undefined') {
  module.exports = { EXEMPLOS, validarCodigo };
}
