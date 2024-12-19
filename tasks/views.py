from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Task_form
from .models import Task
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


@login_required
def tasks(request):

    # pylint: disable=no-member
    Tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    # print(Tasks)
    return render(request, 'tasks.html', {
        'tasks': Tasks
    })


@login_required
def tasks_completed(request):
    # pylint: disable=no-member
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


@login_required
def create_Tasks(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': Task_form
        })
    else:
        try:
            form = Task_form(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': Task_form,
                'error': 'Por favor validar los datos ingresado'
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = Task_form(instance=task)
        return render(request, 'tasks_detail.html', {
            'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = Task_form(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_detail.html', {
                'task': task, 'form': form, 'error': 'Se presenta un error al actualizar la tarea'})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')


@login_required
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
