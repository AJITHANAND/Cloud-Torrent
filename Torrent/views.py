from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import hashlib
from .forms import *
from django.http import JsonResponse, HttpResponse


def encrypt(password: str):
    password = "Qwerty@123"
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


# Create your views here.
def homepage(request):
    return render(request, 'landing/index.html')


def dashboard(request):
    return render(request, 'torrent/index.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = encrypt(request.POST.get('password'))
        try:
            obj = user.objects.get(email=email, password=password)
        except ObjectDoesNotExist:
            return render(request, 'login/login.html', {'err': True})
        request.session['userid'] = obj.id
        return render(request, 'torrent/index.html', )
    elif request.method == "GET":
        return render(request, 'login/login.html')


def signup(request):
    return render(request, 'login/Signup.html')


def usercreate(request):
    # name = request.POST.get('username')
    # email = request.POST.get('email')
    # password = encrypt(request.POST.get('password'))
    # form = Register({name:name, email:email,password:password})
    form = Register(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.password = encrypt(form.password)
        form.save()
        obj = {'status': True}
        return HttpResponse(request, obj, status=200)
    else:
        obj = {'status': False}
        return HttpResponse(obj, status=406)
