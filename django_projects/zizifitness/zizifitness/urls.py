"""zizifitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('customers/', include('customers.urls', namespace='customers')),
    path('signup/', views.signup_view, name="signup"),
    path('customers/<slug:slug>/edit_profile/', views.profile, name="edit-profile"),
    path('accounting/', include('accounting.urls', namespace='accounting')),
]

from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='customers/', permanent=True)),
# ]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
