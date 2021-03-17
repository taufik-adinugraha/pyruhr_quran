from django.db import models

# Create your models here.
class FileUpload(models.Model):
	file = models.FileField(blank=False, null=False)
	remark = models.CharField(max_length=20)
	timestamp = models.DateTimeField(auto_now_add=True)

class CariAyatDS(models.Model):
	file = models.FileField(blank=False, null=False)
	remark = models.CharField(max_length=20)
	timestamp = models.DateTimeField(auto_now_add=True)
	result = models.CharField(blank=True, default='', max_length=1000)
	prediction = models.CharField(blank=True, default='', max_length=1000)
	list_nama_surat = models.CharField(blank=True, default='', max_length=1000)
	arti = models.CharField(blank=True, default='', max_length=1000)
	segment = models.CharField(blank=True, default='cari', max_length=1000)
	
	def __str__(self):
		return self.name