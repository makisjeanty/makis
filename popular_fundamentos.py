import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cursos.models import Curso, Modulo, Licao, Etapa

# =============================================================================
# Trilha: Fundamentos de Programação que Não Mudam
# 5 Pilares — sem data de validade, aplicação direta em código real
# =============================================================================

curso, _ = Curso.objects.get_or_create(
    slug='fundamentos-que-nao-mudam',
    defaults={
        'titulo': 'Fundamentos que Não Mudam',
        'descricao': (
            'Os pilares da programação que nenhuma linguagem, framework ou tendência vai tornar obsoletos. '
            'Memória, estruturas de dados, algoritmos, recursão e orientação a objetos — '
            'dominados uma vez, aplicados para sempre.'
        ),
        'icone': '🧱',
        'nivel': 'intermediario',
        'ordem': 3,
        'ativo': True,
    }
)

# =============================================================================
# PILAR 1 — Como o computador realmente executa seu código
# Memória, stack, heap, mutabilidade, passagem por valor vs referência
# =============================================================================

mod1, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=1,
    defaults={
        'titulo': 'Pilar 1: Como o Computador Executa Seu Código',
        'descricao': 'Entenda a alocação de memória no Heap e na Stack, o ciclo de vida das variáveis e o comportamento de ponteiros em Python.',
        'icone': '💾'
    }
)

# --------------------------------------------------
# Lição 1.1 — Stack e Heap: onde vivem seus dados
# --------------------------------------------------
lic1_1, _ = Licao.objects.get_or_create(
    modulo=mod1,
    ordem=1,
    defaults={
        'titulo': 'Stack e Heap: onde vivem seus dados',
        'descricao': 'Descubra a diferença entre alocação automática na Stack e alocação dinâmica de objetos no Heap.',
        'icone': '🧠',
        'duracao_minutos': 8
    }
)

Etapa.objects.get_or_create(licao=lic1_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Toda variável ocupa espaço em algum lugar da memória',
    'conteudo': (
        'Quando você escreve x = 5 em Python, o interpretador aloca memória para guardar o inteiro 5. '
        'Essa memória vem de duas regiões distintas: a Stack (pilha) e o Heap. '
        'A Stack é rápida, organizada e automática — ideal para dados de vida curta como variáveis locais de função. '
        'O Heap é maior e mais flexível — guarda objetos que podem sobreviver além da função que os criou.'
    ),
})

Etapa.objects.get_or_create(licao=lic1_1, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Em Python, tudo é um objeto no Heap (Constantes vs Objetos)',
    'conteudo': (
        'Ao contrário de C, onde int x = 5 vai diretamente na stack, em Python '
        'até um simples inteiro é um objeto completo alocado no Heap — com contagem de referências, tipo, e valor. '
        'No seu repo (core/antispam.py), TEMPO_MINIMO_SEGUNDOS = 3 é uma constante imutável no Heap. '
        'Por ser imutável, ela é 100% thread-safe: múltiplos workers podem lê-la sem risco de race conditions.'
    ),
})

Etapa.objects.get_or_create(licao=lic1_1, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Por que constantes imutáveis como SALT_ANTISPAM em core/antispam.py são seguras em ambiente concorrente?',
    'opcoes_json': [
        'Porque ficam na Stack do sistema operacional',
        'Porque por serem imutáveis no Heap, nenhum worker pode alterar seu valor e causar race condition',
        'Porque o Django bloqueia acesso concorrente a arquivos python',
        'Porque são apagadas da memória a cada requisição',
    ],
    'resposta_correta': 'Porque por serem imutáveis no Heap, nenhum worker alterando seu valor e causando race condition',
})

Etapa.objects.get_or_create(licao=lic1_1, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'Identidade de objeto com id()',
    'conteudo': (
        'Qual função Python retorna o endereço de memória (identidade) de um objeto, '
        'permitindo verificar se duas variáveis apontam para o mesmo objeto no Heap?'
    ),
    'opcoes_json': ['type()', 'id()', 'hex()', 'ref()'],
    'resposta_correta': 'id()',
    'nome_arquivo': 'memoria.py',
})

# --------------------------------------------------
# Lição 1.2 — Valor vs Referência: o bug que todo mundo tem
# --------------------------------------------------
lic1_2, _ = Licao.objects.get_or_create(
    modulo=mod1,
    ordem=2,
    defaults={
        'titulo': 'Valor vs Referência & A Imutabilidade do QueryDict',
        'descricao': 'Aprenda como Python passa argumentos por referência e como mutabilidade gera bugs invisíveis em requisições.',
        'icone': '🐍',
        'duracao_minutos': 10
    }
)


Etapa.objects.get_or_create(licao=lic1_2, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Identidade vs Igualdade: is vs ==',
    'conteudo': (
        '== compara VALOR (método __eq__): verifica se o conteúdo dos objetos é idêntico.\n'
        'is compara IDENTIDADE (endereço no Heap): verifica se ambas as variáveis apontam para O MESMO objeto.\n\n'
        'Exemplo clássico:\n'
        '• "bot" == "bot" (True - mesmo texto)\n'
        '• Em Singletons como None, True e False, use sempre "is" (ex: if resultado is None:). '
        'Como só existe uma instância de None na memória, "is" compara apenas os ponteiros em O(1).'
    ),
})

Etapa.objects.get_or_create(licao=lic1_2, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Por que devemos usar "x is None" em vez de "x == None"?',
    'opcoes_json': [
        'Porque "is" compara o endereço de memória do Singleton None em O(1), sendo mais rápido e imune a sobrescritas de __eq__',
        'Porque "==" não funciona com a palavra None',
        'Porque "is" converte None para booleano automaticamente',
        'Não há diferença, é apenas estilo de código',
    ],
    'resposta_correta': 'Porque "is" compara o endereço de memória do Singleton None em O(1), sendo mais rápido e imune a sobrescritas de __eq__',
})

