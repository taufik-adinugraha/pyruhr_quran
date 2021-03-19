from django.shortcuts import render

from scipy.io.wavfile import read
from deepspeech import Model
import pandas as pd
import json
import os

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer, CariAyatDSSerializer
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.conf import settings


# paths
BASE_DIR = settings.BASE_DIR
DATA_DIR = settings.DATA_DIR

# DeepSpeech Model
DSQ = Model(f'{BASE_DIR}/deepspeech/output_graph_imams_tusers_v2.pb')
DSQ.enableExternalScorer(f'{BASE_DIR}/deepspeech/quran.scorer')

# Text Quran Utsmani
df = pd.read_csv(f'{DATA_DIR}/quran_utsmani_no_basmalah.csv')
quran_dict = {f'{i[0]}_{i[1]}': i[2].split(' ') for i in df.values}

# search Ayat from quran_dict
def find_ayat(lookup):
    max_score = 0
    all_score = {}
    for key, value in quran_dict.items():
        score = 0
        for i in lookup:
            score += i in value
        match = score/len(value)
        all_score.update({key: (score, match)})
        if score > max_score:
            max_score = score
    if max_score > 0:
        result = { k:v for k, v in all_score.items() if v[0] == max_score }
    else:
        result = {}
    return result

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
	api_urls = {
	'Upload':'/file-upload/',
	'Cari':'/cari-ayat/',
	'Hafalan':'/cek-hafalan/',
	'Bacaan':'/cek-bacaan/',
	}
	return Response(api_urls)

class FileUploadView(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	
	parser_classes = (MultiPartParser, FormParser, )
	
	def post(self, request, format=None, *args, **kwargs):
		file_upload_serializer = FileUploadSerializer(data=request.data)
		
		if file_upload_serializer.is_valid():
			file_upload_serializer.save()
			return Response(file_upload_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CariView(APIView):
	parser_classes = (MultiPartParser, FormParser, )
	
	def post(self, request, format=None, *args, **kwargs):
		cari_ayat_ds_serializer = CariAyatDSSerializer(data=request.data)
		
		if cari_ayat_ds_serializer.is_valid():
			cari_ayat_ds_serializer.save()
			filename = cari_ayat_ds_serializer.data['file']
			filepath = filename[1:]
			sr, signal = read(filepath)
			prediction = DSQ.stt(signal)
			result = find_ayat(prediction.split(' '))
			resp = {
				'result': json.dumps(result),
				'prediction': prediction,
			}
			os.remove(filepath)
			return Response(json.dumps(resp), status=status.HTTP_201_CREATED)
		else:
			return Response(cari_ayat_ds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)