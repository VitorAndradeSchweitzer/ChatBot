
from django.urls import path, include
from . import views
app_name = "Chatbot"
urlpatterns = [
   path('', views.Init.as_view(), name="init"),
   path('register/', views.Register.as_view(), name='register'),
   path('login/', views.Login.as_view(), name='login'),
   
   path('home', views.home.as_view(), name="home")
]
