from django.shortcuts import render, redirect
from .models import RegisterUser
from django.contrib.auth import logout
from django.http import HttpResponse

authorize_user = False


def dashboardPage(request):
    return render(request, "dashboard.html")

def homePage(request):
    if authorize_user:
        return render(request, "homepage.html")
    else:
        return HttpResponse("Unauthenticated user")
def loginPage(request):
    return render(request, "loginpage.html")

def handlelogin(request):
    if request.method == "POST":
        if "loginusername" in request.POST:
            loginusername = request.POST['loginusername']
            loginpassword = request.POST['loginpassword']
            user = RegisterUser.objects.filter(email=loginusername, password=loginpassword).exists()
            if user:
                authorize_user = True
                return render(request, "homepage.html")
            else:
                return render(request, "loginpage.html")
        else:
            email = request.POST['email']
            password = request.POST['password']
            cnf_password = request.POST['cnf_password']
            if password == cnf_password:
                new_user = RegisterUser.objects.create(email=email, password=password)
                return render(request, "homepage.html")
            else:
                return render(request, "loginpage.html")
    return render(request, "loginpage.html")


def forgetPasswordPage(request):
    return render(request, "forgetpassword.html")


def logoutPage(request):
    logout(request)
    return redirect('dashboard')