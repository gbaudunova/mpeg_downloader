from __future__ import unicode_literals
import os
from django.utils.encoding import smart_str
import youtube_dl
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from .forms import LinkForm
from .models import Media
from .tasks import convert

# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(id)s',
    'noplaylist' : True,
    'progress_hooks': [my_hook],
}


def download(request):
    response = HttpResponseRedirect('/')
    if 'url' in request.GET:
        url = request.GET['url']
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                url,
                download=False
            )

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open(result['id'], 'rb') as file_data:
            response = HttpResponse(file_data.read(),
                                    content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                smart_str(result['title']+'.mp3'))
            response['Content-Length'] = os.path.getsize(result['id'])
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
