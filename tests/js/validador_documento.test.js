const test = require('node:test');
const assert = require('node:assert/strict');

const {
    limparDocumento,
    validarCPF,
    validarCNPJ,
    formatarCPF,
    formatarCNPJ,
} = require('../../static/js/validador_documento.js');

test('limparDocumento remove tudo que não é dígito', () => {
    assert.equal(limparDocumento('123.456.789-09'), '12345678909');
    assert.equal(limparDocumento('11.222.333/0001-81'), '11222333000181');
});

test('validarCPF aceita um CPF válido conhecido', () => {
    assert.equal(validarCPF('11144477735'), true);
});

test('validarCPF rejeita dígito verificador incorreto', () => {
    assert.equal(validarCPF('11144477736'), false);
});

test('validarCPF rejeita todos os dígitos iguais', () => {
    assert.equal(validarCPF('11111111111'), false);
});

test('validarCPF rejeita tamanho incorreto', () => {
    assert.equal(validarCPF('123'), false);
});

test('validarCNPJ aceita um CNPJ válido conhecido', () => {
    assert.equal(validarCNPJ('11222333000181'), true);
});

test('validarCNPJ rejeita dígito verificador incorreto', () => {
    assert.equal(validarCNPJ('11222333000182'), false);
});

test('validarCNPJ rejeita todos os dígitos iguais', () => {
    assert.equal(validarCNPJ('11111111111111'), false);
});

test('validarCNPJ rejeita tamanho incorreto', () => {
    assert.equal(validarCNPJ('123'), false);
});

test('formatarCPF adiciona pontuação no padrão 000.000.000-00', () => {
    assert.equal(formatarCPF('11144477735'), '111.444.777-35');
});

test('formatarCNPJ adiciona pontuação no padrão 00.000.000/0000-00', () => {
    assert.equal(formatarCNPJ('11222333000181'), '11.222.333/0001-81');
});
