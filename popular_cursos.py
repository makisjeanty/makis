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
