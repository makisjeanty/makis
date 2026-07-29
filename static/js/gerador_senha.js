function construirCharset({ maiusculas = false, minusculas = false, numeros = false, simbolos = false } = {}) {
    let charset = '';
    if (maiusculas) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (minusculas) charset += 'abcdefghijklmnopqrstuvwxyz';
    if (numeros) charset += '0123456789';
    if (simbolos) charset += '!@#$%^&*()_+-=[]{}|;:,.<>?';
    return charset;
}

// Separado de gerarSenha() (que usa crypto.getRandomValues, só existe no
// navegador) para que a montagem da senha a partir de números aleatórios
// já sorteados seja testável de forma determinística.
function gerarSenhaAPartirDeValores(charset, valoresAleatorios) {
    let senha = '';
    for (let i = 0; i < valoresAleatorios.length; i++) {
        senha += charset[valoresAleatorios[i] % charset.length];
    }
    return senha;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { construirCharset, gerarSenhaAPartirDeValores };
}
