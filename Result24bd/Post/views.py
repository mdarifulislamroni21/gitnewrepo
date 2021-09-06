from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from Post.forms import PostForm,CategoryForm,CommentForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from Post.models import Post,Comment,RepComment,NewsLetter
from django.contrib import messages
from django.urls import reverse
import uuid
# Create your views here.
def home(request):
    allpost=Post.objects.all()
    popular=Post.objects.filter(popular=True)
    admission=Post.objects.filter(category='Admission').order_by('-created')
    islamic=Post.objects.filter(category='Islamic')
    notice=Post.objects.filter(category='Notice')
    job_circular=Post.objects.filter(category='JobCircular')
    diction={'allpost':allpost,'populars':popular,'admissions':admission,'islamics':islamic,
    'notices':notice,'job_circulars':job_circular

    }
    return render(request,'Post/home.html',context=diction)
def CreatePost(request):
    diction={}
    superuser=False
    if request.user.is_superuser:
        superuser=True
        form=PostForm()
        diction={'form':form,'superuser':superuser}
        if request.method=='POST':
            form=PostForm(request.POST,request.FILES)
            if form.is_valid() and request.user.is_superuser:
                nform=form.save(commit=False)
                nform.user=request.user
                title=nform.title
                rep1=title.replace(":","-")
                rep2=rep1.replace(";","-")
                rep3=rep2.replace(":","-")
                rep4=rep3.replace("’","-")
                rep5=rep4.replace(".","-")
                rep6=rep5.replace(",","-")
                rep7=rep6.replace("+","-")
                titlef=rep7.replace("–","-")
                titlef1=titlef.replace("/","-")
                titlef2=titlef1.replace("&","-")
                titlef3=titlef2.replace("|","-")
                nform.slug=titlef3.replace(" ","-")+str(uuid.uuid4())+str(uuid.uuid4())+str(uuid.uuid4())
                nform.save()
            else:
                return HttpResponseRedirect(reverse('error_404_pages_get'))
    else:
        return HttpResponseRedirect(reverse('error_404_pages_get'))
    return render(request,'Post/crate_post.html',context=diction)

def CrCategory(request):
    diction={}
    if request.user.is_superuser:
        form=CategoryForm()
        if request.method=='POST':
            form=CategoryForm(request.POST)
            if form.is_valid() and request.user.is_superuser :
                nform=form.save(commit=False)
                nform.user=request.user
                nform.save()
            else:
                return HttpResponseRedirect(reverse('error_404_pages_get'))
        diction={'form':form}
    else:
        return HttpResponseRedirect(reverse('error_404_pages_get'))
    return render(request,'Post/create_category.html',context=diction)
def ReadMore(request,slug,category):
    allpost=Post.objects.all()
    popular=Post.objects.filter(popular=True)
    sigle_blog=Post.objects.get(slug=slug)
    CommentObj=Comment.objects.filter(blog=sigle_blog)
    diction={'single':sigle_blog,'comments':CommentObj,'populars':popular,'allposts':allpost}
    return render(request,'Post/readmore.html',context=diction)
@login_required
def write_comment(request,slug,category):
    if request.POST:
        user=request.user
        blog_name=Post.objects.get(slug=slug)
        comment=request.POST['comment']
        email=request.POST['email']
        website=request.POST['website']
        name=request.POST['name']
        CommentObj=Comment.objects.create(user=user,blog=blog_name,comment=comment,email=email,website=website,name=name,slug=uuid.uuid4())
        return HttpResponseRedirect(reverse('ReadMore',kwargs={'slug':slug,'category':category}))
def CategoryRead(request,category):
    popular=Post.objects.filter(popular=True)
    PostObj=Post.objects.filter(category=category)
    PostObjcount=PostObj.count()
    count=False
    if PostObjcount != 0:
        count=True
    paginator=Paginator(PostObj,12)
    page=request.GET.get('page')
    try:
        PostObj=paginator.page(page)
    except PageNotAnInteger:
        PostObj=paginator.page(1)
    except EmptyPage:
        PostObj=paginator.page(paginator.num_pages)
    diction={'categorys':PostObj,'name':category,'page':page,'count':count,'populars':popular}
    return render(request,'Post/category.html',context=diction)
@login_required
def ReplieComment(request,slug,message):
    if request.POST:
        user=request.user
        commentget=Comment.objects.get(slug=slug)
        blogname=commentget.blog
        commentMessage=message
        repcomment=request.POST['repcomment']
        createreply=RepComment.objects.create(user=user,comment=commentget,repcomment=repcomment,message=commentMessage)
        return HttpResponseRedirect(reverse('ReadMore',kwargs={'slug':blogname.slug,'category':blogname.category}))
def NewsLetterSub(request):
    if request.method=='POST':
        email=request.POST['email']
        Alrady=NewsLetter.objects.all()
        for check in Alrady:
            if check.email==email:
                messages.warning(request,"This Email Alrady Exist. Thank You for join Our NewsLetter")
                return HttpResponseRedirect(reverse('home'))
        NewsLetterCreate=NewsLetter.objects.create(email=email)
        messages.success(request,'Congratulations! You successfully joined Our NewsLetter. Thank You for join Our NewsLetter')
        return HttpResponseRedirect(reverse('home'))
def contactus(request):
    return render(request,'Post/contact.html')
def EdidPost(request,slug):
    if request.user.is_authenticated:
        PostObj=Post.objects.get(slug=slug)
        if request.user.is_superuser:
            form=PostForm(instance=PostObj)

            diction={'form':form,'slug':slug,'category':PostObj.category}
            if request.method=='POST':
                nform=PostForm(request.POST,request.FILES,instance=PostObj)
                if nform.is_valid():
                    mform=nform.save(commit=False)
                    mform.user=request.user
                    mform.save()
                    form=PostForm(instance=PostObj)
            return render(request,'Post/edid_post.html',context=diction)
        else:
            return HttpResponseRedirect(reverse('home'))
def privacy(request):
    return render(request,'Post/privacy.html')
def error_404_views(request,exception):
    return render(request,'Post/404.html')
def DeletePost(request,slug,category):
    if request.user.is_authenticated:
        PostObj=Post.objects.get(slug=slug)
        if request.user.is_superuser:
            PostObj.delete()
            return HttpResponseRedirect(reverse('CategoryRead',kwargs={'category':category}))
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))
def error_404_pages_get(request):
    return render(request,'Post/404.html')
