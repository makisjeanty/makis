from django import forms

from .models import Resposta, Topico


class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ['titulo', 'autor_nome', 'autor_email', 'conteudo']
        labels = {
            'titulo': 'Título',
            'autor_nome': 'Nome',
            'autor_email': 'E-mail',
            'conteudo': 'Mensagem',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'lw-input', 'placeholder': 'Título do tópico'}),
            'autor_nome': forms.TextInput(attrs={'class': 'lw-input', 'placeholder': 'Seu nome'}),
            'autor_email': forms.EmailInput(attrs={'class': 'lw-input', 'placeholder': 'Seu e-mail'}),
            'conteudo': forms.Textarea(attrs={'class': 'lw-input', 'placeholder': 'Sobre o que você quer conversar?', 'rows': 5}),
        }


class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['autor_nome', 'autor_email', 'conteudo']
        labels = {
            'autor_nome': 'Nome',
            'autor_email': 'E-mail',
            'conteudo': 'Resposta',
        }
        widgets = {
            'autor_nome': forms.TextInput(attrs={'class': 'lw-input', 'placeholder': 'Seu nome'}),
            'autor_email': forms.EmailInput(attrs={'class': 'lw-input', 'placeholder': 'Seu e-mail'}),
            'conteudo': forms.Textarea(attrs={'class': 'lw-input', 'placeholder': 'Sua resposta', 'rows': 4}),
        }
