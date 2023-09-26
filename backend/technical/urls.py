"""technical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from technical.views import login, logged_in, user_info, logout, unstructured

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login, name="login"),
    path('logged_in', logged_in, name="logged_in"),
    path('unstructured', unstructured, name="unstructured"),
    path('user_info', user_info, name="user_info"),
    path('logout', logout, name="logout")
]
