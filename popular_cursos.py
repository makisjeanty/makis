import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cursos.models import Curso, Modulo, Licao, Etapa

# -----------------------------------------------------------------------------
# Curso 1: Python para Iniciantes
# -----------------------------------------------------------------------------
curso_python, _ = Curso.objects.get_or_create(
    slug='python-para-iniciantes',
    defaults={
        'titulo': 'Python para Iniciantes',
        'descricao': 'Aprenda noções básicas de lógica de programação, variáveis e estruturas de dados com desafios interativos.',
        'icone': '🐍',
        'nivel': 'iniciante',
        'ordem': 1,
        'ativo': True,
    }
)

mod1_python, _ = Modulo.objects.get_or_create(
    curso=curso_python,
    ordem=1,
    defaults={'titulo': '1. Noções Básicas de Python'}
)

licao1_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=1,
    defaults={'titulo': 'Para que servem as variáveis?', 'duracao_minutos': 5}
)

licao2_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=2,
    defaults={'titulo': 'Tipos de Dados em Python', 'duracao_minutos': 7}
)

licao3_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=3,
    defaults={'titulo': 'Estruturas Condicionais (if/else)', 'duracao_minutos': 10}
)

# Etapas da Lição 1
Etapa.objects.get_or_create(
    licao=licao1_python,
    ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Python é uma linguagem de programação fantástica',
        'conteudo': 'É a linguagem escolhida por muitas empresas e uma escolha popular para projetos pessoais. Você pode usá-la para automatizar tarefas, análise de dados e IA!',
    }
)

Etapa.objects.get_or_create(
    licao=licao1_python,
    ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Para que os computadores usam variáveis?',
        'opcoes_json': ['Para armazenar informações para uso posterior', 'Para exibir informações na tela'],
        'resposta_correta': 'Para armazenar informações para uso posterior',
    }
)

Etapa.objects.get_or_create(
    licao=licao1_python,
    ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Criando uma Variável',
        'conteudo': 'Para criar uma variável, começamos digitando seu nome. Os nomes não podem conter espaços.',
        'opcoes_json': ['home city', 'city'],
        'resposta_correta': 'city',
        'nome_arquivo': 'script.py',
    }
)

# Etapas da Lição 2
Etapa.objects.get_or_create(
    licao=licao2_python,
    ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Python guarda tipos diferentes de informação',
        'conteudo': 'Os tipos mais comuns são: int (números inteiros, como 10), float (números com casas decimais, como 3.14), str (texto, como "olá") e bool (verdadeiro ou falso).',
    }
)

Etapa.objects.get_or_create(
    licao=licao2_python,
    ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual tipo de dado representa números com casas decimais, como 9.99?',
        'opcoes_json': ['int', 'float', 'str', 'bool'],
        'resposta_correta': 'float',
    }
)

Etapa.objects.get_or_create(
    licao=licao2_python,
    ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Guardando um Nome',
        'conteudo': 'Nomes de pessoas são texto, então precisam ficar entre aspas. Qual das opções guarda corretamente o nome "Maria" na variável nome?',
        'opcoes_json': ['nome = Maria', 'nome = "Maria"'],
        'resposta_correta': 'nome = "Maria"',
        'nome_arquivo': 'script.py',
    }
)

# Etapas da Lição 3
Etapa.objects.get_or_create(
    licao=licao3_python,
    ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Tomando decisões com if/else',
        'conteudo': 'O "if" testa uma condição: se ela for verdadeira, o bloco dentro dele roda. Se for falsa e existir um "else", o bloco do "else" roda no lugar.',
    }
)

Etapa.objects.get_or_create(
    licao=licao3_python,
    ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'O que acontece se a condição do "if" for falsa e existir um "else"?',
        'opcoes_json': ['O bloco do else é executado', 'Nada acontece', 'O programa trava'],
        'resposta_correta': 'O bloco do else é executado',
    }
)

