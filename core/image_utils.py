import io
import os

from PIL import Image
from django.core.files.base import ContentFile


def otimizar_imagem(arquivo, max_dimensao=1920, qualidade=85):
    """Redimensiona (se maior que max_dimensao no lado maior) e converte para
    WebP. Retorna um ContentFile pronto para ser passado a FieldFile.save().
    """
    imagem = Image.open(arquivo)
    imagem = imagem.convert('RGBA' if imagem.mode in ('RGBA', 'LA', 'P') else 'RGB')

    if max(imagem.size) > max_dimensao:
        imagem.thumbnail((max_dimensao, max_dimensao), Image.LANCZOS)

    buffer = io.BytesIO()
    imagem.save(buffer, format='WEBP', quality=qualidade)

    nome_base = os.path.splitext(os.path.basename(arquivo.name))[0]
    return ContentFile(buffer.getvalue(), name=f'{nome_base}.webp')
