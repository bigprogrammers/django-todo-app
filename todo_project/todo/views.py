from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from .models import Todo

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo_list.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Todo.objects.create(user=request.user, title=title)
    return redirect('todo_list')

@login_required
def mark_complete(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')

@login_required
def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('todo_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    django_logout(request)
    return redirect('login')