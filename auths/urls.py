from django.urls import path
from auths import views

app_name = 'auths'

urlpatterns = [
    path('', views.index, name='index'),
    path('authentication/', views.authentication, name='authentication'), 
    path('logout/', views.logout, name='logout'),   
]
