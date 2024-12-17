from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Task_form

from django.http import HttpResponse

# Create your views here.


# Funcion para ver la vista home
def home(request):
    return render(request, 'home.html')

# funcion para ver la vista signup.html


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ingresado ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'La contraseña ingresada no coinciden'
        })


def tasks(request):
    return render(request, 'tasks.html')


def create_Tasks(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': Task_form
        })
    else:
        print(request.POST)
        return render(request, 'create_task.html', {
            'form': Task_form})


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'el usuario y/o la contraseña son incorrectas '
            })
        else:
            login(request, user)
    return redirect('tasks')
