from django.shortcuts import render, redirect
from .models import RegisterUser
from django.contrib.auth import logout
from django.http import HttpResponse
from prediction_file.prediction import get_prediction_rf


global authorize_user


def dashboardPage(request):
    return render(request, "dashboard.html")

def homePage(request):
    global authorize_user
    if authorize_user:
        return render(request, "homepage.html")
    else:
        return HttpResponse("Unauthenticated user")
def loginPage(request):
    return render(request, "loginpage.html")

def handlelogin(request):
    global authorize_user
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
                if new_user:
                    return render(request, "loginpage.html")
            else:
                return render(request, "loginpage.html")
    return render(request, "loginpage.html")


def resultPage(request):
    result = {}
    classifier_list = ["Random Forest Classifier", "Logistic Regression", "SVM",
                       "Gradient Boosting", "KNN Classifier", "All"]
    if request.method == "POST":
        text = request.POST["textfield"]
        radio_btn = int(request.POST["flexRadioDefault"])

        if radio_btn == 5:
            pass
        else:
            result[classifier_list[radio_btn]] = get_prediction_rf(text, radio_btn)
    return render(request, "homepage.html", {"result": result})



def forgetPasswordPage(request):
    return render(request, "forgetpassword.html")

def logoutPage(request):
    global authorize_user
    authorize_user = False
    logout(request)
    return redirect('login')