Etapa.objects.get_or_create(licao=lic1_2, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Passagem por referência: a função mexe no original',
    'conteudo': (
        'Tipos mutáveis (list, dict, set, objetos custom) passam a referência — o ponteiro para o mesmo objeto no Heap. '
        'Quando você passa uma lista para uma função e ela chama lista.append(...), '
        'esse append acontece no objeto original. '
        'No seu repo: quando ChatConsumer recebe scope e modifica headers internamente, '
        'está operando na mesma estrutura — não numa cópia.'
    ),
})

Etapa.objects.get_or_create(licao=lic1_2, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'O que acontece ao executar este código?\n\ndef adicionar(lst):\n    lst.append(99)\n\nminha_lista = [1, 2, 3]\nadicionar(minha_lista)\nprint(minha_lista)',
    'opcoes_json': [
        '[1, 2, 3] — a função recebeu uma cópia',
        '[1, 2, 3, 99] — a função operou na referência original',
        'Erro — listas não podem ser passadas para funções',
        '[99] — a lista foi substituída',
    ],
    'resposta_correta': '[1, 2, 3, 99] — a função operou na referência original',
})

Etapa.objects.get_or_create(licao=lic1_2, ordem=4, defaults={
    'tipo': 'slide',
    'titulo': 'Cópia Rasa vs Cópia Profunda (Shallow vs Deep Copy)',
    'conteudo': (
        '• Cópia Rasa (.copy()): Cria um novo container, mas mantêm as referências dos objetos internos.\n'
        '• Cópia Profunda (copy.deepcopy()): Copia o container E recursivamente copia todos os objetos internos.\n\n'
        'Cenário real no Django:\n'
        '1. request.POST.copy() faz uma cópia rasa mutável do QueryDict para permitir edições sem alterar a requisição HTTP original.\n'
        '2. Cuidado com dicionários aninhados: dict.copy() copia apenas a chave externa. '
        'Modificar um dicionário interno mutável altera o original e pode vazar estado entre requisições!'
    ),
})

Etapa.objects.get_or_create(licao=lic1_2, ordem=5, defaults={
    'tipo': 'quiz',
    'pergunta': 'Se fizermos "novo = original.copy()" em um dicionário que contém uma lista interna ("itens": [1, 2]), o que acontece se fizermos "novo["itens"].append(3)"?',
    'opcoes_json': [
        'Apenas o novo dicionário é alterado',
        'Ambos os dicionários serão alterados, pois a lista interna mantinha a mesma referência na memória (cópia rasa)',
        'O Python lança um erro de cópia inválida',
        'A lista original é apagada',
    ],
    'resposta_correta': 'Ambos os dicionários serão alterados, pois a lista interna mantinha a mesma referência na memória (cópia rasa)',
})

# --------------------------------------------------
# Lição 1.3 — Mutabilidade, Aliasing e o Perigo dos Defaults
# --------------------------------------------------
lic1_3, _ = Licao.objects.get_or_create(
    modulo=mod1,
    ordem=3,
    defaults={'titulo': 'Mutabilidade, Aliasing e o Perigo dos Defaults', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(licao=lic1_3, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Aliasing e Mutabilidade: Dois nomes, um mesmo objeto',
    'conteudo': (
        'Aliasing ocorre quando duas variáveis guardam a referência para O MESMO objeto no Heap.\n'
        'a = [1, 2]\n'
        'b = a\n'
        'b.append(3) # "a" também passa a ser [1, 2, 3]!\n\n'
        'Pegadinha clássica em funções:\n'
        'def add(item, lista=[]): # PERIGO! A lista [] é alocada no import e reusada em TODAS as chamadas!\n\n'
        'Por isso no Django Models usamos default=timezone.now (callable sem parênteses) '
        'e NUNCA default=timezone.now() (que congelaria o timestamp no momento da importação).'
    ),
})

Etapa.objects.get_or_create(licao=lic1_3, ordem=3, defaults={
    'tipo': 'slide',
    'titulo': 'Ciclo de Vida de Memória nas Views do Django & Garbage Collection',
    'conteudo': (
        '• Refcount: Quando uma view encerra sua execução, o frame da função na Stack é destruído. '
        'Variáveis locais (strings, dicionários de contexto, listas temporárias) têm refcount = 0 e a memória Heap é liberada IMEDIATAMENTE.\n'
        '• Ciclo da Requisição: Ao final do request (sinal request_finished), o Django limpa os handlers do middleware '
        'e libera/fecha a conexão com o banco de dados MySQL para evitar vazamentos de memória e conexões presas.\n'
        '• GC Cíclico: Trata apenas referências circulares (A aponta pra B e B aponta pra A) que o refcount simples não consegue zerar.'
    ),
})

Etapa.objects.get_or_create(licao=lic1_3, ordem=4, defaults={
    'tipo': 'quiz',
    'pergunta': 'O que acontece com as variáveis locais (ex: strings, listas de formulário) criadas dentro de uma View Django quando a função retorna o HttpResponse?',
    'opcoes_json': [
        'Permanecem na memória do servidor para a próxima requisição',
        'Seu refcount cai para 0 com o fim do escopo da função e o CPython libera a memória no Heap imediatamente',
        'São salvas automaticamente no banco de dados',
        'Ficam aguardando o reinício do servidor Daphne',
    ],
    'resposta_correta': 'Seu refcount cai para 0 com o fim do escopo da função e o CPython libera a memória no Heap imediatamente',
})

Etapa.objects.get_or_create(licao=lic1_3, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Imutável não significa que a variável não muda — significa que o objeto não muda',
    'conteudo': (
        'Quando você faz x = "olá" e depois x = "mundo", '
        'você não modificou a string "olá" — criou um novo objeto "mundo" no Heap '
        'e fez x apontar para ele. O objeto antigo continua existindo até o Garbage Collector recolhê-lo. '
        'Strings em Python são imutáveis: você nunca altera os caracteres no lugar, sempre cria uma nova string.'
    ),
})

