from __future__ import unicode_literals
import youtube_dl
from celery import shared_task
from django.core.mail import send_mail
from ytconverter import settings




@shared_task
def download(url, email):
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')


    ydl_opts = {
        # 'format': 'bestaudio/best',
        'outtmpl': settings.MEDIA_ROOT + '%(id)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)


    mp3 = '{domain}{path}{filename}{format}'.format(
        domain='http://127.0.0.1:8000',
        path=settings.MEDIA_URL,
        filename='77',
        format='mp4.mp3')

    send(mp3, email)



def send(mp3, email):
    print(mp3)
    print(email)
    send_mail('Mp3 downloading',
              '%s' % (mp3),
              'ivanovaanna038@gmail.com',
              [email])
              # fail_silently=False)

    send()



    # user_email.attach_file('%s/audio/%s.mp3' % (STATIC_DIR, mp3))
# if __name__ == "__main__":
# # download = download(email, url)



