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
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from datetime import datetime, date
import json
from django.http import HttpResponse
from .models import EmailVerification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tasks import send_async_email

@method_decorator(login_required(login_url='login'), name='dispatch')
class VerificarEmailView(View):
    def get(self, request, token):
        
        verification = get_object_or_404(EmailVerification, token=token)

        if verification.is_expired():
            return render(request, "email_message.html", {
                'message': "Este link de verificação expirou."
            })

        if verification.is_verified:
            return render(request, "email_message.html", {
                'message': "Este e-mail já foi verificado."
            })

        verification.is_verified = True
        user = User.objects.get(username=verification.user)
        user.email = verification.temp_email
        user.save()
        verification.save()

        return render(request, "email_message.html", {
                'message': "E-mail verificado com sucesso!"
            })

@method_decorator(login_required(login_url='login'), name='dispatch')
class EnviarEmailView(View):
    def post(self, request):
        email = request.POST.get('email')

        user = request.user

        if User.objects.filter(email=email):
            return render(request, "email_message.html", {
                'message': "E-mail ja cadastrado."
            })

        token = EmailVerification.generate_token()

        verification, created = EmailVerification.objects.get_or_create(user=user)
        verification.temp_email = email
        verification.token = token
        verification.is_verified = False
        verification.save()

        current_site = get_current_site(request)
        verification_url = f"https://62c9c2461d45.ngrok-free.app/verify-email/{token}/"

        subject = 'Verifique seu e-mail'
        message = render_to_string('email_verification.html', {
            'user': user,
            'verification_url': verification_url,
        })

        send_async_email(subject, message, [email])

        return render(request, "email_message.html", {
            'message': "E-mail de verificação enviado."
        })

    def get(self, request):
        return render(request, 'enviar_email_verificacao.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', {})
    
    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if User.objects.filter(username=username): # verifies if the username already exists
                raise Exception('Nome de usuário existente!')

            user = User.objects.create_user(username=username, password=password)
            user.save()

            login(request, user)

            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('enviar_email_verificacao')
        except Exception as e:
            messages.error(request, str(e))
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

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        
        response = super().form_valid(form)

        dateT_end = datetime.combine(date.today(), form.instance.end_hour)

        clocked_end, _ = ClockedSchedule.objects.get_or_create(clocked_time=dateT_end)

        PeriodicTask.objects.create(
            clocked=clocked_end,
            one_off=True,
            name=f"deactive task {form.instance.id}",
            description=form.instance.name,
            task='tasks.tasks.deactive_task',
            args=json.dumps([form.instance.id])
        )

        return response

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ['Trabalho', 'Esportes', 'Estudos', 'Lazer']
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class TasksDeleteView(DeleteView): # Delete View (DELETE)
    model = Task
    template_name = 'deleteTask.html'
    success_url = '/'