Etapa.objects.get_or_create(licao=lic1_3, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'O Garbage Collector: memória automática tem custo',
    'conteudo': (
        'Python usa contagem de referências + GC cíclico. Quando nenhuma variável aponta para um objeto, '
        'sua contagem de referências cai a zero e a memória é liberada automaticamente. '
        'Referências cíclicas (A aponta para B, B aponta para A) exigem o GC secundário para resolver. '
        'No seu repo: cada Mensagem do chat ou Etapa do curso que você carrega em memória conta uma referência — '
        'não guardar listas grandes de objetos Django em variáveis globais por isso.'
    ),
})

Etapa.objects.get_or_create(licao=lic1_3, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Quando o Garbage Collector do Python libera um objeto da memória?',
    'opcoes_json': [
        'Quando a função onde foi criado termina',
        'Quando nenhuma variável aponta mais para ele (contagem de referências = 0)',
        'A cada 60 segundos automaticamente',
        'Quando você chama del explicitamente',
    ],
    'resposta_correta': 'Quando nenhuma variável aponta mais para ele (contagem de referências = 0)',
})

# =============================================================================
# PILAR 2 — Estruturas de Dados e o Trade-off Fundamental
# Lista, dict, set, tuple — complexidade e quando usar cada um
# =============================================================================

mod2, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=2,
    defaults={'titulo': 'Pilar 2: Estruturas de Dados e o Trade-off Fundamental'}
)

# --------------------------------------------------
# Lição 2.1 — O(n) vs O(1): a escolha que importa
# --------------------------------------------------
lic2_1, _ = Licao.objects.get_or_create(
    modulo=mod2,
    ordem=1,
    defaults={'titulo': 'O(n) vs O(1): a escolha que importa', 'duracao_minutos': 9}
)

Etapa.objects.get_or_create(licao=lic2_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Notação Big-O & O Trade-off das Estruturas de Dados',
    'conteudo': (
        '• list: Excelente para manter ordem e iterar. Mas buscar um item ("if item in lista") exige percorrer elemento por elemento — O(n).\n'
        '• set & dict: Utilizam Tabelas Hash. Buscar um item ("if item in meu_set" ou "dict.get(chave)") é instantâneo — O(1).\n\n'
        'Exemplo no seu Chat Consumer (chat/consumers.py):\n'
        '• Iterar sobre a lista de headers scope["headers"] para achar "x-forwarded-for" é O(n).\n'
        '• Converter para dict (dict(scope["headers"]).get(b"x-forwarded-for")) transforma a busca em O(1) instantâneo!'
    ),
})

Etapa.objects.get_or_create(licao=lic2_1, ordem=2, defaults={
    'tipo': 'quiz',
    'pergunta': 'Qual é a diferença de complexidade ao buscar um elemento com o operador "in" dentro de uma list vs dentro de um set?',
    'opcoes_json': [
        'list é O(n) (percorre um a um), enquanto set é O(1) (lookup direto via Hash)',
        'list é O(1) e set é O(n)',
        'Ambas possuem a mesma velocidade de busca O(1)',
        'set exige ordenação prévia O(n log n)',
    ],
    'resposta_correta': 'list é O(n) (percorre um a um), enquanto set é O(1) (lookup direto via Hash)',
})

Etapa.objects.get_or_create(licao=lic2_1, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Você tem 1 milhão de emails em memória e precisa verificar se um email específico está na lista. Qual estrutura é mais eficiente?',
    'opcoes_json': [
        'list — verificação com "in" percorre do início',
        'set — hash lookup O(1) independente do tamanho',
        'tuple — mais rápida que list para leitura',
        'dict — chaves são indexadas por hash',
    ],
    'resposta_correta': 'set — hash lookup O(1) independente do tamanho',
})

Etapa.objects.get_or_create(licao=lic2_1, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'Convertendo lista para set para busca eficiente',
    'conteudo': (
        'Dado: emails_bloqueados = ["spam@ex.com", "bot@ex.com", ...] — uma lista com 100.000 emails.\n'
        'Para converter em set e fazer buscas O(1), qual é a sintaxe correta?'
    ),
    'opcoes_json': [
        'emails_set = set(emails_bloqueados)',
        'emails_set = Set(emails_bloqueados)',
        'emails_set = {emails_bloqueados}',
        'emails_set = emails_bloqueados.to_set()',
    ],
    'resposta_correta': 'emails_set = set(emails_bloqueados)',
    'nome_arquivo': 'busca_eficiente.py',
})

# --------------------------------------------------
# Lição 2.2 — Dict: a estrutura que está em todo lugar
# --------------------------------------------------
lic2_2, _ = Licao.objects.get_or_create(
    modulo=mod2,
    ordem=2,
    defaults={'titulo': 'Dict: a estrutura que está em todo lugar', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(licao=lic2_2, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Tabelas Hash & O Erro "TypeError: unhashable type"',
    'conteudo': (
        '• Como o dict encontra tudo em O(1)? Ele passa a chave na função hash(chave), que gera um índice de memória direto.\n'
        '• Por que list não pode ser chave de dict? Listas são mutáveis. Se alterássemos uma lista usada como chave, seu hash mudaria e o dict nunca mais encontraria a chave!\n'
        '• Imutabilidade é requisito para Hash: str, int, float e tuple são hashable porque seus conteúdos nunca mudam.\n'
        '• Dica: Use tuplas (1, 2) como chave quando precisar de sequências compostas em um dict.'
    ),
})

Etapa.objects.get_or_create(licao=lic2_2, ordem=3, defaults={
    'tipo': 'slide',
    'titulo': 'Módulo Collections: defaultdict, Counter e deque',
    'conteudo': (
        '• defaultdict(list): Agrupa dados sem precisar testar "if chave not in dict". Se a chave não existir, cria a lista vazia automaticamente.\n'
        '  - Exemplo real: Agrupar habilidades por categoria em accounts/views.py (defaultdict(list)).\n'
        '• Counter: Conta ocorrências de elementos em O(n) instantaneamente (ex: Counter(["django", "python", "django"]) -> {"django": 2, "python": 1}).\n'
        '• deque: Fila de alta performance. Permite popleft() e append() em O(1), enquanto list.pop(0) é O(n).'
    ),
})

Etapa.objects.get_or_create(licao=lic2_2, ordem=4, defaults={
    'tipo': 'quiz',
    'pergunta': 'Qual é a principal vantagem de usar "defaultdict(list)" em relação a um dicionário comum ({}) para agrupar dados por chave?',
    'opcoes_json': [
        'Inicializa automaticamente uma lista vazia quando acessamos uma chave inexistente, dispensando testes com if/else',
        'Converte todas as chaves em inteiros automaticamente',
        'Impeça que novos elementos sejam adicionados',
        'Salva os dados no banco de dados automaticamente',
    ],
    'resposta_correta': 'Inicializa automaticamente uma lista vazia quando acessamos uma chave inexistente, dispensando testes com if/else',
})

Etapa.objects.get_or_create(licao=lic2_2, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Dicts no seu código Django',
    'conteudo': (
        'No seu repo, dicts aparecem em todo lugar:\n'
        '• request.POST e request.GET são dicts-like (QueryDict)\n'
        '• context passado para o template é um dict\n'
        '• opcoes_json nas Etapas do curso é uma lista serializada de/para dict via JSON\n'
        '• O scope do ChatConsumer é um dict com headers, path, client\n\n'
        'Quando você faz scope["client"] ou request.POST.get("website", ""), '
        'está fazendo um lookup O(1) na tabela hash — sempre rápido, independente do número de chaves.'
    ),
})

