import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Post, Categoria, Tag
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.first()

if admin_user:
    admin_user.first_name = "Makis"
    admin_user.last_name = "Jeanty"
    admin_user.save()

# Categorias
cat_resumos, _ = Categoria.objects.get_or_create(nome='Resumos Técnicos', defaults={'slug': 'resumos-tecnicos'})
cat_desafios, _ = Categoria.objects.get_or_create(nome='Desafios', defaults={'slug': 'desafios'})

# Tags
tag_ia, _ = Tag.objects.get_or_create(nome='IA', defaults={'slug': 'ia'})
tag_python, _ = Tag.objects.get_or_create(nome='Python', defaults={'slug': 'python'})
tag_perf, _ = Tag.objects.get_or_create(nome='Performance', defaults={'slug': 'performance'})

artigos_novos = [
    {
        'slug': 'engenharia-de-prompt-e-agentes-de-ia-em-python',
        'titulo': 'Engenharia de Prompt e Agentes de IA em Python: Como Construir Assistentes Especializados',
        'categoria': cat_resumos,
        'resumo': 'Explorando a construção de agentes de IA desacoplados em Python com controle de estado, validação de saída estruturada e otimização de contexto para produção.',
        'conteudo': """# Engenharia de Prompt e Agentes de IA em Python

A transição de chamadas simples de API para a construção de **Agentes de IA autônomos** exige uma mudança fundamental na arquitetura de software. Não se trata apenas de enviar um texto para uma LLM, mas de orquestrar estado, controlar contexto e garantir saídas estruturadas e previsíveis.

neste artigo, abordo os padrões essenciais para construir assistentes de IA resilientes em Python.

---

## 🎯 1. Validação de Saída Estruturada com Schemas

Um dos maiores desafios ao integrar LLMs em pipelines de software é a variabilidade das respostas em texto livre. Para contornar isso, utilizamos **saídas estruturadas** com esquemas estritos (JSON Schema / Pydantic):

```python
from pydantic import BaseModel, Field

class AnaliseRequisitos(BaseModel):
    resumo_executivo: str = Field(description="Resumo claro da demanda")
    complexidade: str = Field(description="Baixa, Média ou Alta")
    tecnologias_recomendadas: list[str]
    riscos_identificados: list[str]
```

Isso garante que a resposta da IA possa ser consumida diretamente por sistemas backend sem necessidade de expressões regulares frágeis.

---

## 🧠 2. Gestão de Memória e Janela de Contexto

Para manter o custo controlado e evitar alucinações por excesso de tokens, aplicamos técnicas de **compacção de contexto**:

1. **Memória Resumida (Summary Memory)**: Em conversas longas, o histórico antigo é compactado periodicamente por um modelo menor.
2. **Retrieval-Augmented Generation (RAG)**: Apenas os fragmentos de documentação relevantes para a pergunta atual são injetados no prompt.

---

## ⚡ Conclusão

Construir produtos acionados por IA requer aplicar a mesma disciplina de engenharia de software tradicional: tipagem forte, tratamento de exceções e monitoria de latência.
""",
        'tags': [tag_ia, tag_python],
    },
    {
        'slug': 'otimizacao-de-performance-no-django-6-caching-e-asgi',
        'titulo': 'Otimização de Performance no Django 6: Caching com Redis, Queries Otimizadas e ASGI',
        'categoria': cat_desafios,
        'resumo': 'Técnicas essenciais para eliminar gargalos de banco de dados com select_related, estratégias de cache distribuído em Redis e concorrência assíncrona.',
        'conteudo': """# Otimização de Performance no Django 6

Em aplicações web de alto tráfego, pequenos gargalos no ORM ou na camada de banco de dados podem se multiplicar rapidamente sob carga. No **Django 6**, dispomos de ferramentas nativas poderosas para garantir latências abaixo de 50ms.

---

## 🔍 1. Eliminando a Consulta N+1 no ORM

O erro mais comum em projetos Django é realizar consultas em loop sem pré-carregar relacionamentos:

```python
# ❌ INCORRETO: Executa 1 consulta para os posts + N consultas para os autores
posts = Post.objects.all()
for p in posts:
    print(p.autor.first_name)

# ✅ CORRETO: Executa apenas 1 consulta JOIN
posts = Post.objects.select_related('autor').all()
```

O uso apropriado de `select_related` (para Chaves Estrangeiras) e `prefetch_related` (para Muitos-para-Muitos) reduz o tempo de resposta em até 80%.

---

## 🚀 2. Cache Estratégico com Redis

Para endpoints de leitura intensa (como listagem de artigos e ferramentas), o uso do **Redis** evita batidas desnecessárias no banco de dados MySQL:

```python
from django.core.cache import cache

def get_produtos_destaque():
    produtos = cache.get('produtos_destaque')
    if not produtos:
        produtos = list(Projeto.objects.filter(destaque=True))
        cache.set('produtos_destaque', produtos, timeout=3600)  # Cache por 1 hora
    return produtos
```

---

## 🏁 Resultado

Combinando **queries otimizadas**, **cache de fragmentos** e **servidor ASGI (Daphne)**, conseguimos atender milhares de requisições por minuto mantendo o consumo de CPU e RAM mínimos na VPS.
""",
        'tags': [tag_python, tag_perf],
    }
]

for item in artigos_novos:
    tags = item.pop('tags')
    post, created = Post.objects.update_or_create(
        slug=item['slug'],
        defaults={
            **item,
            'autor': admin_user,
            'publicado': True,
            'data_publicacao': timezone.now(),
        }
    )
    post.tags.set(tags)
    status_str = "Criado" if created else "Atualizado"
    print(f"✅ Artigo do Blog: {post.titulo} ({status_str})")

print("\n🚀 Artigos adicionados com sucesso ao Blog!")
