# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect(reverse('users:success'))
    return render(request, 'login_and_reg/index.html')

def login(request):
    if request.method == 'POST':
        result = User.objects.validateLogin(request.POST)
        if result[0]:
            return log_user_in(request, result[1])
        print_errors(request, result[1])
    return redirect('/')

def register(request):
    if request.method == 'POST':
        result = User.objects.register(request.POST)
        if result[0]:
            return log_user_in(request, result[1])
        print_errors(request, result[1])
    return redirect('/')

def success(request):
    if not 'user' in request.session:
        return redirect(reverse('users:index'))
    return redirect(reverse('books:index'))

def logout(request):
    del request.session['user']
    return redirect('/')

def log_user_in(request, user):
    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
    }
    return redirect(reverse('users:success'))

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.INFO, error)
