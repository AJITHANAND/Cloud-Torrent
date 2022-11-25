from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.homepage, name="homepage"),
    path('login', views.login, name='login'),
    path('singup', views.signup, name='signup'),
    path('create', views.usercreate, name='create'),
    path('logout', views.logout, name='logout'),
    path('add', views.add_torrent, name="add"),
    path('refresh', views.refresh_torrent, name='refresh'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
