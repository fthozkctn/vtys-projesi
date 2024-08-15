from django.shortcuts import HttpResponse,redirect
from django.shortcuts import render, get_object_or_404

from .forms import ProjeForm, TaskForm
from django.contrib import messages
from .models import Proje, CustomUser
from .models import Task
from django.utils import timezone

def projeler(request):
    projeler = Proje.objects.filter(user = request.user)
    uye_projeleri = Proje.objects.filter(users=request.user)
    context = {
        "projeler":projeler,
        "uye_projeleri":uye_projeleri,
    }
    return render(request, "projeler.html", context)

def index(request):
    projeler = Proje.objects.all()
    context = {"projeler": projeler}
    return render(request, "index.html", context)

def projeEkle(request):
    form = ProjeForm(request.POST or None)

    if form.is_valid():
        proje = form.save(commit=False)
        proje.user = request.user
        proje.save()
        form.save_m2m()
        
        messages.success(request, "Proje başarıyla oluşturuldu")
        return redirect("index")

    return render(request,"proje_ekle.html",{"form":form})
def detail(request, id):
    proje = get_object_or_404(Proje, id=id)
    return render(request, "detail.html",{"proje":proje})

def userDetail(request, id):
    customuser = get_object_or_404(CustomUser, id=id)
    assigned_tasks = customuser.assigned_tasks.all()
    current_datetime = timezone.now()
    completed_tasks = 0
    delayed_tasks = 0
    for task in assigned_tasks:
        if task.status == 'Tamamlandı':
            completed_tasks += 1
        elif task.due_date <= current_datetime:
            delayed_tasks += 1

    context =   {"customuser" : customuser, "assigned_tasks" : assigned_tasks, "completed_tasks" : completed_tasks, "delayed_tasks" : delayed_tasks}
    return render(request, "userdetail.html", context)
          

def uyegoster(request):
    uye = Proje.members.all()
    context = {"uye": uye}
    return render(request, "detail.html", context)

def updateProje(request, id):
    proje = get_object_or_404(Proje, id=id )
    form = ProjeForm(request.POST or None, request.FILES or None, instance = proje)
    if form.is_valid():
        proje = form.save(commit=False)
        proje.user = request.user
        proje.save()
        
        messages.success(request, "Proje'yi başarıyla güncellediniz")
        return redirect("index")
    
    return render(request, "updateproje.html", {"form" : form})

def deleteProje(request, id):
    proje = get_object_or_404(Proje, id=id)
    proje.delete()
    messages.success(request, "Proje başarıyla silindi")
    return redirect("projeler")


def createTask(request, id):
    proje = get_object_or_404(Proje, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, proje=proje)
        if form.is_valid():
            task = form.save(commit=False)
            task.proje = proje
            task.save()
            task.update_status()
            return redirect('index')
    else:
        form = TaskForm(proje=proje)
    return render(request, 'create_task.html', {'form': form, 'proje': proje})

def taskDetail(request, id):
    customuser = get_object_or_404(CustomUser, id=id)
    assigned_tasks = customuser.assigned_tasks.all()
    current_datetime = timezone.now()
    for task in assigned_tasks:
        if task.due_date < current_datetime and task.status != 'Tamamlandı':
            task.status = 'Gecikti'
            task.save()
        if current_datetime > task.start_date and task.status != 'Tamamlandı' and task.due_date > current_datetime:
            task.status = 'Devam Ediyor'
            task.save()
        if current_datetime < task.start_date and task.status != 'Tamamlandı':
            task.status = 'Tamamlancak'
            task.save()

        if task.status == 'Tamamlandı':
            pass

    return render(request, "görevlerim.html", {"assigned_tasks" : assigned_tasks, "task.status" : task.status})

def taskDetailProje(request, id):
    proje = get_object_or_404(Proje, id=id)
    tasks = proje.tasks.all()
    return render(request, "detail.html", {"tasks" : tasks, "proje": proje})


def submitTask(request, id):
    task = get_object_or_404(Task, id=id)
    task.status = 'Tamamlandı'
    task.save()
    proje = task.proje
    proje.ended_date += timezone.timedelta(days=1)
    proje.save_without_update()
    messages.success(request, "Görev Tamamlandı Olarak İşaretlendi")
    return redirect('görevlerim', id=task.assignee.id)