Etapa.objects.get_or_create(
    licao=licao3_python,
    ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Comparando Valores',
        'conteudo': 'Para comparar se duas coisas são iguais dentro de um "if", usamos "==" (dois sinais de igual), não "=". Qual linha está correta?',
        'opcoes_json': ['if idade = 18:', 'if idade == 18:'],
        'resposta_correta': 'if idade == 18:',
        'nome_arquivo': 'script.py',
    }
)

licao4_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=4,
    defaults={'titulo': 'Verdadeiro e Falso: Booleanos', 'duracao_minutos': 5}
)

licao5_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=5,
    defaults={'titulo': 'Tipos de Comparação', 'duracao_minutos': 6}
)

licao6_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=6,
    defaults={'titulo': 'Verificando Igualdade de Números', 'duracao_minutos': 5}
)

licao7_python, _ = Licao.objects.get_or_create(
    modulo=mod1_python,
    ordem=7,
    defaults={'titulo': 'Formatando Strings', 'duracao_minutos': 6}
)

# Etapas da Lição 4
Etapa.objects.get_or_create(
    licao=licao4_python, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'O tipo que só tem dois valores possíveis',
        'conteudo': 'O tipo bool só existe com dois valores: True (verdadeiro) ou False (falso), sempre com a primeira letra maiúscula. Toda comparação em Python (como 5 > 3) resulta num desses dois valores.',
    }
)
Etapa.objects.get_or_create(
    licao=licao4_python, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual desses é um valor booleano válido em Python?',
        'opcoes_json': ['Verdadeiro', 'True', '"true"'],
        'resposta_correta': 'True',
    }
)
Etapa.objects.get_or_create(
    licao=licao4_python, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Testando um Valor Booleano',
        'conteudo': 'Qual linha guarda corretamente o valor verdadeiro na variável "ativo"?',
        'opcoes_json': ['ativo = true', 'ativo = True'],
        'resposta_correta': 'ativo = True',
        'nome_arquivo': 'script.py',
    }
)

# Etapas da Lição 5
Etapa.objects.get_or_create(
    licao=licao5_python, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Comparando valores entre si',
        'conteudo': 'Python tem seis operadores de comparação, todos resultando em True ou False: == (igual), != (diferente), > (maior), < (menor), >= (maior ou igual) e <= (menor ou igual).',
    }
)
Etapa.objects.get_or_create(
    licao=licao5_python, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual operador verifica se dois valores são diferentes?',
        'opcoes_json': ['==', '!=', '<>'],
        'resposta_correta': '!=',
    }
)
Etapa.objects.get_or_create(
    licao=licao5_python, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Comparando Idades',
        'conteudo': "Qual expressão verifica corretamente se 'idade' é maior ou igual a 18?",
        'opcoes_json': ['idade => 18', 'idade >= 18'],
        'resposta_correta': 'idade >= 18',
        'nome_arquivo': 'script.py',
    }
)

# Etapas da Lição 6
Etapa.objects.get_or_create(
    licao=licao6_python, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': '== compara, = atribui',
        'conteudo': 'Um erro muito comum é confundir "=" (atribuição, guarda um valor) com "==" (comparação, pergunta se dois valores são iguais). "5 == 5" retorna True; "x = 5" apenas guarda o número 5 em x.',
    }
)
Etapa.objects.get_or_create(
    licao=licao6_python, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'O que a expressão "5 == 5" retorna?',
        'opcoes_json': ['True', 'False', '5'],
        'resposta_correta': 'True',
    }
)
Etapa.objects.get_or_create(
    licao=licao6_python, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Comparando Duas Notas',
        'conteudo': "Qual linha verifica corretamente se a variável 'nota' é igual a 10?",
        'opcoes_json': ['if nota = 10:', 'if nota == 10:'],
        'resposta_correta': 'if nota == 10:',
        'nome_arquivo': 'script.py',
    }
)