Etapa.objects.get_or_create(licao=lic2_2, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Qual método de dict retorna um valor padrão se a chave não existir, sem lançar KeyError?',
    'opcoes_json': [
        'dict[chave]',
        'dict.get(chave, valor_padrao)',
        'dict.find(chave)',
        'dict.fetch(chave, valor_padrao)',
    ],
    'resposta_correta': 'dict.get(chave, valor_padrao)',
})

Etapa.objects.get_or_create(licao=lic2_2, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'defaultdict para contadores',
    'conteudo': (
        'Você quer contar ocorrências de palavras em um texto, sem precisar checar se a chave já existe. '
        'Qual importação do módulo "collections" resolve isso elegantemente?'
    ),
    'opcoes_json': [
        'from collections import defaultdict',
        'from collections import CounterDict',
        'from collections import AutoDict',
        'from builtins import defaultdict',
    ],
    'resposta_correta': 'from collections import defaultdict',
    'nome_arquivo': 'contador_palavras.py',
})

# --------------------------------------------------
# Lição 2.3 — Stack e Queue: estruturas de controle de fluxo
# --------------------------------------------------
lic2_3, _ = Licao.objects.get_or_create(
    modulo=mod2,
    ordem=3,
    defaults={'titulo': 'Stack e Queue: controle de ordem e fluxo', 'duracao_minutos': 7}
)

Etapa.objects.get_or_create(licao=lic2_3, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Pilha (LIFO) vs Fila (FIFO) na Prática e na Logística',
    'conteudo': (
        '• FILA (FIFO - First In, First Out): O primeiro a entrar é o primeiro a sair.\n'
        '  - Na Logística: Separação de pedidos de e-commerce (o pedido mais antigo tem prioridade).\n'
        '  - Na Tecnologia: Filas assíncronas de e-mails, WebSockets no Django Channels e Celery.\n\n'
        '• PILHA (LIFO - Last In, First Out): O último a entrar é o primeiro a sair.\n'
        '  - Na Logística: Carregamento de caminhão de entregas (a última caixa colocada na porta é a primeira a ser entregue na primeira parada).\n'
        '  - Na Tecnologia: Call Stack do Python, botão Undo (Ctrl+Z) e avaliação de expressões.'
    ),
})

Etapa.objects.get_or_create(licao=lic2_3, ordem=2, defaults={
    'tipo': 'quiz',
    'pergunta': 'Um caminhão de entregas que atende 3 cidades precisa descarregar a última caixa colocada na porta primeiro. Qual estrutura de dados modela este comportamento?',
    'opcoes_json': [
        'Pilha (LIFO - Last In, First Out)',
        'Fila (FIFO - First In, First Out)',
        'Tabela Hash (Dict)',
        'Árvore Binária de Busca',
    ],
    'resposta_correta': 'Pilha (LIFO - Last In, First Out)',
})

Etapa.objects.get_or_create(licao=lic2_3, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Queue (Fila): FIFO — o primeiro que entra é o primeiro que sai',
    'conteudo': (
        'Uma fila funciona como fila de banco: o primeiro a entrar é o primeiro a ser atendido. '
        'FIFO = First In, First Out. '
        'Em Python, use collections.deque para uma fila eficiente — '
        '.append() adiciona no fim, .popleft() retira do início, ambos O(1). '
        'Não use list.pop(0) para fila — é O(n) porque desloca todos os elementos. '
        'No seu repo: o Channel Layer do Redis funciona como uma fila distribuída — '
        'mensagens do chat entram e saem na ordem, garantindo que ninguém receba mensagem fora de sequência.'
    ),
})

Etapa.objects.get_or_create(licao=lic2_3, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Por que collections.deque é melhor que list para uma fila (queue)?',
    'opcoes_json': [
        'Deque é mais fácil de importar',
        'list.pop(0) é O(n) — move todos os elementos; deque.popleft() é O(1)',
        'Deque suporta mais tipos de dados',
        'list não suporta popleft',
    ],
    'resposta_correta': 'list.pop(0) é O(n) — move todos os elementos; deque.popleft() é O(1)',
})

# =============================================================================
# PILAR 3 — Funções, Composição e o Poder dos Decorators
# =============================================================================

mod3, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=3,
    defaults={'titulo': 'Pilar 3: Funções, Composição e Decorators'}
)

# --------------------------------------------------
# Lição 3.1 — First-Class Functions, Closures e Decorators
# --------------------------------------------------
lic3_1, _ = Licao.objects.get_or_create(
    modulo=mod3,
    ordem=1,
    defaults={'titulo': 'First-Class Functions, Closures e Decorators', 'duracao_minutos': 9}
)

