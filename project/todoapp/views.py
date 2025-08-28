from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
# Create your views here.

def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()
    return render(request, 'todoapp/todo.html', {})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Senha muito curta!')
            return redirect('register')
        
        get_all_users_username = User.objects.filter(username=username)

        if get_all_users_username:
            messages.error(request, 'Erro, nome já existente!')
            return redirect('register')

        new_user = User.objects.create_user(username = username, email = email, password = password)
        new_user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login') 
    return render(request, 'todoapp/register.html', {})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username = username, password = password)

        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Erro, usuário não existe!')
            return redirect('login')            

    return render(request, 'todoapp/login.html', {})

