from django.shortcuts import redirect
from django.http import HttpResponse

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group != 'admin':
            return HttpResponse("You're not allow to view this page.")
        return view_func(request, *args,**kwargs)
    return wrapper_function



def secretary_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group != 'secretary':
            return HttpResponse("You're not allow to view this page.")
        return view_func(request, *args,**kwargs)
    return wrapper_function