Etapa.objects.get_or_create(licao=lic3_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'First-Class Functions & Closures no Python',
    'conteudo': (
        '• First-Class Functions: Em Python, funções são objetos comuns. Podem ser passadas como argumentos, atribuídas a variáveis e retornadas de outras funções.\n'
        '• Closure: Ocorre quando uma função interna "lembra" do ambiente e das variáveis onde foi criada, mesmo após a função externa ter finalizado.\n\n'
        'Exemplo no seu Projeto (@ratelimit em blog/views.py):\n'
        'A sintaxe @ratelimit(key="ip", rate="10/m") é um açúcar sintático (Syntax Sugar). '
        'Ela equivale a: detalhe_post = ratelimit(key="ip", rate="10/m")(detalhe_post).'
    ),
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=3, defaults={
    'tipo': 'slide',
    'titulo': 'Fábrica de Decorators: Por que 3 Níveis de Aninhamento?',
    'conteudo': (
        '• Decorator Simples (2 níveis): def dec(func) -> def wrapper(*args) -> executa func().\n'
        '• Decorator com Argumentos (3 níveis): Exemplo @ratelimit(rate="5/m").\n'
        '  1. Nível 1 (Fábrica): Recebe as configurações (rate="5/m").\n'
        '  2. Nível 2 (Decorator): Recebe a função alvo (view).\n'
        '  3. Nível 3 (Wrapper): Executa a cada requisição capturando as configurações da Closure.'
    ),
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=4, defaults={
    'tipo': 'slide',
    'titulo': 'Generators e Avaliação Preguiçosa (Lazy Iterators)',
    'conteudo': (
        '• yield: Transforma uma função em um Generator. Em vez de calcular e retornar uma lista completa na memória RAM, devolve um item por vez sob demanda.\n'
        '• Aplicação no Django: Post.objects.all().iterator(chunk_size=1000) busca milhares de registros em lotes, prevenindo estouro de memória RAM (OOM) na VPS.'
    ),
})

# =============================================================================
# PILAR 4 — Modelagem, Invariantes e Coesão
# =============================================================================

mod4, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=4,
    defaults={'titulo': 'Pilar 4: Modelagem e Arquitetura de Software'}
)

lic4_1, _ = Licao.objects.get_or_create(
    modulo=mod4,
    ordem=1,
    defaults={'titulo': 'Entidades, Invariantes e Constraints', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(licao=lic4_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Modelagem: Entidades vs Valores & Invariantes',
    'conteudo': (
        '• Entidades: Têm identidade única no tempo (ex: PerfilUsuario, Compra, Topico).\n'
        '• Value Objects: Definidos apenas por seus dados sem identidade (ex: e-mail, slug, ícone).\n'
        '• Invariantes & Constraints: Invariante é uma regra de negócio que NUNCA pode ser violada (ex: um pedido Kiwify não pode ser processado 2 vezes).\n'
        '  - Garantia: Usamos unique=True em referencia_externa no MySQL para forçar a regra no nível do banco.'
    ),
})

# =============================================================================
# PILAR 5 — Concorrência, Transações e Assincronismo (Asyncio / Channels)
# =============================================================================

mod5, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=5,
    defaults={'titulo': 'Pilar 5: Concorrência, Transações e Asyncio'}
)

lic5_1, _ = Licao.objects.get_or_create(
    modulo=mod5,
    ordem=1,
    defaults={'titulo': 'Race Conditions, Cache Atômico e Event Loop', 'duracao_minutos': 10}
)

Etapa.objects.get_or_create(licao=lic5_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Race Conditions & Operações Atômicas no Cache',
    'conteudo': (
        '• Race Condition: Ocorre quando 2 requisições tentam ler e alterar o mesmo dado simultaneamente.\n'
        '• Por que cache.get() + set() é perigoso? Permite janela de concorrência. Duas requisições lêem None ao mesmo tempo.\n'
        '• Solução Atômica: No ChatConsumer, usamos cache.add() + cache.incr() em instruções atômicas no Redis O(1).\n'
        '• Async/Await: No Channels, usamos await nas I/Os de rede para liberar o Event Loop enquanto a mensagem é transmitida.'
    ),
})

