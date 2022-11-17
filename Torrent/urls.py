from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.homepage, name="homepage"),
    path('login', views.login, name='login'),
]
