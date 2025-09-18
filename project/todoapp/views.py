from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        
        if task:
            new_todo = todo(user=request.user, todo_name=task)
            new_todo.save()
        else:
            messages.error(request, ' ')
        
        # Adicione este redirecionamento para evitar duplicação
        return redirect('home-page')

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
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
    if request.user.is_authenticated:
        return redirect('home-page')
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

def LogoutView(request):
    logout(request)
    return redirect('login')

@login_required
def delete_task(request, name):
    todo.objects.filter(user=request.user, todo_name=name).delete()
    
    #messages.success(request, 'Tarefa(s) excluída(s) com sucesso!')
    
    return redirect('home-page')

@login_required
def Update(request,id):
    get_todo = todo.objects.get(id=id)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

