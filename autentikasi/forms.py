# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))




class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control",
            }
        ))
    GENDER_CHOICES = (
        ('', ''),
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
    kelamin = forms.CharField(
        widget = forms.Select(
            choices = GENDER_CHOICES,
            attrs={
                "placeholder" : "Jenis Kelamin",                
                "class": "form-control"
            }
        ))
    CURRENT_YEAR = datetime.now().year
    BIRTH_YEAR_CHOICES = list(range(CURRENT_YEAR-5, CURRENT_YEAR-85, -1))
    tgl_lahir = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES)
        )
    kode_lembaga = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Kode Lembaga",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'kelamin', 'tgl_lahir', 'kode_lembaga', 'password1', 'password2')


