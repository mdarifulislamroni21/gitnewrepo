from django.conf.urls import url
from django.urls import path
from User import views
urlpatterns=[
   path('registration/',views.USignUp,name='USignUp'),
   path('login/',views.USignIn,name='USignIn'),
   path('logout/',views.Signout,name='Signout'),
   path('profile/edit',views.UProfileEddid,name='UProfileEddid')
]
