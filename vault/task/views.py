from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib import messages


# Create your views here.

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task has been saved to SQLite3')
            return redirect('add_task')
    else:
        form = TaskForm()

    search = request.GET.get('search')
    if search:
        data = Task.objects.filter(user=request.user, task_name__icontains=search)
    else:
        data = Task.objects.filter(user=request.user)

    context = {'data': data, 'form': form}
    return render(request, 'task/add_task.html', context)

@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request,'Task removed from SQLite3')
    return redirect('add_task')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task has been updated')
            return redirect('add_task')
    else:
        form = TaskForm(instance=task)

    context = {'form': form, 'task': task}
    return render(request, 'task/edit_task.html', context)