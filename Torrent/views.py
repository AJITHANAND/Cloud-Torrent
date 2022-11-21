from django.shortcuts import render
import hashlib
from .forms import *
from django.http import JsonResponse


def encrypt(password: str):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


# Create your views here.
def homepage(request):
    return render(request, 'landing/index.html')


def dashboard(request):
    return render(request, 'torrent/index.html')


def login(request):
    if request.method == "POST":
        print(request.body)
        return render(request, 'login/login.html')
    elif request.method == "GET":
        return render(request, 'login/login.html')


def signup(request):
    if request.method == "POST":
        usercreate(request)
    return render(request, 'login/Signup.html')


def usercreate(request):
    form = Register(request.POST)
    print(request.POST)
    if form.is_valid():
        # form.save()
        obj = {'status': True}
        return JsonResponse(obj, status=200)
    else:
        obj = {'status': False}
        return JsonResponse(obj, status=406)
