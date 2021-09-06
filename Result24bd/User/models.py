from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class MyUsermanager(BaseUserManager):
    def _create_user(self,email,username,password,**extra_fields):
        if not email:
            raise ValueError("The Email Must be set!!")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser = True")
        return self._create_user(email,password,**extra_fields)
class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=20)
    email=models.EmailField(unique=True,null=True)
    is_staff=models.BooleanField(ugettext_lazy('staff statas'),default=False,help_text=ugettext_lazy('Designates whether the user can log this site'))
    is_active=models.BooleanField(ugettext_lazy('active'),default=True,help_text=ugettext_lazy('Designates whether the user should br treated as active. Unselect this instead of deletion account'))
    USERNAME_FIELD='email'
    objects=MyUsermanager()
    def __str__(self):
        return self.email
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    username=models.CharField(max_length=264,blank=True,editable=False)
    picture=models.ImageField(upload_to="user_profile")
    full_name=models.CharField(max_length=264,blank=True)
    company_name=models.CharField(max_length=264,blank=True)
    address=models.TextField(max_length=300,blank=True)
    city=models.CharField(max_length=40,blank=True)
    zipcode=models.CharField(max_length=10,blank=True)
    country=models.CharField(max_length=50,blank=True)
    phone=models.CharField(max_length=20,blank=True)
    join_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username + "'s Profile'"
    def get_fully_field(self):
        fields_name=[f.name for f in self._meta.get_fields()]
        for field_mane in fields_name:
            value=geattr(self.field_mane)
            if value is None or value =='':
                return False
        return True
@receiver(post_save,sender=User)
def create_profile(sender,created,instance,**kwargs):
    if created:
        Profile.objects.create(user=instance,username=instance.username)
@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.username=instance.username
    instance.profile.save()
