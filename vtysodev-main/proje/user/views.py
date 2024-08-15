from django.shortcuts import render,redirect

from user.models import CustomUser
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        newUser = CustomUser.objects.create_user(
            username,
            email,
            password,
            )
        login(request, newUser)
        messages.info(request, "Başarıyla Kayıt Oldunuz...")
        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "register.html", context)

def loginUser(requset):
    form = LoginForm(requset.POST or None)
    context = {
        "form" : form 
    }
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if user is None:
            messages.info(requset, "Kullanıcı Adı veya Parola hatalı")
            return render(requset, "login.html", context)
        messages.info(requset, "Başarıyla Giriş Yaptınız")
        login(requset,user)
        return redirect("index")
    return render(requset, "login.html",context)
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıylı Çıkış Yapıldır")
    return redirect("index")

def user_list(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'userlist.html', context)
