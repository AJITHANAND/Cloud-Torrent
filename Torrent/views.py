from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'landing/index.html')


def dashboard(request):
    return render(request, 'torrent/index.html')
