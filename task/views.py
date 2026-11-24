from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import *
from random import randint
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


def registraion(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            username = username,

            email = email,
            password = password,
            is_active = False
        )
        user.save()


        code = str(randint(100000, 999999))

        ConfEmail.objects.update_or_create(
            user = user,
            code = code
        )
        send_mail(
            "Hello brother please Confirm Email We are nit Hackers ve want only steal yout account",
            f"Your code is {code}",
            'norep1y@softc1ub.tj',
            [user.email]
        )
        return redirect('confirm_email')

    return render(request, "registration.html")








def confirm_email(request):
    if request.method == 'POST':
        username = request.POST.get("username")

        code = request.POST.get("code")

        user = User.objects.filter(username = username).first()
        
        code_obj = ConfEmail.objects.filter(user = user).first()
        
        if code_obj.code == code:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            return redirect("confirm_email")
    return render(request, 'confirm_email.html')


    
    

    
        
@login_required
def show_profile(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "profile.html", {"tasks": tasks})





        
@login_required
def send_message_all(request):
    if request.method == 'POST':
        users = User.objects.all()

        for user in users:
            send_mail(
                'News',
                'Hello user it reclam.',
                'norep1y@softc1ub.tj',
                [user.email]
            )

        return redirect('profile')

    return render(request, 'send_message.html')


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(request, username = data['username'], password = data['password'])
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            return redirect("login")
    return render(request, 'login.html')





@login_required
def task_create(request):
    if request.method == "POST":
        Task.objects.create(
            user = request.user,
            title = request.POST["title"],
            description = request.POST["description"],
            completed = request.POST.get("completed") == "on"
        )
        return redirect('profile')

    return render(request, "task_form.html")




@login_required
def task_detail(request, id):
    task = Task.objects.get(pk = id, user = request.user)
    return render(request, "task_detail.html", {"task": task})





@login_required
def task_update(request, id):
    task = Task.objects.get(pk = id, user = request.user)

    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST["description"]
        task.completed = request.POST.get("completed") == "on"
        task.save()
        return redirect('profile')

    return render(request, "task_edit.html", {"task": task})






@login_required
def task_delete(request, id):
    task = Task.objects.get(pk = id, user = request.user)

    if request.method == "POST":
        task.delete()
        return redirect('profile')

    return render(request, "task_delete.html", {"task": task})
