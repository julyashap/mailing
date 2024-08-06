from datetime import datetime
from smtplib import SMTPException
import pytz
from django.core.cache import cache
from blog.models import Blog
from config import settings
from config.settings import ENABLE_CACHE
from mailing.models import Newsletter, NewsletterLog
from django.core.mail import send_mail
from users.models import User


def sending_mail():
    zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.now(zone)

    newsletters = Newsletter.objects.filter(first_sending__lte=now).filter(status__in=['created', 'launched']).\
        filter(is_active=True)

    for newsletter in newsletters:
        is_created = newsletter.status == 'created'

        if not is_created:
            last_attempt_time = NewsletterLog.objects.filter(newsletter=newsletter).\
                order_by('-last_attempt').first().last_attempt

        if is_created or \
                newsletter.periodicity == 'daily' and (last_attempt_time - newsletter.first_sending).days == 1 or \
                newsletter.periodicity == 'weekly' and (last_attempt_time - newsletter.first_sending).days == 7 or \
                newsletter.periodicity == 'monthly' and \
                (last_attempt_time.month - newsletter.first_sending.month).months == 1:

            newsletter_log = NewsletterLog.objects.create(
                last_attempt=now,
                status=True,
                newsletter=newsletter
            )

            try:
                client_emails = newsletter.clients.values_list('email', flat=True)

                server_answer = send_mail(
                    newsletter.message.title,
                    newsletter.message.body,
                    newsletter.user.email,
                    list(client_emails),
                    fail_silently=False
                )

                if is_created:
                    newsletter.status = 'launched'
                    newsletter.save()

                if server_answer:
                    newsletter_log.server_answer = server_answer

            except SMTPException:
                newsletter.status = 'cancelled'
                newsletter.save()

                newsletter_log.status = False

                if server_answer:
                    newsletter_log.server_answer = server_answer

            newsletter_log.save()

        if newsletter.last_sending <= now:
            newsletter.status = 'completed'
            newsletter.save()


def cache_random_blog():
    if ENABLE_CACHE:
        key = 'random_blog'
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.all().order_by('?')[:3]
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.all().order_by('?')[:3]
    return blog_list


def cache_newsletter_total_count():
    if ENABLE_CACHE:
        key = 'newsletter_total_count'
        newsletter_count = cache.get(key)
        if newsletter_count is None:
            newsletter_count = Newsletter.objects.count()
            cache.set(key, newsletter_count)
    else:
        newsletter_count = Newsletter.objects.count()
    return newsletter_count


def cache_newsletter_active_count():
    if ENABLE_CACHE:
        key = 'newsletter_active_count'
        newsletter_count = cache.get(key)
        if newsletter_count is None:
            newsletter_count = Newsletter.objects.filter(is_active=True).count()
            cache.set(key, newsletter_count)
    else:
        newsletter_count = Newsletter.objects.filter(is_active=True).count()
    return newsletter_count


def cache_users_count():
    if ENABLE_CACHE:
        key = 'users_count'
        users_count = cache.get(key)
        if users_count is None:
            users_count = User.objects.count()
            cache.set(key, users_count)
    else:
        users_count = User.objects.count()
    return users_count


def cache_blog_list():
    if ENABLE_CACHE:
        key = 'blog_list'
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.all()
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.all()
    return blog_list
