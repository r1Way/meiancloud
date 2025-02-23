from django.shortcuts import render, redirect
from .views import default_context

def page_not_found(request,exception,template_name='home/errors/404.html'):
    '''404 Not Found'''
    return render(request,template_name=template_name,context=default_context(request))

def server_error(request, template_name='home/errors/500.html'):
    '''500 Server Error'''
    return render(request, template_name,context=default_context(request))

def permission_denied(request,template_name='home/errors/403.html'):
    '''403 Permission Denied'''
    return render(request,template_name,context=default_context(request))