# Etapas da Lição 7
Etapa.objects.get_or_create(
    licao=licao7_python, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Inserindo variáveis dentro de um texto',
        'conteudo': 'Uma f-string começa com "f" antes das aspas e permite inserir variáveis direto no texto usando chaves, como f"Você tem {idade} anos" — sem precisar concatenar pedaços de texto com "+".',
    }
)
Etapa.objects.get_or_create(
    licao=licao7_python, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual das opções abaixo é uma f-string válida?',
        'opcoes_json': ['"Olá, {nome}"', 'f"Olá, {nome}"'],
        'resposta_correta': 'f"Olá, {nome}"',
    }
)
Etapa.objects.get_or_create(
    licao=licao7_python, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Montando uma Mensagem',
        'conteudo': 'Com idade = 20, qual código imprime corretamente "Você tem 20 anos"?',
        'opcoes_json': ['print("Você tem" + idade + "anos")', 'print(f"Você tem {idade} anos")'],
        'resposta_correta': 'print(f"Você tem {idade} anos")',
        'nome_arquivo': 'script.py',
    }
)

# -----------------------------------------------------------------------------
# Módulo 2: Laços de Repetição
# -----------------------------------------------------------------------------
mod2_python, _ = Modulo.objects.get_or_create(
    curso=curso_python,
    ordem=2,
    defaults={'titulo': '2. Laços de Repetição'}
)

licao1_mod2, _ = Licao.objects.get_or_create(
    modulo=mod2_python,
    ordem=1,
    defaults={'titulo': 'O Laço For', 'duracao_minutos': 7}
)

licao2_mod2, _ = Licao.objects.get_or_create(
    modulo=mod2_python,
    ordem=2,
    defaults={'titulo': 'O Laço While', 'duracao_minutos': 7}
)

licao3_mod2, _ = Licao.objects.get_or_create(
    modulo=mod2_python,
    ordem=3,
    defaults={'titulo': 'Break e Continue', 'duracao_minutos': 6}
)

Etapa.objects.get_or_create(
    licao=licao1_mod2, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Repetindo ações com o for',
        'conteudo': 'O laço "for" percorre uma sequência de valores e repete um bloco de código para cada um deles. "for i in range(5):" repete o bloco 5 vezes, com i valendo 0, 1, 2, 3 e 4.',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod2, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'O que a função range(5) gera?',
        'opcoes_json': ['Os números de 1 a 5', 'Os números de 0 a 4', 'Um texto com 5 caracteres'],
        'resposta_correta': 'Os números de 0 a 4',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod2, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Repetindo uma Ação',
        'conteudo': 'Qual linha imprime os números de 0 a 4, um por vez?',
        'opcoes_json': ['for i in range(5) print(i)', 'for i in range(5): print(i)'],
        'resposta_correta': 'for i in range(5): print(i)',
        'nome_arquivo': 'script.py',
    }
)

Etapa.objects.get_or_create(
    licao=licao2_mod2, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Repetindo enquanto uma condição for verdadeira',
        'conteudo': 'O laço "while" repete um bloco de código enquanto sua condição continuar verdadeira. Se a condição nunca se tornar falsa, o programa entra em um loop infinito.',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod2, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': "Quando um laço 'while' para de executar?",
        'opcoes_json': ['Quando a condição se torna falsa', 'Depois de exatamente 10 repetições', 'Nunca para sozinho'],
        'resposta_correta': 'Quando a condição se torna falsa',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod2, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Evitando Loop Infinito',
        'conteudo': 'Dentro do laço, qual linha atualiza o contador para que o "while" eventualmente pare?',
        'opcoes_json': ['contador = contador', 'contador += 1'],
        'resposta_correta': 'contador += 1',
        'nome_arquivo': 'script.py',
    }
)

