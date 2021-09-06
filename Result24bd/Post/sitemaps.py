from django.contrib.sitemaps import Sitemap
from Post.models import Post
class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()
