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
    """
    "When the user requests the dashboard page, render the dashboard.html template."
    
    The render function takes two arguments: the request object and the name of the template to render
    
    :param request: The request is an HttpRequest object. It contains metadata about the request
    :return: The dashboard.html file is being returned.
    """
    return render(request, "dashboard.html")


def homePage(request):
    """
    If the user is authorized, render the homepage.html template. Otherwise, return an error message
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request
    :return: The homePage function is returning a render of the homepage.html file.
    """
    global authorize_user
    try:
        if authorize_user:
            return render(request, "homepage.html")
        else:
            return HttpResponse("Unauthenticated user")
    except Exception as e:
        return HttpResponse(e.args[0])


def loginPage(request):
    """
    It takes a request object as an argument, and returns a rendered template called "loginpage.html"
    
    :param request: This is the request object that is sent to the view
    :return: The login page is being returned.
    """
    return render(request, "loginpage.html")


def handlelogin(request):
    """
    It takes a request object as input, and returns a response object
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: the response of the request.
    """
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
    """
    It takes the text from the textfield and the radio button value from the dropdown and then calls the
    appropriate function to classify the text
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: The result is being returned.
    """
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
                result["SVM"] = rfClassifier(text)
            elif radio_btn == 3:
                result[classifier_list[radio_btn]] = GBClassifier(text)
            elif radio_btn == 1:
                result[classifier_list[radio_btn]] = LRClassifier(text)
            elif radio_btn == 4:
                result[classifier_list[radio_btn]] = KNNClassifier(text)
            elif radio_btn == 2:
                result[classifier_list[radio_btn]] = rfClassifier(text)
            else:
                result[classifier_list[radio_btn]] = rfClassifier(text)
        return render(request, "homepage.html", {"result": result})
    except Exception as e:
        return HttpResponse(e.args[0])



def forgetPasswordPage(request):
    """
    It renders the forgetpassword.html page
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    such as the HTTP method, host, path, and more
    :return: the render of the forgetpassword.html page.
    """
    return render(request, "forgetpassword.html")


def logoutPage(request):
    """
    If the user is logged in, log them out and redirect them to the login page
    
    :param request: The request is an HttpRequest object
    :return: the redirect function.
    """
    global authorize_user
    if authorize_user:
        authorize_user = False
        logout(request)
    return redirect('login')


def aboutUs(request):
    """
    If the user is authorized, render the about.html page.
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request
    :return: The aboutUs function is returning the about.html page.
    """
    global authorize_user
    try:
        if authorize_user:
            return render(request, "about.html")
        else:
            return HttpResponse("Unauthenticated user")
    except Exception as e:
        return HttpResponse(e.args[0])


def handleforgetPassword(request):
    """
    It takes the email address from the user, sends a reset password link to the email address, and then
    renders the forgetpassword.html page with a message
    
    :param request: The initial request object sent from the browser
    :return: the render function.
    """
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
    """
    It renders the newpass.html template
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method, host, path, and more
    :return: The newpass.html file is being returned.
    """
    return render(request, "newpass.html")


def postResetPass(request):
    """
    If the request method is POST, then get the password and confirm password from the request, and if
    they match, then update the password in the database
    
    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: the render function.
    """
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

