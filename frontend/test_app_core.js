const assert = require('node:assert/strict');
const test = require('node:test');
const { EXEMPLOS, validarCodigo } = require('./app-core.js');


test('disponibiliza pelo menos três exemplos relacionados ao escopo', () => {
  assert.equal(Object.keys(EXEMPLOS).length, 3);
  assert.ok(EXEMPLOS.variaveis.codigo.includes('nome'));
  assert.ok(EXEMPLOS.operadores.codigo.includes('resultado'));
  assert.ok(EXEMPLOS.condicional.codigo.includes('if'));
});

test('cada exemplo possui título, descrição e código editável', () => {
  for (const exemplo of Object.values(EXEMPLOS)) {
    assert.ok(exemplo.titulo);
    assert.ok(exemplo.descricao);
    assert.equal(typeof exemplo.codigo, 'string');
    assert.ok(exemplo.codigo.trim().length > 0);
  }
});

test('valida entrada vazia ou composta apenas por espaços', () => {
  assert.match(validarCodigo(''), /Informe um código/);
  assert.match(validarCodigo(' \n\t '), /Informe um código/);
});

test('permite código válido e caracteres especiais', () => {
  assert.equal(validarCodigo('mensagem = "Olá <Python>"'), '');
});
