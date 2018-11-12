from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Picture


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture

        fields = ('content',
                  )
        labels = {
            'content': _('Imagem'),
        }
        help_texts = {
            'content': _('Faça o upload da sua imagem.'),
        }
        error_messages = {
            'content': {
            },
        }
        widgets = {
        }