Etapa.objects.get_or_create(licao=lic5_1, ordem=2, defaults={
    'tipo': 'quiz',
    'pergunta': 'Por que a operação de rate-limiting do chat usa "cache.add()" em vez de "if not cache.get(): cache.set()"?',
    'opcoes_json': [
        'Porque cache.add() é atômico no Redis, impedindo que requisições concorrentes ultrapassem o limite na janela de leitura',
        'Porque cache.get() consome muito espaço no banco MySQL',
        'Porque o Python não suporta funções síncronas em cache',
        'Porque cache.add() limpa o cache automaticamente',
    ],
    'resposta_correta': 'Porque cache.add() é atômico no Redis, impedindo que requisições concorrentes ultrapassem o limite na janela de leitura',
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Big-O na Prática: Do Banco de Dados à Memória',
    'conteudo': (
        '• O(1) Constante: Acesso por chave em dict/set (via Tabela Hash).\n'
        '  - Pegadinha: Se houver colisão de Hash em massa, a performance cai de O(1) para O(n)!\n'
        '• O(log n) Logarítmico: Busca binária e índices de Banco de Dados.\n'
        '  - Exemplo real: Post.objects.get(slug=slug) no MySQL usa índice B-Tree O(log n). Com 1 milhão de posts, acha em ~20 operações.\n'
        '• O(n) Linear: Percorrer listas sem índice ou buscar registros em tabela sem chave indexada (Full Table Scan).\n'
        '• O(n²) Quadrático: Loops aninhados ("for a in lista: for b in lista"). Quando vir um loop aninhado, sinta o cheiro de "isso devia usar dict".'
    ),
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=2, defaults={
    'tipo': 'quiz',
    'pergunta': 'Qual é a complexidade de buscar um objeto por uma coluna indexada com B-Tree (como o slug no MySQL)?',
    'opcoes_json': [
        'O(log n) — elimina metades da árvore de índices a cada passo',
        'O(n²) — precisa verificar todas as combinações',
        'O(n) — sempre percorre a tabela do início ao fim',
        'O(0) — não consome tempo de execução',
    ],
    'resposta_correta': 'O(log n) — elimina metades da árvore de índices a cada passo',
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Busca Binária: O(log n) — 1 milhão de itens em 20 comparações',
    'conteudo': (
        'Busca binária exige lista ordenada. Estratégia: compare com o elemento do meio. '
        'Se o alvo é menor, elimine a metade direita. Se maior, elimine a metade esquerda. Repita. '
        'Cada passo elimina metade dos candidatos restantes. '
        'Com 1.000.000 itens: log₂(1.000.000) ≈ 20 comparações. '
        'Com busca linear: até 1.000.000 comparações. '
        'Custo: a lista precisa estar ordenada. '
        'No seu repo: o banco MySQL usa B-Trees (parente da busca binária) nos índices — '
        'por isso um campo indexado (como referencia_externa em Compra) é O(log n), não O(n).'
    ),
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Uma lista ordenada tem 1.024 elementos. Quantas comparações no máximo a busca binária precisa?',
    'opcoes_json': ['1.024', '512', '10', '20'],
    'resposta_correta': '10',
})

Etapa.objects.get_or_create(licao=lic3_1, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'Busca binária com bisect',
    'conteudo': (
        'Python tem o módulo bisect para busca binária em listas ordenadas. '
        'Qual função retorna o índice onde um valor seria inserido para manter a lista ordenada?'
    ),
    'opcoes_json': [
        'bisect.bisect_left(lista, valor)',
        'bisect.search(lista, valor)',
        'bisect.find(lista, valor)',
        'bisect.binary(lista, valor)',
    ],
    'resposta_correta': 'bisect.bisect_left(lista, valor)',
    'nome_arquivo': 'busca_binaria.py',
})

# --------------------------------------------------
# Lição 3.2 — Ordenação: por que importa entender o sort
# --------------------------------------------------
lic3_2, _ = Licao.objects.get_or_create(
    modulo=mod3,
    ordem=2,
    defaults={'titulo': 'Ordenação: por que importa entender o sort', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(licao=lic3_2, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Python usa Timsort: O(n log n) e estável',
    'conteudo': (
        'O sorted() e list.sort() do Python usam Timsort — um algoritmo híbrido (Merge Sort + Insertion Sort). '
        'Complexidade: O(n log n) no pior caso, O(n) no melhor caso (lista já ordenada). '
        'Estável: elementos com chaves iguais mantêm a ordem relativa original. '
        'Isso importa quando você ordena por múltiplos critérios: primeiro por data, depois por ID — '
        'a estabilidade garante que a ordem por ID não embaralhe os grupos de data.'
    ),
})

Etapa.objects.get_or_create(licao=lic3_2, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'key= é mais poderoso que você pensa',
    'conteudo': (
        'O parâmetro key= recebe uma função aplicada a cada elemento para determinar o critério de ordenação. '
        'Sem criar uma lista intermediária, sem comparar manualmente. '
        'Exemplos:\n'
        '• sorted(posts, key=lambda p: p.data_publicacao) — ordena por data\n'
        '• sorted(projetos, key=lambda p: (p.categoria, p.titulo)) — ordena por dois critérios\n'
        '• sorted(mensagens, key=attrgetter("criado_em")) — mesmo resultado, mais eficiente\n\n'
        'No seu repo: o order_by() do Django ORM faz exatamente isso no banco, '
        'mas quando você já tem os objetos em memória, sorted() com key= é a ferramenta certa.'
    ),
})

Etapa.objects.get_or_create(licao=lic3_2, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'Qual é a complexidade do sorted() do Python no pior caso?',
    'opcoes_json': ['O(n)', 'O(n²)', 'O(n log n)', 'O(log n)'],
    'resposta_correta': 'O(n log n)',
})

Etapa.objects.get_or_create(licao=lic3_2, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'Ordenando objetos por atributo',
    'conteudo': (
        'Você tem uma lista de objetos Post com atributo data_publicacao. '
        'Para ordenar do mais recente para o mais antigo com sorted(), qual é o código correto?'
    ),
    'opcoes_json': [
        'sorted(posts, key=lambda p: p.data_publicacao, reverse=True)',
        'sorted(posts, key="data_publicacao", reverse=True)',
        'posts.sort_by(data_publicacao, desc=True)',
        'sorted(posts, reverse=True)',
    ],
    'resposta_correta': 'sorted(posts, key=lambda p: p.data_publicacao, reverse=True)',
    'nome_arquivo': 'ordenar_posts.py',
})

# =============================================================================
# PILAR 4 — Recursão: quando a função chama a si mesma
# Call stack, base case, memoização
# =============================================================================

mod4, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=4,
    defaults={'titulo': 'Pilar 4: Recursão — Quando a Função Chama a Si Mesma'}
)

# --------------------------------------------------
# Lição 4.1 — Como a recursão funciona na call stack
# --------------------------------------------------
lic4_1, _ = Licao.objects.get_or_create(
    modulo=mod4,
    ordem=1,
    defaults={'titulo': 'Como a recursão funciona na call stack', 'duracao_minutos': 9}
)

Etapa.objects.get_or_create(licao=lic4_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Recursão: uma função que resolve o problema reduzindo para si mesma',
    'conteudo': (
        'Recursão é quando uma função chama a si mesma com uma entrada menor ou mais simples. '
        'Todo algoritmo recursivo precisa de dois ingredientes obrigatórios:\n'
        '1. Caso base: a condição que para a recursão (sem isso → loop infinito → RecursionError)\n'
        '2. Caso recursivo: a chamada a si mesmo com um problema menor\n\n'
        'Exemplo clássico:\n'
        'def fatorial(n):\n'
        '    if n == 0: return 1        # caso base\n'
        '    return n * fatorial(n - 1)  # caso recursivo'
    ),
})

