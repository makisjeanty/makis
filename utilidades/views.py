from django.shortcuts import render


def lista(request):
    return render(request, 'utilidades/lista.html')


def gerador_senha(request):
    return render(request, 'utilidades/gerador_senha.html')


def validador_documento(request):
    return render(request, 'utilidades/validador_documento.html')


def formatador_json(request):
    return render(request, 'utilidades/formatador_json.html')


def conversor_base64(request):
    return render(request, 'utilidades/conversor_base64.html')


def gerador_hash(request):
    return render(request, 'utilidades/gerador_hash.html')


def gerador_uuid(request):
    return render(request, 'utilidades/gerador_uuid.html')


def contador_texto(request):
    return render(request, 'utilidades/contador_texto.html')


def conversor_timestamp(request):
    return render(request, 'utilidades/conversor_timestamp.html')


def minificador_codigo(request):
    return render(request, 'utilidades/minificador_codigo.html')


def calculadora_tokens(request):
    return render(request, 'utilidades/calculadora_tokens.html')


def gerador_prompts(request):
    return render(request, 'utilidades/gerador_prompts.html')


def json_para_markdown(request):
    return render(request, 'utilidades/json_para_markdown.html')


def extrator_codigo_ia(request):
    return render(request, 'utilidades/extrator_codigo_ia.html')


def gerador_readme(request):
    return render(request, 'utilidades/gerador_readme.html')


def seguranca_owasp(request):
    return render(request, 'utilidades/seguranca_owasp.html')


def agente_orientador(request):
    return render(request, 'utilidades/agente_orientador.html')


def seo_especialista(request):
    return render(request, 'utilidades/seo_especialista.html')


def achador_oportunidades(request):
    return render(request, 'utilidades/achador_oportunidades.html')


def mini_curso(request):
    return render(request, 'utilidades/mini_curso.html')




