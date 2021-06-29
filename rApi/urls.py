from django.urls import path
from rApi import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('searchByUserName/', views.SearchByName),
    path('searchByUserPhoneNumber/', views.SearchByPhoneNumber),
    path('markTheNumberSpam/', views.MarkNumberSpam),
    path('registration/', views.Registation),
     path('login/', obtain_auth_token),
    
]