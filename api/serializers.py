from rest_framework import serializers

from .models import FileUpload, CariAyatDS

class FileUploadSerializer(serializers.ModelSerializer):
  class Meta():
    model = FileUpload
    fields = ('file', 'remark', 'timestamp')

class CariAyatDSSerializer(serializers.ModelSerializer):
	class Meta():
		model = CariAyatDS
		fields = ('file', 'remark', 'timestamp','result', 'prediction')