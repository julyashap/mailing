from django.db import models
from users.models import User

NULLABLE = {
    "blank": True,
    "null": True
}


class Client(models.Model):
    email = models.EmailField(verbose_name='email')
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='отчество')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f"{self.email} ({self.last_name} {self.first_name})"


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='тема')
    body = models.TextField(verbose_name='тело сообщения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    PERIODICITY_CHOICES = (
        ('daily', 'раз в день'),
        ('weekly', 'раз в неделю'),
        ('monthly', 'раз в месяц'),
    )

    STATUS_CHOICES = (
        ('created', 'создана'),
        ('launched', 'запущена'),
        ('completed', 'завершена'),
        ('cancelled', 'отменена'),
    )

    first_sending = models.DateTimeField(verbose_name='первая отправка')
    last_sending = models.DateTimeField(verbose_name='последняя отправка')
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, verbose_name='статус')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            ('can_read_all_newsletters', 'Может просматривать любые рассылки'),
            ('can_change_is_active', 'Может отключать рассылку')
        ]

    def __str__(self):
        return f"{self.first_sending} {self.status}"


class NewsletterLog(models.Model):
    last_attempt = models.DateTimeField(verbose_name='последняя попытка')
    status = models.BooleanField(verbose_name='статус')
    server_answer = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')

    newsletter = models.ForeignKey(Newsletter, **NULLABLE, on_delete=models.CASCADE, verbose_name='рассылка')

    class Meta:
        verbose_name = 'попытки рассылки'
        verbose_name_plural = 'попытка рассылки'

    def __str__(self):
        return f"{self.last_attempt} {self.status}"
