from django.shortcuts import render, redirect
from .models import RegisterUser
from django.contrib.auth import logout
from django.http import HttpResponse
from prediction_file.prediction import rfClassifier, LRClassifier, GBClassifier, KNNClassifier
import hashlib
import smtplib

forget_email = ""
authorize_user = False



def dashboardPage(request):
    return render(request, "dashboard.html")

def homePage(request):
    global authorize_user
    try:
        if authorize_user:
            return render(request, "homepage.html")
        else:
            return HttpResponse("Unauthenticated user")
    except Exception as e:
        return HttpResponse(e.args[0])

def loginPage(request):
    return render(request, "loginpage.html")

def handlelogin(request):
    global authorize_user
    try:
        if request.method == "POST":
            if "loginusername" in request.POST:
                loginusername = request.POST['loginusername']
                loginpassword = request.POST['loginpassword']
                encMessage = hashlib.sha1(loginpassword.encode())
                user = RegisterUser.objects.filter(email=loginusername, password=encMessage.hexdigest()).exists()
                if user:
                    authorize_user = True
                    return render(request, "homepage.html")
                else:
                    msg = "Incorrect email or password"
                    return render(request, "loginpage.html", {"msg": msg})
            else:
                email = request.POST['email']
                password = request.POST['password']
                cnf_password = request.POST['cnf_password']
                if password == cnf_password:
                    encMessage = hashlib.sha1(password.encode())
                    new_user = RegisterUser.objects.create(email=email, password=encMessage.hexdigest())
                    if new_user:
                        msg = "User successfully Registered"
                        return render(request, "loginpage.html", {"msg": msg})
                else:
                    msg = "User successfully Registered"
                    return render(request, "loginpage.html", {"msg": msg})
        return render(request, "loginpage.html")
    except Exception as e:
        return HttpResponse(e.args[0])


def resultPage(request):
    result = {}
    classifier_list = ["Random Forest Classifier", "Logistic Regression", "SVM",
                       "Gradient Boosting", "KNN Classifier", "All"]
    try:
        if request.method == "POST":
            text = request.POST["textfield"]
            radio_btn = int(request.POST.get("dropdown", 0))

            if radio_btn == 5:
                result["Gradient Boosting"] = GBClassifier(text)
                result["Logistic Regression"] = LRClassifier(text)
                result["KNN Classifier"] = KNNClassifier(text)
                result["Random Forest Classifier"] = rfClassifier(text)
            elif radio_btn == 3:
                result[classifier_list[radio_btn]] = GBClassifier(text)
            elif radio_btn == 1:
                result[classifier_list[radio_btn]] = LRClassifier(text)
            elif radio_btn == 4:
                result[classifier_list[radio_btn]] = KNNClassifier(text)
            else:
                result[classifier_list[radio_btn]] = rfClassifier(text)
        return render(request, "homepage.html", {"result": result})
    except Exception as e:
        return HttpResponse(e.args[0])



def forgetPasswordPage(request):
    return render(request, "forgetpassword.html")

def logoutPage(request):
    global authorize_user
    if authorize_user:
        authorize_user = False
        logout(request)
    return redirect('login')

def aboutUs(request):
    global authorize_user
    try:
        if authorize_user:
            return render(request, "about.html")
        else:
            return HttpResponse("Unauthenticated user")
    except Exception as e:
        return HttpResponse(e.args[0])

def handleforgetPassword(request):
    global forget_email
    if request.method == "POST":
        email = request.POST["email"]
        forget_email = email
        print(email)
        # s = smtplib.SMTP('smtp.gmail.com', 587)
        # s.starttls()
        # msg = email.message.Message()
        # msg['Subject'] = 'Reset Password Link'
        # msg['From'] = 'Verification email'
        # msg['To'] = email
        # msg.add_header('Content-Type', 'text/html')
        # msg.set_payload("""
        #         This is the verified message from Rasa-ChatBot for Authorized status. Click the below link
        #         to visit your account.<br>
        #         http://127.0.0.1:8000/resetpassword/.
        #         This message is from CHATBOT-RASA powered by Musa.<br>
        #         For more Information contact at abc@gmail.com
        #         """)
        # s.login("", "")
        # s.sendmail(msg['From'], [msg['To']], msg.as_string())
        # s.quit()

        msg = """
                    This message is only for registered user.
                    Reset Password link sent to your register email account. 
                """
        return render(request, "forgetpassword.html", {"msg": msg})
def resetPass(request):
    return render(request, "newpass.html")

def postResetPass(request):
    global forget_email
    if request.method == "POST":
        passw = request.POST["password"]
        cnf_pass = request.POST["cnf_password"]

        if passw == cnf_pass:
            encMessage = hashlib.sha1(passw.encode())
            new_user = RegisterUser.objects.update(email=forget_email, password=encMessage.hexdigest())
            if new_user:
                msg = "successfully password changes"
                return render(request, "loginpage.html", {"msg": msg})
            else:
                msg = "user not registeres"
                return render(request, "newpass.html", {"msg": msg})
        else:
            msg = "password not matched"
            return render(request, "newpass.html", {"msg": msg})

