# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import rekaman, data_surat, terjemah
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
from time import time
import numpy as np
import pandas as pd
import json
import os



try:
    list_nama_surat = [f'{i.id}. {i.nama_surat_indo} ({i.nama_surat_arab})' for i in data_surat.objects.all()]
    list_nama_surat_arab = [i.nama_surat_arab for i in data_surat.objects.all()]
    max_ayat = [i.jumlah_ayat for i in data_surat.objects.all()]
    arti = {f'{i.no_surat}_{i.no_ayat}':i.terjemah for i in terjemah.objects.all()}
    info_juz = pd.read_csv('data/info_juz.csv')
except:
    pass


@login_required(login_url="/login/")
def history(request, var):
    # var: variable to sort data (ayat, ukuran, waktu)
    db = rekaman.objects.filter(user=request.user.id).order_by('no_surat', 'no_ayat')
    if var == 'ukuran':
        db = rekaman.objects.filter(user=request.user.id).order_by('-ukuran')
    elif var == 'waktu':
        db = rekaman.objects.filter(user=request.user.id).order_by('-waktu')
    elif var in np.arange(1,115).astype('str'):
        db = rekaman.objects.filter(user=request.user.id, no_surat=int(var))        
    ndb = []
    for e in db:
        tmp = {
            'pk': e.pk,
            'no_surat': e.no_surat, 
            'no_ayat': e.no_ayat, 
            'no_surat__no_ayat': f'{e.no_surat}__{e.no_ayat}',
            'ukuran': e.ukuran, 
            'waktu': e.waktu,
            'filepath': f'/{e.filepath}',
            'nama_surat': list_nama_surat_arab[e.no_surat-1],
            'max_ayat': max_ayat[e.no_surat-1],
        }
        ndb.append(tmp)
    try:
        total_size = round(db.aggregate(Sum('ukuran'))['ukuran__sum']/1000, 2)
    except:
        total_size = 0
    data = {
        'db': ndb,
        'total_ayat': db.count(),
        'list_nama_surat': json.dumps(list_nama_surat),
        # 'total_surat': db.order_by().values('no_surat').distinct().count(),
        'total_ukuran': total_size,
        'segment': 'history',
    }
    # get selected surat (filter option)
    if var in np.arange(1,115).astype('str'):
        data.update({'selected_surat': list_nama_surat[int(var)-1]})
    else:
        data.update({'selected_surat': 'surat_ayat'})
    return render(request, 'history.html', data)


@login_required(login_url="/login/")
def delete_ayat(request, pk):
    if request.method == 'POST':
        dat = rekaman.objects.get(pk=pk)
        u = User.objects.get(username=dat.user)
        filePath = dat.filepath
        dat.delete()
        os.system(f'rm -f {filePath}')
    return redirect('history', 'surat_ayat')


@login_required(login_url="/login/")
def record(request, no_surat__no_ayat):
    if no_surat__no_ayat == '0':
        no_surat, no_ayat = 1, 1
    else:
        no_surat = int(no_surat__no_ayat.split('__')[0])
        no_ayat = int(no_surat__no_ayat.split('__')[1])
    arti = {f'{i.no_surat}_{i.no_ayat}':i.terjemah for i in terjemah.objects.all()}
    data = {
        'no_surat': no_surat,
        'no_ayat': no_ayat,
        'max_ayat': max_ayat,
        'list_nama_surat': json.dumps(list_nama_surat),
        'arti': json.dumps(arti),
        'segment': 'record',
    }     
    return render(request, 'record.html', data)


@login_required(login_url="/login/")
def upload(request):
    if request.method == 'POST':
        chars = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        filePath = 'audio/' + str(time()).replace('.','')[:12] + "".join([chars[i] for j in range(8) for i in np.random.randint(0,len(chars),1)]) + '.wav'
        with open(filePath, 'wb') as file:
            file.write(request.body)
        data = request.headers['info'].split('_')
        b = User.objects.get(id=request.user.id)
        size = os.path.getsize(filePath)//1000
        try:
            # if data for particular "surat" & "ayat" already exist
            c = b.rekaman_set.get(no_surat=data[0], no_ayat=data[1])
            # delete old wav
            os.system(f'rm -f {c.filepath}')
            # update values
            c.ukuran = size
            c.filepath = filePath
            c.waktu = datetime.now()
            c.save()
        except:
            # new entry
            juz = info_juz[(info_juz['no_surat']==int(data[0])) & (info_juz['no_ayat']==int(data[1]))]['juz'].values[0]
            b.rekaman_set.create(no_surat=data[0], no_ayat=data[1], juz=juz ,ukuran=size, filepath=filePath)
        return redirect('history', 'surat_ayat')





