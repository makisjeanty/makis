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

print("✅ Cursos, Módulos, Lições e Etapas criadas com sucesso!")
