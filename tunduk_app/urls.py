"""tunduk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    #path('test_request', views.test_request, name = 'test_request'),
    path('send_request_template/<int:service_id>', views.send_request_template, name = 'send_request_template'),
    path('send_request/<int:service_id>', views.send_request, name = 'send_request'),
    path('pdf/', views.pdf, name = 'pdf'),
    path('logout_request/', views.logout_request, name = 'logout_request'),
    path('login/', views.user_login, name = 'user_login'),
]
