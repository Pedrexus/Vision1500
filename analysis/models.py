import os

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def user_image_path(instance, filename):
    my_path = 'pictures_{0}/{1}'.format(slugify(instance.user.username),
                                        filename)
    return os.path.join(settings.MEDIA_ROOT, my_path)


class Market(models.Model):
    class Meta:
        verbose_name = 'Mercado'
        verbose_name_plural = 'Mercados'

    name = models.CharField(max_length=50, verbose_name='Nome do Mercado')

    def __str__(self):
        return self.name


class Picture(models.Model):
    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)

    market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True,
                               blank=True)
    content = models.ImageField(upload_to=user_image_path)

    def __str__(self):
        return ': '.join([self.user.username, str(self.id)])
