from django.urls import path


from . import views

# app_name = "account_app"

urlpatterns = [
    path('', views.dashboardPage, name='dashboard'),
    path('home/', views.homePage, name='home'),
    path('login/', views.loginPage, name='login'),
    path('forgetpassword/', views.forgetPasswordPage, name='forgetpassword'),

    path('handlelogin/', views.handlelogin, name='handlelogin'),
    path('result/', views.resultPage, name='result'),
    path('logout/', views.logoutPage, name='logout'),
    path('aboutus/', views.aboutUs, name='aboutus'),
    path('resetpassword/', views.resetPass, name='resetpass'),
    path('handleforget/', views.handleforgetPassword, name='handleforgetpassword'),
    path('postresetpassword/', views.postResetPass, name='postresetpass'),
]