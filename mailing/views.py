from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, DetailView
from mailing.models import Client, Message, Newsletter, NewsletterLog
from mailing.services import cache_random_blog, cache_newsletter_total_count, cache_newsletter_active_count, \
    cache_users_count
from users.models import User


class MailingView(TemplateView):
    template_name = 'mailing/mailing_start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context['client_message'] = False
        elif Client.objects.filter(user=self.request.user) and Message.objects.filter(user=self.request.user):
            context['client_message'] = True
        else:
            context['client_message'] = False

        context['blogs'] = cache_random_blog()
        context['newsletters_total_count'] = cache_newsletter_total_count()
        context['newsletters_active_count'] = cache_newsletter_active_count()
        context['users_count'] = cache_users_count()

        return context


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    fields = ('email', 'first_name', 'last_name', 'patronymic', 'comment',)
    success_url = reverse_lazy('mailing:list_client')

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if not user.has_perm('mailing.can_read_all_newsletters'):
            self.queryset = Client.objects.filter(user=user)

        return super().get_queryset(*args, **kwargs)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ('email', 'first_name', 'last_name', 'patronymic', 'comment',)
    success_url = reverse_lazy('mailing:list_client')

    def test_func(self):
        return self.get_object().user == self.request.user


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mailing/confirm_delete.html'
    success_url = reverse_lazy('mailing:list_client')

    def test_func(self):
        return self.get_object().user == self.request.user


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    fields = ('title', 'body',)
    success_url = reverse_lazy('mailing:list_message')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if not user.has_perm('mailing.can_read_all_newsletters'):
            self.queryset = Message.objects.filter(user=user)

        return super().get_queryset(*args, **kwargs)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    fields = ('title', 'body',)
    success_url = reverse_lazy('mailing:list_message')

    def test_func(self):
        return self.get_object().user == self.request.user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mailing/confirm_delete.html'
    success_url = reverse_lazy('mailing:list_message')

    def test_func(self):
        return self.get_object().user == self.request.user


class NewsletterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Newsletter
    fields = ('first_sending', 'last_sending', 'periodicity', 'clients', 'message',)
    success_url = reverse_lazy('mailing:list_newsletter')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)

        return form

    def form_valid(self, form):
        if form.is_valid():
            form.instance.status = 'created'
            form.instance.user = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if not user.has_perm('mailing.can_read_all_newsletters'):
            self.queryset = Newsletter.objects.filter(user=user)

        return super().get_queryset(*args, **kwargs)


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter


class NewsletterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Newsletter
    fields = ('first_sending', 'last_sending', 'periodicity', 'clients', 'message',)
    success_url = reverse_lazy('mailing:list_newsletter')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)

        return form


class NewsletterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Newsletter
    template_name = 'mailing/confirm_delete.html'
    success_url = reverse_lazy('mailing:list_newsletter')

    def test_func(self):
        return self.get_object().user == self.request.user


class NewsletterLogListView(LoginRequiredMixin, ListView):
    model = NewsletterLog

    def get_queryset(self, *args, **kwargs):
        newsletter = Newsletter.objects.get(pk=self.kwargs.get('pk'))

        self.queryset = NewsletterLog.objects.filter(newsletter=newsletter)

        return super().get_queryset(*args, **kwargs)


@permission_required('mailing.can_change_is_active')
def newsletter_blocking(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_active = False
    newsletter.save()
    return redirect(reverse('mailing:list_newsletter'))


@permission_required('mailing.can_change_is_active')
def newsletter_unblocking(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_active = True
    newsletter.save()
    return redirect(reverse('mailing:list_newsletter'))
