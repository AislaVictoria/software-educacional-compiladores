const assert = require('node:assert/strict');
const test = require('node:test');
const { EXEMPLOS, validarCodigo } = require('./app-core.js');

test('disponibiliza pelo menos cinco exemplos relacionados ao escopo', () => {
  assert.ok(Object.keys(EXEMPLOS).length >= 5);
  assert.ok(EXEMPLOS.variaveis.codigo.includes('nome'));
  assert.ok(EXEMPLOS.operadores.codigo.includes('resultado'));
  assert.ok(EXEMPLOS.condicional.codigo.includes('if'));
});

test('cada exemplo possui titulo, descricao e codigo editavel', () => {
  for (const exemplo of Object.values(EXEMPLOS)) {
    assert.ok(exemplo.titulo);
    assert.ok(exemplo.descricao);
    assert.equal(typeof exemplo.codigo, 'string');
    assert.ok(exemplo.codigo.trim().length > 0);
  }
});

test('valida entrada vazia ou composta apenas por espacos', () => {
  assert.match(validarCodigo(''), /Informe um código/);
  assert.match(validarCodigo(' \n\t '), /Informe um código/);
});

test('permite codigo valido e caracteres especiais', () => {
  assert.equal(validarCodigo('mensagem = "Olá <Python>"'), '');
});

test('disponibiliza exemplo de erro lexico', () => {
  assert.ok(EXEMPLOS.erro_lexico);
  assert.ok(EXEMPLOS.erro_lexico.codigo.includes('@'));
});

test('disponibiliza exemplo de erro sintatico', () => {
  assert.ok(EXEMPLOS.erro_sintatico);
  assert.ok(EXEMPLOS.erro_sintatico.codigo.endsWith('+'));
});

test('aceita exatamente 10000 caracteres', () => {
  assert.equal(validarCodigo('x'.repeat(10000)), '');
});

test('rejeita codigo acima do limite', () => {
  assert.match(
    validarCodigo('x'.repeat(10001)),
    /limite/
  );
});

test('rejeita valores que nao sejam texto', () => {
  assert.notEqual(validarCodigo(null), '');
  assert.notEqual(validarCodigo(undefined), '');
  assert.notEqual(validarCodigo(123), '');
});

test('conta caracteres Unicode corretamente', () => {
  const caractere = String.fromCodePoint(0x1F600);

  assert.equal(
    validarCodigo(caractere.repeat(10000)),
    ''
  );

  assert.match(
    validarCodigo(caractere.repeat(10001)),
    /limite/
  );
});
