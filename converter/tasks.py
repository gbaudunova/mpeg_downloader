from __future__ import unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from ytconverter import settings
import youtube_dl


@shared_task
def download(url, email):
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': settings.MEDIA_ROOT + '/mp3/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'extractaudio' : True,
        'noplaylist': True,
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        name = result.get('id', None)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    mp3 = '{domain}{path}{filename}{format}'.format(
        domain='http://127.0.0.1:8000',
        path=settings.MEDIA_URL,
        filename=name,
        format='mp3')

    send(mp3, email)

def send(mp3, email):
    print(mp3)
    print(email)
    send_mail('Mp3 downloading',
              'Dowloaded %s' % mp3,
              settings.EMAIL_HOST_USER,
              [email])
              #fail_silently=True)