Etapa.objects.get_or_create(
    licao=licao3_mod2, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Controlando o laço com break e continue',
        'conteudo': '"break" encerra o laço imediatamente, mesmo que a condição ainda seja verdadeira. "continue" pula o restante da repetição atual e vai direto para a próxima.',
    }
)
Etapa.objects.get_or_create(
    licao=licao3_mod2, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': "O que o comando 'break' faz dentro de um laço?",
        'opcoes_json': ['Encerra o laço imediatamente', 'Pula para a próxima repetição', 'Reinicia o laço do zero'],
        'resposta_correta': 'Encerra o laço imediatamente',
    }
)
Etapa.objects.get_or_create(
    licao=licao3_mod2, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Parando no Momento Certo',
        'conteudo': 'Qual comando usamos para sair do laço assim que encontrarmos o número 7 numa lista?',
        'opcoes_json': ['continue', 'break'],
        'resposta_correta': 'break',
        'nome_arquivo': 'script.py',
    }
)

# -----------------------------------------------------------------------------
# Módulo 3: Estruturas de Dados
# -----------------------------------------------------------------------------
mod3_python, _ = Modulo.objects.get_or_create(
    curso=curso_python,
    ordem=3,
    defaults={'titulo': '3. Estruturas de Dados'}
)

licao1_mod3, _ = Licao.objects.get_or_create(
    modulo=mod3_python,
    ordem=1,
    defaults={'titulo': 'Listas', 'duracao_minutos': 8}
)

licao2_mod3, _ = Licao.objects.get_or_create(
    modulo=mod3_python,
    ordem=2,
    defaults={'titulo': 'Dicionários', 'duracao_minutos': 8}
)

licao3_mod3, _ = Licao.objects.get_or_create(
    modulo=mod3_python,
    ordem=3,
    defaults={'titulo': 'Tuplas', 'duracao_minutos': 6}
)

Etapa.objects.get_or_create(
    licao=licao1_mod3, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Guardando vários valores numa lista',
        'conteudo': 'Uma lista guarda vários valores em ordem, como "frutas = [\'maçã\', \'banana\', \'uva\']". Cada item tem uma posição (índice), começando em 0.',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod3, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': "Como acessamos o primeiro item de uma lista chamada 'frutas'?",
        'opcoes_json': ['frutas[1]', 'frutas[0]', 'frutas(0)'],
        'resposta_correta': 'frutas[0]',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod3, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Adicionando Itens',
        'conteudo': 'Qual método adiciona um novo item ao final de uma lista?',
        'opcoes_json': ['frutas.add("maçã")', 'frutas.append("maçã")'],
        'resposta_correta': 'frutas.append("maçã")',
        'nome_arquivo': 'script.py',
    }
)

Etapa.objects.get_or_create(
    licao=licao2_mod3, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Guardando pares de chave e valor',
        'conteudo': 'Um dicionário guarda valores associados a uma chave, como "pessoa = {\'nome\': \'Ana\', \'idade\': 30}". Em vez de posição numérica, acessamos os valores pela chave.',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod3, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': "Como acessamos o valor associado à chave 'nome' num dicionário chamado 'pessoa'?",
        'opcoes_json': ["pessoa['nome']", 'pessoa.nome', 'pessoa[0]'],
        'resposta_correta': "pessoa['nome']",
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod3, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Criando um Dicionário',
        'conteudo': "Qual sintaxe cria corretamente um dicionário com a chave 'cor' e valor 'azul'?",
        'opcoes_json': ["['cor', 'azul']", "{'cor': 'azul'}"],
        'resposta_correta': "{'cor': 'azul'}",
        'nome_arquivo': 'script.py',
    }
)

Etapa.objects.get_or_create(
    licao=licao3_mod3, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Listas que não podem ser alteradas',
        'conteudo': 'Uma tupla é parecida com uma lista, mas depois de criada não pode ser modificada. Usamos parênteses em vez de colchetes: "coordenadas = (10, 20)".',
    }
)
Etapa.objects.get_or_create(
    licao=licao3_mod3, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual a principal diferença entre uma lista e uma tupla?',
        'opcoes_json': ['A tupla não pode ser alterada depois de criada', 'A tupla só guarda números', 'Não existe diferença'],
        'resposta_correta': 'A tupla não pode ser alterada depois de criada',
    }
)
Etapa.objects.get_or_create(
    licao=licao3_mod3, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Identificando uma Tupla',
        'conteudo': 'Qual das opções abaixo cria uma tupla?',
        'opcoes_json': ['coordenadas = [10, 20]', 'coordenadas = (10, 20)'],
        'resposta_correta': 'coordenadas = (10, 20)',
        'nome_arquivo': 'script.py',
    }
)

