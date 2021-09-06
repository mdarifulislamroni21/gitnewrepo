from django import forms
from User.models import User,Profile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
#create NewForm
class USingUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1=forms.CharField(label='Password',widget=forms.TextInput(attrs={'type':'password'}))
    password2=forms.CharField(label='Re Password',error_messages={'incomplete': 'Please enter a valid password.'},widget=forms.TextInput(attrs={'type':'password'}))
    class Meta:
        model=User
        fields=('email','username','password1','password2')
    email.help_text = ''
    password1.help_text=''
    password2.help_text=''
    error_messages = {
        'password_mismatch': ("password and re password didn't match."),
    }
class UProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('user',)
