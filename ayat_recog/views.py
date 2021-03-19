from django.shortcuts import render, redirect
from django.http import HttpResponse
from scipy.io.wavfile import read
from deepspeech import Model
from django.conf import settings
import pandas as pd
import json
import io
import os


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


def cari(request):
    data = {
        'segment': 'cari',
    }
    if request.method == 'POST':
        # audio recognition
        sr, signal = read(request.FILES['file'].file)
        prediction = DSQ.stt(signal)
        result = find_ayat(prediction.split(' '))
        # sorting based on similarity (high --> low)
        result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
        data = {
            'result': json.dumps(result),
            'prediction': prediction,
            'segment': 'cari',
        }        
        return HttpResponse(json.dumps(data), content_type='application/json')
    return render(request, 'cari.html', data)


def hafalan(request):
    data = {
        'segment': 'hafalan',
    } 
    if request.method == 'POST':
        # audio recognition
        sr, signal = read(request.FILES['file'].file)
        prediction = DSQ.stt(signal).split(' ')
        data = {
            'prediction': prediction,
            'segment': 'hafalan',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')     
    return render(request, 'hafalan.html', data)


def bacaan(request):
    data = {
        'segment': 'bacaan',
    } 
    if request.method == 'POST':
        # audio recognition
        sr, signal = read(request.FILES['file'].file)
        prediction = DSQ.stt(signal).split(' ')
        data = {
            'prediction': prediction,
            'segment': 'bacaan',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')     
    return render(request, 'bacaan.html', data)

    