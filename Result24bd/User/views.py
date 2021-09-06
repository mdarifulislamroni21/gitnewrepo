from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from User.forms import USingUpForm,UProfileForm
from User.models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def USignUp(request):
    form=USingUpForm()
    if request.method =='POST':
        form=USingUpForm(request.POST)
        if form.is_valid():
            form.save()
    diction={'form':form,'button':'Registration','button2':'Sign Up'}
    return render(request,'User/logreg.html',context=diction)
def USignIn(request):
    form=AuthenticationForm()
    diction={'form':form,'button':'Login','button2':'Sign In'}
    state=''
    if request.POST:
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if not user.is_superuser:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    state = "Your account is not active, please contact the administrator."
            else:
                state = "Your email or password were incorrect.please try to currect details"
        else:
           state = "Your email or password were incorrect.please try to currect details"

    diction.update({
        'state': state,
    })
    return render(request,'User/logreg.html',context=diction)
@login_required
def Signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('USignIn'))
@login_required
def UProfileEddid(request):
    user=request.user
    ProfileObj=Profile.objects.get(user=user)
    form=UProfileForm(instance=ProfileObj)
    if request.method =='POST':
        form=UProfileForm(request.POST,request.FILES,instance=ProfileObj)
        if form.is_valid():
            nform=form.save(commit=False)
            nform.user=request.user
            nform.save()
            form=UProfileForm(instance=ProfileObj)
    diction={'form':form,}
    return render(request,'User/profileeddid.html',context=diction)
