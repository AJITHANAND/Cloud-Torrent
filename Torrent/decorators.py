from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect

from .models import *


def useronly(function):
    def wrap(request, *args, **kwargs):
        try:
            entry = user.objects.get(id=request.session.get('userid'))
            # print(entry)
            return function(request, *args, **kwargs)
        except ObjectDoesNotExist:
            # print('not logged')
            return redirect('login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
