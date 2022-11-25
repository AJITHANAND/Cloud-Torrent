from django.core.exceptions import ObjectDoesNotExist
import hashlib
from .forms import *
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .decorators import *
from Engine.add_queue import add_to_queue, get_client

def encrypt(password: str):
    password = "Qwerty@123"
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


def homepage(request):
    return render(request, 'landing/index.html')


@useronly
def dashboard(request):
    id = request.session.get('userid')
    obj = user.objects.get(id=id)
    return render(request, 'torrent/index.html', {'user': obj})


def login(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = encrypt(request.POST.get('password'))
        try:
            obj = user.objects.get(email=email, password=password)
        except ObjectDoesNotExist:
            return render(request, 'login/login.html', {'err': True})
        request.session['userid'] = obj.id
        return redirect('dashboard')
    elif request.method == "GET":
        return render(request, 'login/login.html')


def logout(request):
    request.session.flush()
    return redirect('login')


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


def add_torrent(request):
    link = request.POST.get('link')
    torrent = get_client()
    print(add_to_queue(torrent, link))
    return HttpResponse(request, status=200)
