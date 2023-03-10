from email import message
from multiprocessing import context
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView

# Create your views here.

def Register(request):
   
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for <strong>{}</strong>'.format(user))
            return redirect('/login/')
    else:
        form = UserCreationForm()
    
    context={
        'form':form
    }
    return render(request, 'register.html',context)

def Login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        info = '<strong>{}</strong>. Account was logined !'.format(user)

        messages.success(request,info)


        if user is not None:
            login(request,user)
            redirect('/')
        
        else:
            messages.success(request,'Username or password is incorrect!')
    


def LogOut(request):
    r=request.user
    logout(request)
    info = '<strong>{}</strong>. You have successfully loged out!'.format(r)
    messages.success(request,info)
    print(messages)
    return redirect('/login/')


def Home(request):
    return render(request,'Home.html')



def customhandler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response




def Main2(request):
    return render(request,'main2.html')

def Job(request):
    jobs=Jobs.objects.all()

    context={
        'jobs':jobs
    }
    return render(request,'jobs.html',context)

def Job2(request):
    jobs = BaseJob.objects.all()

    context={
        'jobs':jobs
    }
    return render(request,'job2.html',context)

def Employee(request):
    context={
        'employee':Employee1.objects.all(),
        'jobs':Jobs.objects.all(),
    }
    return render(request,'employee.html',context)

def Employee2(request):
    context={
        'employee':BaseEmployee.objects.all(),
        'jobs':BaseJob.objects.all(),
    }
    return render(request,'employee2.html',context)

def AddJob(request):
    name = request.POST['job']
    Jobs.objects.create(name=name)
    return redirect('/job/')

def BaseJobs(request):
    add_job=request.POST['basejob']
    BaseJob.objects.create(name=add_job)
    return redirect('/job2/')

def Tahrir(request):

    if request.POST:
        new_job = request.POST['job']
        new_id=request.POST['id']
        just_job=Jobs.objects.get(id=new_id)
        just_job.name=new_job
        just_job.save()
        print(new_job)
        return redirect('/job/')
    else:
        tahrir_id = request.GET.get('job')
        tahrir=Jobs.objects.get(id=tahrir_id)
        print(tahrir_id,tahrir)

        context={
            'job':tahrir,
            'jobs':Jobs.objects.all(),
        }
        return render(request,'jobs.html',context)

def BaseEdit(request,id):
    if request.method =='POST':
        baseedit=BaseJob.objects.get(id=id)
        baseedit.name=request.POST['baseedit']
        baseedit.save()
        return redirect('/job2/')

    else:      
        baseedit=BaseJob.objects.get(id=id)

        context={
            'baseedit':baseedit,
            'jobs':BaseJob.objects.all(),

        }


        return render(request,'job2.html',context)

def Ochir(request,id):
    ochir=Jobs.objects.get(id=id)
    ochir.delete()
    return redirect('/job/')

def BaseOchir(request,id):
    base_ochir=BaseJob.objects.get(id=id)
    base_ochir.delete()
    # base_ochir.save()
    return redirect('/job2/')

def Filter2(request):
    job = request.GET['job']
    employee = BaseEmployee.objects.filter(job_id=job)
    context = {
        'employee':employee,
        'works':Jobs.objects.all(),
    }
    return render(request, 'employee2.html', context)

def Filter(request):
    job = request.GET['job']
    employee = Employee1.objects.filter(job_id=job)
    context = {
        'employee':employee,
        'works':Jobs.objects.all(),
    }
    return render(request, 'employee.html', context)

def AddWorker(request):
    r=request.POST
    full_name=r['full_name']
    job=r['job']
    degree=r['degree']
    phone=r['phone']
    BaseEmployee.objects.create(full_name=full_name,job_id=job,degree=degree,phone=phone)
    
    return redirect('/employee2/')

def AddWorker1(request):
    r=request.POST
    full_name=r['full_name']
    job=r['job']
    degree=r['degree']
    phone=r['phone']
    Employee1.objects.create(full_name=full_name,job_id=job,degree=degree,phone=phone)
    
    return redirect('/employee/')
