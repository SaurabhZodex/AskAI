from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('upload/', views.upload_files, name='upload_files'),
    path('selectRepo/', views.select_repo, name='select_repo'),
    path('askQuestion/', views.ask_question, name='ask_question'),  
    path('send_answer/', views.send_answer, name='send_answer'),
]
