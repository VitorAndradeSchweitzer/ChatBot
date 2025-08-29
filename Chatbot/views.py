from django.shortcuts import render
from django.views.generic import TemplateView

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import  login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import json


from . import chatbot_utils
from .forms import RegisterForm, LoginForm
from .models import ConversationMemory, ChatMessage
class Init(TemplateView):
    template_name = "pages/init.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
        
    def post(self, request):
        context = self.get_context_data()
        user_input = request.POST.get("user_input", "")
        context['inicio'] = True
                
        if user_input:
    
            #response = chatbot_utils.chatbot_generate_response(user_input)
            response = {}
            context['response'] = response
            context['user_input'] = user_input
            context['number'] = [1] * 15
            
        return render(request, self.template_name, context )
    def get(self, request):
        context = self.get_context_data()
        context['number'] = [1] * 15
        context['inicio'] = True
        return render(request, self.template_name, context )
    
    
    

class Register(TemplateView):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            user.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('Chatbot:login')
        else:
            return render(request, 'pages/registration/register.html', {'errors': form.errors})
    
    def get(self, request):
        return render(request, 'pages/registration/register.html')


class Login(TemplateView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)  # Função nativa do Django para login
            return redirect('Chatbot:home')
        return render(request, 'pages/registration/login.html', {'form': form})

    def get(self, request):
        form = LoginForm()
    
        return render(request, 'pages/registration/login.html', {'form': form})
    

class home(TemplateView):
    template_name = "pages/home.html"
    

        
    def get(self, request):
        context = self.get_context_data()
        conversation_id = request.GET.get("conversation_id", '')
        if conversation_id:
            conversation = get_object_or_404(ConversationMemory, user=request.user.id, id=conversation_id)
            messages = ChatMessage.objects.filter(conversation=conversation).order_by('created_at')
        
            context['conversation'] = conversation

            context['messages'] = messages
        
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.get_context_data()
        conversation_id = request.GET.get("conversation_id", 0)
        user_message = request.POST.get('user_message')
        
        if user_message:
            conversation, _ = ConversationMemory.objects.get_or_create(user=request.user, id=conversation_id)
            messages = ChatMessage.objects.filter(conversation=conversation.id).order_by('created_at')
            response = chatbot_utils.generate_response_with_summary(conversation, user_message)
            
            context['conversation'] = conversation
            context['messages'] = messages
        else:
            print("no bitches")
        return render(request, self.template_name, context)
        
