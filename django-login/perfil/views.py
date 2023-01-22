from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django import forms
from . import models
from django.http import HttpResponse
from django.core.validators import validate_email 
from django.contrib.auth.mixins import LoginRequiredMixin 


class Login(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'perfil/login.html')
        
    def post(self,*args, **kwargs):


        usuario = self.request.POST.get('username')
        senha = self.request.POST.get('password')


        self.renderizar = render(self.request, 'perfil/login.html')

        if not usuario or not senha:
            messages.error(
                self.request,
                'Usuario ou senha invalidos.'
            )
            return redirect('login')
        
        user = authenticate(self.request, username=usuario, password=senha)

        if not user:
            messages.error(
                self.request,
                'Usuario ou senha invalidos'
            )
            return redirect('login')
        
        else:
            login(self.request, user)
            return redirect('inicialsite:dashboard')

        

    



class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')








class Cadastro(View):
    def get(self,*args, **kwargs):
        return render(self.request, 'perfil/cadastro.html')
    
    def post(self,*args, **kwargs):

        validation_error_msgss = {}

        usuario = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        password2 = self.request.POST.get('password2')    
        

        try:
            validate_email(email)
        except:
            messages.error(self.request,
            'Email invalido!')
            return render(self.request, 'perfil/cadastro.html')
        
        if len(password) < 6:
            messages.error(self.request, 'Senha precisa ter ao menos 6 digitos!')
            return render(self.request, 'accounts/cadastro.html')

        if len(usuario) < 3:
            messages.error(self.request, 'Usuario precisa ter ao menos 6 digitos!')
            return render(self.request, 'accounts/cadastro.html')

        if password != password2:
            messages.error(self.request, 'Senhas não estão iguais!!')
            return render(self.request, 'perfil/cadastro.html')
        
        if User.objects.filter(username=usuario).exists():
            messages.error(self.request, 'Usuario já existe!')
            return render(self.request, 'perfil/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(self.request, 'Email já existe!')
            return render(self.request, 'perfil/cadastro.html')

        messages.success(self.request, 'Cadastrado com sucesso!, Agora faça login.')
        user = User.objects.create_user(
            username=usuario, email=email, password=password, )
        user.save()
        self.request.session.save()
        return redirect('login')

class AtualizarPerfil(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, 'perfil/atualizar.html')
        return redirect('login')
    
    def post(self,*args, **kwargs):
        if self.request.user.is_authenticated:

            usuario = self.request.POST.get('username')
            email = self.request.POST.get('email')
            password = self.request.POST.get('password')
            password2 = self.request.POST.get('password2')    
        
            emaildb = User.objects.get(email=email)

             
            try:
             validate_email(email)
                
            except:

                messages.error(self.request,
                'Email invalido!')


                return render(self.request, 'perfil/atualizar.html')

            if password != '':
                if len(password) < 6:
                    messages.error(self.request, 'Senha precisa ter ao menos 6 digitos!')
                    return render(self.request, 'perfil/atualizar.html')

            if len(usuario) < 3:
                messages.error(self.request, 'Usuario precisa ter ao menos 6 digitos!')
                return render(self.request,'perfil/atualizar.html')

            if password != '':
                if password != password2:
                    messages.error(self.request, 'Senhas não estão iguais!!')
                    return render(self.request, 'perfil/atualizar.html')
                  
            
            if User.objects.filter(username=usuario).exists():
                messages.error(self.request, 'Usuario já existe!')
                return render(self.request, 'perfil/atualizar.html')
    
            usuariouser = get_object_or_404(
                User, username=self.request.user.username)
            usuariouser.username = usuario


            emaildb = User.objects.get(email=email)

            if password:
                usuariouser.set_password(password)
                if password == '':
                    usuariouser.password = self.request.user.password
                    
            if email != emaildb:
                usuariouser.email = email

            usuariouser.save()
            self.request.session.save()

            return redirect('logout')
             
            


class Deletarperfil(View):
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            id = self.request.user.id
            user = User.objects.get(id=id)
            user.delete()
            self.request.session.save()
    

            return redirect('login')
        return redirect('login')