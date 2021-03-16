# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:    
                msg = 'username atau password tidak valid'    
        else:
            msg = 'form isian tidak tervalidasi'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg, "segment": "login"})



def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.kelamin = form.cleaned_data.get('kelamin')
            user.profile.tgl_lahir = form.cleaned_data.get('tgl_lahir')
            user.profile.lembaga = form.cleaned_data.get('lembaga')
            user.profile.kabupaten_kota = form.cleaned_data.get('kabupaten_kota')
            user.profile.provinsi = form.cleaned_data.get('provinsi')
            user.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'Akun berhasil dibuat - silakan <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'form tidak valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })



@login_required(login_url="/login/")
def profile(request):
    db = User.objects.get(username=request.user)
    if request.method == "POST":
        db.username = request.POST['username']
        db.profile.kelamin = request.POST['kelamin']
        db.profile.tgl_lahir = request.POST['tgl_lahir']
        db.profile.lembaga = request.POST['lembaga']
        db.profile.kabupaten_kota = request.POST['kabupaten_kota']
        db.profile.provinsi = request.POST['provinsi']
        db.save()
        db = User.objects.get(username=request.POST['username'])
    data = {
        'username': db.username,
        'email': db.email,
        'kelamin': db.profile.kelamin,
        'tgl_lahir': db.profile.tgl_lahir,
        'lembaga': db.profile.lembaga,
        'kabupaten_kota': db.profile.kabupaten_kota,
        'provinsi': db.profile.provinsi,
        'segment': 'profile',
    } 
    return render(request, 'profile.html', data)