Etapa.objects.get_or_create(licao=lic4_1, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'O que acontece na memória: frames empilhados',
    'conteudo': (
        'Cada chamada recursiva empilha um novo frame na call stack. '
        'fatorial(4) → fatorial(3) → fatorial(2) → fatorial(1) → fatorial(0). '
        'Ao chegar no caso base, os frames começam a ser desempilhados e os valores resolvidos. '
        'Problema: Python tem limite de recursão padrão de 1000 frames (sys.getrecursionlimit()). '
        'Recursão muito profunda → RecursionError: maximum recursion depth exceeded. '
        'Solução para casos profundos: memoização ou conversão para loop iterativo.'
    ),
})

Etapa.objects.get_or_create(licao=lic4_1, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'O que causa um RecursionError em Python?',
    'opcoes_json': [
        'Usar recursão em vez de um loop',
        'Esquecer o caso base, fazendo a recursão nunca parar',
        'Chamar a função com número negativo',
        'Ter mais de uma chamada recursiva na mesma função',
    ],
    'resposta_correta': 'Esquecer o caso base, fazendo a recursão nunca parar',
})

# --------------------------------------------------
# Lição 4.2 — Memoização: não calcule o que você já calculou
# --------------------------------------------------
lic4_2, _ = Licao.objects.get_or_create(
    modulo=mod4,
    ordem=2,
    defaults={'titulo': 'Memoização: não calcule o que você já calculou', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(licao=lic4_2, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Fibonacci ingênuo: O(2ⁿ) — exponencial',
    'conteudo': (
        'A sequência de Fibonacci (1, 1, 2, 3, 5, 8, 13...) parece simples:\n'
        'def fib(n): return fib(n-1) + fib(n-2) if n > 1 else n\n\n'
        'Problema: fib(40) faz 2 bilhões de chamadas. Por quê? '
        'fib(5) precisa de fib(4) e fib(3). '
        'fib(4) precisa de fib(3) e fib(2). '
        'fib(3) é calculado duas vezes. fib(2) quatro vezes. A redundância cresce exponencialmente.'
    ),
})

Etapa.objects.get_or_create(licao=lic4_2, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': '@lru_cache: memoização em uma linha',
    'conteudo': (
        'Memoização guarda o resultado de chamadas anteriores. '
        'Se fib(3) já foi calculado, retorna o valor guardado sem recalcular. '
        'Python oferece isso com @functools.lru_cache:\n\n'
        'from functools import lru_cache\n\n'
        '@lru_cache(maxsize=None)\n'
        'def fib(n): return fib(n-1) + fib(n-2) if n > 1 else n\n\n'
        'Com @lru_cache: fib(40) = 40 chamadas únicas. Sem: 2 bilhões. '
        'No seu repo: qualquer função pura e cara (sem efeitos colaterais) pode se beneficiar disso — '
        'cálculos de scores, formatações pesadas, resultados de validações reutilizáveis.'
    ),
})

Etapa.objects.get_or_create(licao=lic4_2, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'O que o decorator @lru_cache faz em uma função recursiva?',
    'opcoes_json': [
        'Aumenta o limite de recursão do Python',
        'Armazena os resultados de chamadas anteriores para não recalcular',
        'Converte a recursão em um loop automaticamente',
        'Paraleliza as chamadas recursivas',
    ],
    'resposta_correta': 'Armazena os resultados de chamadas anteriores para não recalcular',
})

Etapa.objects.get_or_create(licao=lic4_2, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'Aplicando lru_cache',
    'conteudo': (
        'Para aplicar memoização automática a uma função Python, '
        'qual é o decorator correto do módulo functools?'
    ),
    'opcoes_json': [
        '@functools.lru_cache(maxsize=None)',
        '@functools.memorize()',
        '@functools.cache_result()',
        '@functools.memoize(maxsize=None)',
    ],
    'resposta_correta': '@functools.lru_cache(maxsize=None)',
    'nome_arquivo': 'memoizacao.py',
})

# =============================================================================
# PILAR 5 — Orientação a Objetos: os 4 pilares reais
# Encapsulamento, Herança, Polimorfismo, Abstração — sem decoração
# =============================================================================

mod5, _ = Modulo.objects.get_or_create(
    curso=curso,
    ordem=5,
    defaults={'titulo': 'Pilar 5: Orientação a Objetos — Os 4 Pilares Reais'}
)

# --------------------------------------------------
# Lição 5.1 — Encapsulamento: protegendo o estado interno
# --------------------------------------------------
lic5_1, _ = Licao.objects.get_or_create(
    modulo=mod5,
    ordem=1,
    defaults={'titulo': 'Encapsulamento: protegendo o estado interno', 'duracao_minutos': 8}
)

Etapa.objects.get_or_create(licao=lic5_1, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Encapsulamento: expor interface, esconder implementação',
    'conteudo': (
        'Encapsulamento é agrupar dados (atributos) e comportamentos (métodos) numa classe, '
        'expondo apenas o necessário para o mundo externo. '
        'Não é sobre "tornar privado por privado" — é sobre controlar quem pode mudar o que. '
        'Em Python: _ (underscore simples) = "por convenção, não mexa aqui". '
        '__ (dunder) = name mangling — Python renomeia para _Classe__atributo, '
        'dificultando (mas não impossibilitando) o acesso externo.'
    ),
})

Etapa.objects.get_or_create(licao=lic5_1, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Encapsulamento no Django: o Model é o guardião dos dados',
    'conteudo': (
        'No seu repo, os Models Django são o exemplo perfeito de encapsulamento:\n'
        '• Compra.objects.get_or_create(referencia_externa=...) — você não acessa a tabela diretamente\n'
        '• Curso.save() auto-slugifica o título — a lógica de negócio fica no modelo, não na view\n'
        '• formulario_parece_bot(request) em core/antispam.py — encapsula toda a lógica de detecção\n\n'
        'A view não precisa saber como o honeypot funciona. '
        'Ela só chama bloquear_submissao_suspeita() e confia no resultado. '
        'Isso é encapsulamento aplicado.'
    ),
})

