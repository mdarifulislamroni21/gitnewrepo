from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
# Create your models here.
class Categorys(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_category',on_delete=models.CASCADE)
    name=models.CharField(max_length=30,unique=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
ad='Admission'
category_option=(('','Select Category Here'),('Admission',f"{ad}"),('Result','Result'),('Notice','Notice'),('Examination','Examination'),('Islamic','Islamic'),('JobCircular','JobCircular'))
class Post(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='post_user',on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    slug=models.CharField(max_length=3000,unique=True)
    image=models.ImageField(upload_to='blog_post_image')
    popular=models.BooleanField(default=False)
    category=models.CharField(max_length=50,choices=category_option)
    discription=RichTextUploadingField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering=['-created']
    def pages(category):
        getCategory=Post.objects.filter(category=category)
        countCategory=getCategory.count
        return countCategory
    def get_absolute_url(self):
        return reverse('ReadMore',kwargs={'slug':self.slug,'category':self.category})
class PostImage(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='image_user',on_delete=models.CASCADE)
    slug=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='Discription_post')
class Comment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='comment_user',on_delete=models.CASCADE)
    blog=models.ForeignKey(Post,related_name='comment_post',on_delete=models.CASCADE)
    slug=models.CharField(max_length=1003)
    comment=models.CharField(max_length=1000)
    email=models.EmailField()
    website=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
class RepComment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='repcomment_user',on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,related_name='repcomment_comment',on_delete=models.CASCADE)
    repcomment=models.CharField(max_length=1000)
    message=models.CharField(max_length=1000)
    created=models.DateTimeField(auto_now_add=True)
class NewsLetter(models.Model):
    email=models.EmailField()
    created=models.DateTimeField(auto_now_add=True)
