from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import ClientCreateView, ClientDeleteView, ClientUpdateView, ClientListView, MessageCreateView, \
    MessageDeleteView, MessageUpdateView, MessageListView, NewsletterCreateView, NewsletterDeleteView, \
    NewsletterUpdateView, NewsletterListView, MailingView, ClientDetailView, NewsletterDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingView.as_view(), name='mailing_start'),

    path('client/create', ClientCreateView.as_view(), name='create_client'),
    path('client/', ClientListView.as_view(), name='list_client'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='detail_client'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('message/create', MessageCreateView.as_view(), name='create_message'),
    path('message/', MessageListView.as_view(), name='list_message'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('newsletter/create', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('newsletter/', NewsletterListView.as_view(), name='list_newsletter'),
    path('newsletter/<int:pk>', NewsletterDetailView.as_view(), name='detail_newsletter'),
    path('newsletter/update/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('newsletter/delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
]
