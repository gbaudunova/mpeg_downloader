from __future__ import unicode_literals
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
import youtube_dl
from celery import shared_task
from django.core.mail import send_mail
from django.core import mail


@shared.task()
def download(request):
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s',
        'noplaylist': True,
        'progress_hooks': [my_hook],
    }
    response = HttpResponseRedirect('/')
    if 'url' in request.GET:
        url = request.GET['url']
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url,download=False)
            title = result.get('id', None)



    return response

def send_mail(email):

    title = 'mp3 downloading'


    message = '''
                You downloaded - %s
                your mp3 link is - %s
            ''' % (url, generated_mp3)

    send_mail(
        'Title',
        'Here is the message.',
        settings.EMAIL_HOST_USER, [email],
        fail_silently=False,
    )




