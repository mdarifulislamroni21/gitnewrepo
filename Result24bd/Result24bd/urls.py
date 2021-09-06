from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include
from Post import views
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#for DEBUG=False
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
#for sitemap
from django.contrib.sitemaps.views import sitemap
from Post.sitemaps import PostSitemap
sitemaps={'items':PostSitemap}
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('result/admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('account/',include('User.urls')),
    path('user/create/post/',views.CreatePost,name="CreatePost"),
    path('user/edid/post/<str:slug>/',views.EdidPost,name="EdidPost"),
    path('user/delete/post/<category>/<str:slug>/',views.DeletePost,name="DeletePost"),
    path('user/create/category/',views.CrCategory,name="CrCategory"),
    re_path(r"^result/admin/", admin.site.urls),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    path('category/<category>/<str:slug>/',views.ReadMore,name='ReadMore'),
    path('comment/<category>/<str:slug>/',views.write_comment,name='write_comment'),
    path('category/<category>/',views.CategoryRead,name='CategoryRead'),
    path('replycomment/<str:slug>/<message>/',views.ReplieComment,name='ReplieComment'),
    path('newsletter/',views.NewsLetterSub,name='NewsLetterSub'),
    path('contact/',views.contactus,name='contactus'),
    path('privacy-policy/',views.privacy,name='privacy'),
    path('sitemap.xml/',sitemap,{'sitemaps':sitemaps}),
    path('404/',views.error_404_pages_get,name='error_404_pages_get'),
]
handler404='Post.views.error_404_views'
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
