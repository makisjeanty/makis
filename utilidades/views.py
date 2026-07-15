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
