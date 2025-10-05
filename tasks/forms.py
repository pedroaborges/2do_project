from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean_end_hour(self): # verifies if the end hour is greater than the init hour
        init_hour = self.cleaned_data.get('init_hour')
        end_hour = self.cleaned_data.get('end_hour')

        if end_hour < init_hour:
            self.add_error('end_hour', 'Valor inválido.')
        
        return end_hour