# -----------------------------------------------------------------------------
# Módulo 4: Funções
# -----------------------------------------------------------------------------
mod4_python, _ = Modulo.objects.get_or_create(
    curso=curso_python,
    ordem=4,
    defaults={'titulo': '4. Funções'}
)

licao1_mod4, _ = Licao.objects.get_or_create(
    modulo=mod4_python,
    ordem=1,
    defaults={'titulo': 'Criando Funções', 'duracao_minutos': 7}
)

licao2_mod4, _ = Licao.objects.get_or_create(
    modulo=mod4_python,
    ordem=2,
    defaults={'titulo': 'Parâmetros e Retorno', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(
    licao=licao1_mod4, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Empacotando código reutilizável',
        'conteudo': 'Uma função agrupa um bloco de código que pode ser reutilizado sempre que precisarmos. Criamos uma com "def nome_da_funcao():" e a executamos escrevendo seu nome seguido de parênteses.',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod4, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual palavra-chave usamos para criar uma função em Python?',
        'opcoes_json': ['function', 'def', 'func'],
        'resposta_correta': 'def',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod4, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Chamando uma Função',
        'conteudo': "Como chamamos (executamos) uma função já criada chamada 'saudacao'?",
        'opcoes_json': ['saudacao', 'saudacao()'],
        'resposta_correta': 'saudacao()',
        'nome_arquivo': 'script.py',
    }
)

Etapa.objects.get_or_create(
    licao=licao2_mod4, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Recebendo dados e devolvendo resultados',
        'conteudo': 'Uma função pode receber parâmetros entre os parênteses, como "def soma(a, b):", e devolver um resultado com "return". Quem chamou a função recebe esse valor de volta.',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod4, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': "O que o comando 'return' faz dentro de uma função?",
        'opcoes_json': ['Devolve um valor para quem chamou a função', 'Imprime o valor na tela', 'Encerra o programa'],
        'resposta_correta': 'Devolve um valor para quem chamou a função',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod4, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Somando Dois Números',
        'conteudo': "Qual função soma 'a' e 'b' e devolve o resultado corretamente?",
        'opcoes_json': ['def soma(a, b): print a + b', 'def soma(a, b): return a + b'],
        'resposta_correta': 'def soma(a, b): return a + b',
        'nome_arquivo': 'script.py',
    }
)

# -----------------------------------------------------------------------------
# Módulo 5: Strings e Boas Práticas
# -----------------------------------------------------------------------------
mod5_python, _ = Modulo.objects.get_or_create(
    curso=curso_python,
    ordem=5,
    defaults={'titulo': '5. Strings e Boas Práticas'}
)

licao1_mod5, _ = Licao.objects.get_or_create(
    modulo=mod5_python,
    ordem=1,
    defaults={'titulo': 'Manipulando Texto', 'duracao_minutos': 7}
)

licao2_mod5, _ = Licao.objects.get_or_create(
    modulo=mod5_python,
    ordem=2,
    defaults={'titulo': 'Boas Práticas de Código', 'duracao_minutos': 6}
)

Etapa.objects.get_or_create(
    licao=licao1_mod5, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Trabalhando com texto',
        'conteudo': 'Strings têm métodos prontos para transformar texto, como .upper() (maiúsculas), .lower() (minúsculas) e .strip() (remove espaços nas pontas). f-strings, como f"Olá, {nome}!", inserem variáveis dentro do texto.',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod5, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual método transforma um texto em letras maiúsculas?',
        'opcoes_json': ['.upper()', '.maiusculo()', '.big()'],
        'resposta_correta': '.upper()',
    }
)
Etapa.objects.get_or_create(
    licao=licao1_mod5, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Formatando uma Mensagem',
        'conteudo': 'Qual forma insere corretamente o valor da variável "nome" dentro do texto usando f-string?',
        'opcoes_json': ['f"Olá, nome!"', 'f"Olá, {nome}!"'],
        'resposta_correta': 'f"Olá, {nome}!"',
        'nome_arquivo': 'script.py',
    }
)

