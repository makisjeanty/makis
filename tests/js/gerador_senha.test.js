const test = require('node:test');
const assert = require('node:assert/strict');

const { construirCharset, gerarSenhaAPartirDeValores } = require('../../static/js/gerador_senha.js');

test('construirCharset retorna vazio quando nenhuma opção é marcada', () => {
    assert.equal(construirCharset({}), '');
    assert.equal(construirCharset(), '');
});

test('construirCharset combina apenas os conjuntos marcados', () => {
    assert.equal(construirCharset({ minusculas: true }), 'abcdefghijklmnopqrstuvwxyz');
    assert.equal(construirCharset({ numeros: true }), '0123456789');
    assert.equal(
        construirCharset({ maiusculas: true, numeros: true }),
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    );
});

test('construirCharset inclui símbolos quando marcado', () => {
    assert.equal(construirCharset({ simbolos: true }), '!@#$%^&*()_+-=[]{}|;:,.<>?');
});

test('gerarSenhaAPartirDeValores mapeia cada valor para um caractere do charset via módulo', () => {
    const charset = 'ABCD';
    // índices 0,1,2,3 e depois "dá a volta": 4 % 4 = 0, 5 % 4 = 1
    const senha = gerarSenhaAPartirDeValores(charset, [0, 1, 2, 3, 4, 5]);
    assert.equal(senha, 'ABCDAB');
});

test('gerarSenhaAPartirDeValores respeita o tamanho do array de valores, não o do charset', () => {
    const charset = 'XY';
    const senha = gerarSenhaAPartirDeValores(charset, [0, 1, 0, 1, 0]);
    assert.equal(senha.length, 5);
    assert.equal(senha, 'XYXYX');
});

test('gerarSenhaAPartirDeValores com array vazio retorna string vazia', () => {
    assert.equal(gerarSenhaAPartirDeValores('ABCD', []), '');
});