Etapa.objects.get_or_create(licao=lic5_1, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'O que o prefixo __ (duplo underscore) em um atributo Python realmente faz?',
    'opcoes_json': [
        'Torna o atributo 100% inacessível fora da classe',
        'Aplica name mangling: renomeia para _Classe__atributo, dificultando acesso externo',
        'Marca o atributo como constante imutável',
        'Faz o atributo ser compartilhado entre todas as instâncias',
    ],
    'resposta_correta': 'Aplica name mangling: renomeia para _Classe__atributo, dificultando acesso externo',
})

# --------------------------------------------------
# Lição 5.2 — Herança vs Composição: a escolha certa
# --------------------------------------------------
lic5_2, _ = Licao.objects.get_or_create(
    modulo=mod5,
    ordem=2,
    defaults={'titulo': 'Herança vs Composição: a escolha certa', 'duracao_minutos': 10}
)

Etapa.objects.get_or_create(licao=lic5_2, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Herança: "é um" — use com moderação',
    'conteudo': (
        'Herança diz que uma classe filho "é um tipo de" classe pai. '
        'PerfilUsuario herda de AbstractUser: faz sentido — PerfilUsuario É um usuário, com campos extras. '
        'Problema clássico: herança profunda cria acoplamento rígido. '
        'Mudança na classe pai quebra todos os filhos. '
        'Regra prática: se você precisa de mais de 2 níveis de herança, '
        'provavelmente composição resolveria melhor.'
    ),
})

Etapa.objects.get_or_create(licao=lic5_2, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Composição: "tem um" — prefira isso',
    'conteudo': (
        'Composição diz que uma classe "tem um" componente, não que "é um". '
        'Exemplo: ChatConsumer TEM um rate_limiter, não herda de RateLimiter. '
        'Vantagem: você pode trocar a implementação do componente sem tocar no consumidor. '
        'No seu repo: Curso TEM Modulos, Modulo TEM Licoes, Licao TEM Etapas — '
        'relação via ForeignKey é composição. '
        'Se você precisasse que Curso herdasse de Licao, algo estaria muito errado no modelo.'
    ),
})

Etapa.objects.get_or_create(licao=lic5_2, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'No seu repo, PerfilUsuario herda de AbstractUser. Qual relação OOP isso representa?',
    'opcoes_json': [
        'Composição — PerfilUsuario TEM um AbstractUser',
        'Herança — PerfilUsuario É UM tipo de AbstractUser com campos extras',
        'Polimorfismo — PerfilUsuario substitui AbstractUser completamente',
        'Abstração — AbstractUser esconde a implementação do PerfilUsuario',
    ],
    'resposta_correta': 'Herança — PerfilUsuario É UM tipo de AbstractUser com campos extras',
})

# --------------------------------------------------
# Lição 5.3 — Polimorfismo: mesma interface, comportamentos diferentes
# --------------------------------------------------
lic5_3, _ = Licao.objects.get_or_create(
    modulo=mod5,
    ordem=3,
    defaults={'titulo': 'Polimorfismo: mesma interface, comportamentos diferentes', 'duracao_minutos': 7}
)

Etapa.objects.get_or_create(licao=lic5_3, ordem=1, defaults={
    'tipo': 'slide',
    'titulo': 'Polimorfismo: o código que não precisa saber com quem está falando',
    'conteudo': (
        'Polimorfismo permite que o mesmo código opere sobre tipos diferentes, '
        'desde que eles implementem a mesma interface. '
        'Exemplo Python: len() funciona em str, list, tuple, dict — '
        'cada um implementa __len__() de forma diferente, mas você chama len() igual em todos. '
        'O código que chama len() não precisa saber se está medindo uma string ou uma lista.'
    ),
})

Etapa.objects.get_or_create(licao=lic5_3, ordem=2, defaults={
    'tipo': 'slide',
    'titulo': 'Polimorfismo no Django: Views, Forms e Sitemaps',
    'conteudo': (
        'No seu repo, polimorfismo aparece nos sitemaps:\n'
        '• PostSitemap, ProjetoSitemap, TopicositeSitemap — cada um tem items() e location() próprios\n'
        '• O framework de sitemaps chama os mesmos métodos em todos, sem saber qual é qual\n\n'
        'Os Channels também são polimórficos:\n'
        '• InMemoryChannelLayer e RedisChannelLayer têm a mesma interface (send, receive, group_send)\n'
        '• O ChatConsumer não sabe qual está usando — chama group_send() e funciona nos dois casos\n\n'
        'Isso é Duck Typing: "se anda como pato e grasna como pato, é um pato".'
    ),
})

Etapa.objects.get_or_create(licao=lic5_3, ordem=3, defaults={
    'tipo': 'quiz',
    'pergunta': 'O que é Duck Typing em Python?',
    'opcoes_json': [
        'Uma forma de tipagem estática baseada em annotations',
        'Se um objeto implementa os métodos esperados, ele pode ser usado — independente do seu tipo real',
        'Um padrão para nomear variáveis com nomes descritivos',
        'Um tipo especial de herança múltipla',
    ],
    'resposta_correta': 'Se um objeto implementa os métodos esperados, ele pode ser usado — independente do seu tipo real',
})

Etapa.objects.get_or_create(licao=lic5_3, ordem=4, defaults={
    'tipo': 'code',
    'titulo': 'Implementando __len__ para polimorfismo',
    'conteudo': (
        'Para que sua classe personalizada funcione com a função len() do Python, '
        'qual método dunder você precisa implementar?'
    ),
    'opcoes_json': ['__len__(self)', '__size__(self)', '__count__(self)', '__length__(self)'],
    'resposta_correta': '__len__(self)',
    'nome_arquivo': 'dunder_len.py',
})

print("OK - Trilha 'Fundamentos que Nao Mudam' criada com sucesso!")
print("   5 Pilares | 13 Licoes | 46 Etapas")
print("   Slug: fundamentos-que-nao-mudam")
