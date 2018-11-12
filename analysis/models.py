from django.conf import settings
from django.db import models


def user_image_path(instance, filename):
    return 'pictures_{0}/{1}'.format(instance.user.username, filename)


class Picture(models.Model):
    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    content = models.ImageField(upload_to=user_image_path)

    def __str__(self):
        return ': '.join([self.user.username, str(self.id)])
