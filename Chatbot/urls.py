
from django.urls import path, include
from . import views
app_name = "Chatbot"
urlpatterns = [
   
   path('api/teste2', views.APIendpointteste2.as_view(), name="teste2"),
   
   path('', views.Init.as_view(), name="init")
]
