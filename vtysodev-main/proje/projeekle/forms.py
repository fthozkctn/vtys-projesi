from django import forms
from django.shortcuts import redirect
from user.models import CustomUser
from .models import Proje, Task
from django.utils import timezone

class ProjeForm(forms.ModelForm):
    class Meta:
        model = Proje
        fields = ["title", "users", "content", "ended_date"]
        widgets = {
            'users': forms.CheckboxSelectMultiple
        }
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ProjeForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['users'].queryset = CustomUser.objects.exclude (id=user.id)
            else:
                self.fields['users'].queryset = CustomUser.objects.all() 
          

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['proje', 'assignee', 'start_date', 'due_date', 'description']

    widgets = {
            'assignee': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': timezone.now().strftime('%Y-%m-%d')}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': timezone.now().strftime('%Y-%m-%d')}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    
    def __init__(self, *args, **kwargs):
        proje = kwargs.pop('proje', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if proje:
            self.fields['assignee'].queryset = proje.users.all()
            self.fields['proje'].widget.attrs['readonly'] = True
            self.initial['proje'] = proje.title
            self.fields['proje'].widget.attrs['class'] = 'form-control-plaintext'