from django import forms

from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'conteudo']
        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'conteudo': 'Comentário',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'lw-input', 'placeholder': 'Seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'lw-input', 'placeholder': 'Seu e-mail'}),
            'conteudo': forms.Textarea(attrs={'class': 'lw-input', 'placeholder': 'Seu comentário', 'rows': 4}),
        }
