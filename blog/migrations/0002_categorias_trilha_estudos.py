from django.db import migrations
from django.utils.text import slugify


CATEGORIAS = ['Estudos de Caso', 'Resumos Técnicos', 'Desafios']


def criar_categorias(apps, schema_editor):
    # Historical model não tem o save() customizado que gera o slug, então setamos aqui
    Categoria = apps.get_model('blog', 'Categoria')
    for nome in CATEGORIAS:
        Categoria.objects.get_or_create(nome=nome, defaults={'slug': slugify(nome)})


def remover_categorias(apps, schema_editor):
    Categoria = apps.get_model('blog', 'Categoria')
    Categoria.objects.filter(nome__in=CATEGORIAS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_categorias, remover_categorias),
    ]
