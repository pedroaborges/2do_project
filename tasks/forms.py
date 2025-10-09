from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'category', 'init_hour', 'end_hour']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-input-purple text-text-input placeholder:text-text-input/60 rounded-lg p-3 border-0 focus:ring-2 focus:ring-light-purple',
                'placeholder': 'Digite a tarefa aqui',
                'id': 'name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-input-purple text-text-input placeholder:text-text-input/60 rounded-lg p-3 border-0 focus:ring-2 focus:ring-light-purple',
                'placeholder': 'Adicione uma descrição...',
                'rows': 3,
                'id': 'description'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-input-purple text-text-input rounded-lg p-3 border-0 focus:ring-2 focus:ring-light-purple',
                'id': 'category'
            }),
            'init_hour': forms.TimeInput(attrs={
                'class': 'bg-card-purple text-white p-2 rounded-lg border-none',
                'type': 'time',
                'id': 'init_hour'
            }),
            'end_hour': forms.TimeInput(attrs={
                'class': 'bg-card-purple text-white p-2 rounded-lg border-none',
                'type': 'time',
                'id': 'end_hour'
            }),
        }

    def clean_end_hour(self):
        """Verifica se a hora de término é maior que a de início"""
        init_hour = self.cleaned_data.get('init_hour')
        end_hour = self.cleaned_data.get('end_hour')

        if init_hour and end_hour and end_hour < init_hour:
            raise forms.ValidationError('A hora de término deve ser posterior à hora de início.')
        return end_hour