
from django import forms
from .models import Task


class Task_form(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asigna titulo de tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe tu tarea'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
        }
