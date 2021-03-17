# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('record/<str:no_surat__no_ayat>/', views.record, name='record'),
    path('metadata/', views.metadata_rekaman, name='metadata'),
    path('upload/', views.upload, name='upload'),
    path('history/<str:var>', views.history, name='history'),
    path('history/delete/<int:pk>/', views.delete_ayat, name='delete_ayat'),
]