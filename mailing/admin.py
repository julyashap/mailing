from django.contrib import admin

from mailing.models import Client, Message, Newsletter, NewsletterLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'patronymic', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_sending', 'periodicity', 'status', 'message',)


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_attempt', 'status', 'server_answer',)