Etapa.objects.get_or_create(
    licao=licao2_mod5, ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'Escrevendo código fácil de entender',
        'conteudo': 'Nomes de variáveis descritivos (como "idade_usuario" em vez de "x") e comentários explicando decisões não óbvias tornam o código mais fácil de entender e manter no futuro — inclusive por você mesmo.',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod5, ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': "Por que usar nomes de variáveis descritivos, como 'idade_usuario' em vez de 'x'?",
        'opcoes_json': ['Deixa o código mais fácil de entender e manter', 'Deixa o programa mais rápido', 'É obrigatório pelo Python'],
        'resposta_correta': 'Deixa o código mais fácil de entender e manter',
    }
)
Etapa.objects.get_or_create(
    licao=licao2_mod5, ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Escolhendo um Bom Nome',
        'conteudo': 'Qual nome de variável é mais claro para guardar a idade de uma pessoa?',
        'opcoes_json': ['x = 25', 'idade = 25'],
        'resposta_correta': 'idade = 25',
        'nome_arquivo': 'script.py',
    }
)

# -----------------------------------------------------------------------------
# Curso 2: Engenharia de IA & Prompting
# -----------------------------------------------------------------------------
curso_ia, _ = Curso.objects.get_or_create(
    slug='engenharia-de-ia-e-prompting',
    defaults={
        'titulo': 'Engenharia de IA & Prompting',
        'descricao': 'Construa assistentes de IA avançados, agentes autônomos e controle de contexto com modelos de linguagem.',
        'icone': '🤖',
        'nivel': 'intermediario',
        'ordem': 2,
        'ativo': True,
    }
)

mod1_ia, _ = Modulo.objects.get_or_create(
    curso=curso_ia,
    ordem=1,
    defaults={'titulo': '1. Fundamentos de LLMs & System Prompts'}
)

licao1_ia, _ = Licao.objects.get_or_create(
    modulo=mod1_ia,
    ordem=1,
    defaults={'titulo': 'O que é um System Prompt?', 'duracao_minutos': 6}
)

# Etapas da Lição 1
Etapa.objects.get_or_create(
    licao=licao1_ia,
    ordem=1,
    defaults={
        'tipo': 'slide',
        'titulo': 'O System Prompt define as regras do jogo',
        'conteudo': 'Antes da conversa começar, o system prompt diz ao modelo quem ele é, como deve se comportar e quais limites deve respeitar — o usuário nunca vê essa instrução diretamente.',
    }
)

Etapa.objects.get_or_create(
    licao=licao1_ia,
    ordem=2,
    defaults={
        'tipo': 'quiz',
        'pergunta': 'Qual é o principal objetivo de um system prompt?',
        'opcoes_json': [
            'Definir o comportamento e as regras do assistente antes da conversa começar',
            'Armazenar o histórico de mensagens do usuário',
        ],
        'resposta_correta': 'Definir o comportamento e as regras do assistente antes da conversa começar',
    }
)

Etapa.objects.get_or_create(
    licao=licao1_ia,
    ordem=3,
    defaults={
        'tipo': 'code',
        'titulo': 'Montando a Requisição',
        'conteudo': 'Para dar instruções ao modelo antes da conversa do usuário, o campo "role" dessa mensagem deve receber qual valor?',
        'opcoes_json': ['"role": "user"', '"role": "system"'],
        'resposta_correta': '"role": "system"',
        'nome_arquivo': 'api_request.py',
    }
)

print("✅ Cursos, Módulos, Lições e Etapas criadas com sucesso!")
