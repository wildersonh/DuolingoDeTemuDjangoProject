from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaskForm
from .models import Task
from .models import Certificado
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html', {'user':request.user})

def signup(request):
    if request.method == 'GET':
        print('Enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']: 
            try:
                #registrer users
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError: 
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Cotraseña no coinciden'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datacompleted__isnull=True)
    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datacompleted__isnull=False).order_by('-datacompleted')
    return render(request, 'tasks.html',{
        'tasks': tasks
    })

@login_required
def create_tasks(request):
    if request.method == 'GET':
        return render(request, 'create_tasks.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_tasks = form.save(commit=False)
            new_tasks.user = request.user
            new_tasks.save()
            return redirect('tasks')
        except ValueError:

            return render(request, 'create_tasks.html', {
                'form': TaskForm,
                'error': 'No se guardo correctamente'
            })

@login_required
def tasks_details(request, task_id):
    if request.method == 'GET':
        tasks = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=tasks)
        return render(request, 'task_details.html', {'tasks': tasks, 'form': form})
    else:
        try: 
            tasks = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=tasks)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_details.html', {'tasks': tasks, 'form': form, 'error': 'Error actualizando'})
             
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datacompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html',{
            'from': AuthenticationForm,
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'iniciar_sesion.html',{
                'from': AuthenticationForm,
                'error': 'Usuario o Contraseña es incorrecto'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required     
def completar(request):
    return render(request, 'completar.html')

@login_required
def preguntas(request):
    return render(request, 'preguntas.html')

@login_required
def certificado(request):
    return render(request, 'certificado.html', {
        'usuario': request.user,
        'certificado': Certificado
    })