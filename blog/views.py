from django.views.generic import DetailView
from blog.models import Blog
from mailing.services import cache_blog_list


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=cache_blog_list()):
        self.object = super().get_object(queryset)

        self.object.count_views += 1
        self.object.save()

        return self.object
