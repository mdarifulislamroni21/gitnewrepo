from django import forms
from Post.models import Post,Categorys,PostImage
#create new forms
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude=('user','slug')
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Categorys
        exclude=('user',)
class PostImageForm(forms.ModelForm):
    class Meta:
        model=PostImage
        exclude=('slug',)
class CommentForm(forms.Form):
    comment=forms.CharField(widget=forms.Textarea,max_length=1000)
    email=forms.EmailField()
    website=forms.CharField(max_length=100)
    name=forms.CharField(max_length=100)
