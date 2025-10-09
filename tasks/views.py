from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views import View
from datetime import datetime
from .forms import TaskForm
from .models import Task

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', {})
    
    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username): # verifies if the username already exists
                raise

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('login')
        except:
            messages.error(request, 'Nome de usuário existente!')
            return redirect('register')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    
    def post(self, request):
        try:
            username = request.POST.get('uname')
            password = request.POST.get('pass')

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('home')
        except:
            messages.error(request, 'Usuário ou senha incorreto(s).')
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            return redirect('login')
        except:
            messages.error(request, 'Usuário não logado.')
            return redirect('home')

@method_decorator(login_required(login_url='login'), name='dispatch')
class TasksListView(ListView): # List View (GET)
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(owner=user)

        query = self.request.GET.get('search')

        if query: # filters based on user's search
            queryset = queryset.filter(Q(name__icontains=query))

        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()

        total = tasks.count()
        done = tasks.filter(status=True).count()
        percentage = (done / total * 100) if total > 0 else 0

        month_name = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

        context['month'] = month_name[datetime.today().month-1]
        context['day'] = datetime.today().day

        context['search'] = self.request.GET.get('search', '')

        context['percentage'] = round(percentage, 2)
        context['total'] = total
        context['done'] = done
        
        return context
    
    def post(self, request, *args, **kwargs): # Mark task as completed or not
        task_id = request.POST.get('task_id')
        if task_id:
            task = get_object_or_404(Task, id=task_id, owner=request.user)
            task.status = not task.status
            task.save()
        return redirect('home')

@method_decorator(login_required(login_url='login'), name='dispatch')
class TasksCreateView(CreateView): # Create View (POST)
    model = Task
    form_class = TaskForm
    template_name = 'newTask.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class TasksDetailView(DetailView): # Detail View (RETRIEVE)
    model = Task
    template_name = 'detailTask.html'

@method_decorator(login_required(login_url='login'), name='dispatch')
class TasksUpdateView(UpdateView): # Update View (PUT)
    model = Task
    form_class = TaskForm
    template_name = 'updateTask.html'
    context_object_name = 'task'
    success_url = '/'

@method_decorator(login_required(login_url='login'), name='dispatch')
class TasksDeleteView(DeleteView): # Delete View (DELETE)
    model = Task
    template_name = 'deleteTask.html'
    success_url = '/'