from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
	path('',views.apiOverview, name='api-overview'),
	path('file-upload/', views.FileUploadView.as_view(), name='file-upload'),
	path('cari-ayat/', views.CariView.as_view(), name='cari-ayat'),
]