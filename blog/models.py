from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    picture = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    published_at = models.DateTimeField(verbose_name='дата публикации')

    class Meta:
        verbose_name = 'статья блога'
        verbose_name_plural = 'статьи блога'

    def __str__(self):
        return f'{self.pk}. {self.title}'
