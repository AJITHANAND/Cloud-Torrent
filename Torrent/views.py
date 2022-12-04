import json

from django.core.exceptions import ObjectDoesNotExist
import hashlib
from .forms import *
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .decorators import *
from Engine.add_queue import add_to_queue, get_client, get_status, delete_torrrent
from Engine.compress import makeZipFile
from Drive.drive import create_folder, create_parent_folder, upload_files
from Drive.Google import Create_Service


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
        obj.progress = float(info['progress']) * 100
        obj.downloads = obj.size * obj.progress / 100
        obj.userid = user.objects.get(id=userid)
        if info['progress'] == 1:
            obj.completed = True
        obj.save()
    return HttpResponse(request, status=200)


def generatelink(id):
    return "https://drive.google.com/uc?export=download&id={0}".format(id)


def encrypt(password: str):
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
    print("printing hash on views:", hash)
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


def completed(request):
    hash = request.GET.get('hash')
    userid = request.GET.get('user')
    torrent_client = get_client()
    if torrent_client is None:
        return HttpResponse(request, status=503)
    info = get_status(torrent_client, hash)
    if info['progress'] != 1:
        return HttpResponse(request, status=503)
    try:
        driveobj = Gdrive.objects.get(userid_id=userid, hash=hash)
        id = driveobj.gid
        link = generatelink(id)
        return HttpResponse(json.dumps({'id': link}), content_type='application/json', status=201)
    except ObjectDoesNotExist:
        tobj = torrent.objects.get(hash=hash)

        name = makeZipFile(info['name'])
        dirid = create_folder(userid, '1hDSrXbTMiHYvDDDWd9RiSIH1DIMXY5hB')
        gid = upload_files(name, dirid)

        driveobj = Gdrive()
        driveobj.userid = user.objects.get(id=userid)
        driveobj.torrentid = tobj
        driveobj.hash = hash
        driveobj.size = tobj.size
        driveobj.name = name
        driveobj.dirid = dirid
        driveobj.gid = gid
        driveobj.save()
        link = generatelink(gid)
        return HttpResponse(json.dumps({'id': link}), content_type='application/json', status=201)
