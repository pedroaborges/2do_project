from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from .serializers import TaskSerializer
from rest_framework import permissions
from rest_framework import viewsets
from .models import Task

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
@extend_schema(tags=['Tarefas'])
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated] # verifies if the user is logged in

    queryset = Task.objects.none()
    serializer_class = TaskSerializer
    pagination_class = Pagination

    def get_queryset(self): # gets just user's tasks, not all
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer): # saves user's tasks correctly
        serializer.save(owner=self.request.user)