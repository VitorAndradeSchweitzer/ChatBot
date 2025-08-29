from django.contrib import admin
from .models import ConversationMemory, ChatMessage, Product

admin.site.register(ChatMessage)
admin.site.register(ConversationMemory)
admin.site.register(Product)