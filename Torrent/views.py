import json

from django.core.exceptions import ObjectDoesNotExist
import hashlib
from .forms import *
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .decorators import *
from Engine.add_queue import add_to_queue, get_client, get_status, delete_torrrent


def refresh_torrent(request):
    userid = request.session.get('userid')
    torrents = torrent.objects.filter(userid=userid).values()
    torrent_client = get_client()
    for i in torrents:
        info = get_status(torrent_client, i['hash'])
        obj = torrent.objects.get(hash=i['hash'])
        obj.name = info['name']
        obj.hash = info['hash']
        obj.size = int(info['total_size'])
        obj.downloads = int(info['downloaded'])
        obj.progress = float(info['progress']) * 100
        obj.userid = user.objects.get(id=userid)
        obj.save()
    return HttpResponse(request, status=200)


def encrypt(password: str):
    password = "Qwerty@123"
    return hashlib.sha512(password.encode('utf-8')).hexdigest()


def homepage(request):
    return render(request, 'landing/index.html')


@useronly
def dashboard(request):
    id = request.session.get('userid')
    obj = user.objects.get(id=id)
    torrents = torrent.objects.filter(userid=obj.id).values()
    for i in torrents:
        i['size'] = round(float(i['size']) / 1048576, 2)
        i['downloads'] = round(i['downloads'] / 1048576, 2)
    return render(request, 'torrent/index.html', {'user': obj, 'obj': torrents})


def login(request):
    if request.session.get('userid') is not None:
        return redirect('dashboard')
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
    userid = request.session.get('userid')
    torrent_client = get_client()
    if torrent_client is None:
        return HttpResponse(request, status=503)
    hash = add_to_queue(torrent_client, link)
    print(hash)
    info = get_status(torrent_client, hash)
    print(json.dumps(info, indent=4))
    try:
        obj = torrent.objects.get(hash=hash)
    except ObjectDoesNotExist:
        obj = torrent()
    obj.name = info['name']
    obj.hash = info['hash']
    obj.size = int(info['total_size'])
    obj.downloads = int(info['downloaded'])
    obj.progress = float(info['progress']) * 100
    obj.userid = user.objects.get(id=userid)
    obj.save()
    return HttpResponse(request, status=200)


def delete(request):
    hash = request.GET.get('hash')
    torrent_client = get_client()
    if torrent_client is None:
        return HttpResponse(request, status=503)
    obj = torrent.objects.get(hash=hash)
    obj.delete()
    delete_torrrent(torrent_client, hash)
    return HttpResponse(request, status=200)
