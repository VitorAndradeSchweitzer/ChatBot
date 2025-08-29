from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ConversationMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memory = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ("human", "Usuário"),
        ("ai", "Assistente"),
    )

    conversation = models.ForeignKey(ConversationMemory, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=450)
    price = models.FloatField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(default=None, null=True)
    
    def __str__(self):
        return self.name
        