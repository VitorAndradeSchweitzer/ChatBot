from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='Usuário')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Esse nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse email já está cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Usuário ou senha incorretos.")
            self.user = user

        return cleaned_data