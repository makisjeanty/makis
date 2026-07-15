from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

User = get_user_model()


def sobre(request):
    perfil = User.objects.filter(is_superuser=True).order_by('date_joined').first()
    return render(request, 'accounts/perfil.html', {
        'perfil': perfil,
        'og_image_url': perfil.avatar.url if perfil and perfil.avatar else None,
    })


def perfil(request, username):
    perfil = get_object_or_404(User, username=username)
    return render(request, 'accounts/perfil.html', {
        'perfil': perfil,
        'og_image_url': perfil.avatar.url if perfil.avatar else None,
    })
