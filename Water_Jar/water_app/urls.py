"""Water_Jar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('savewater/', views.savewater, name='savewater'),
    path('edit/', views.edit, name='edit'),
    path('editcost/', views.editcost, name='editcost'),
    path('jarhistory/', views.jarhistory, name='jarhistory'),
    path('entry/', views.entry, name='entry'),

    # path('editcost/', views.editcost, name='editcost'),
]
