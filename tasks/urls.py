from .views import RegisterView, LoginView, LogoutView, TasksListView, TasksCreateView, TasksDetailView, TasksUpdateView, TasksDeleteView, EnviarEmailView, VerificarEmailView
from django.urls import path

urlpatterns = [
    path('', TasksListView.as_view(), name='home'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('task/new/', TasksCreateView.as_view(), name='new'),
    path('task/<int:pk>/delete/', TasksDeleteView.as_view(), name='delete'),
    path('task/<int:pk>/update/', TasksUpdateView.as_view(), name='update'),
    path('task/<int:pk>/detail/', TasksDetailView.as_view(), name='detail'),

    path('enviar-email-verificacao/', EnviarEmailView.as_view(), name='enviar_email_verificacao'),
    path('verify-email/<str:token>/', VerificarEmailView.as_view(), name='verificar_email'),
]