from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Picture


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture

        fields = ('market',
                  'content',
                  )
        labels = {
            'market': _('Supermercado'),
            'content': _('Imagem'),
        }
        help_texts = {
            'market': _('O supermercado onde você está'),
            'content': _('Faça o upload da sua imagem.'),
        }
        error_messages = {
            'content': {
            },
        }
        widgets = {
        }
