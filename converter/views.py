# from __future__ import unicode_literals
# import os
# from django.utils.encoding import smart_str
# import youtube_dl
# from django.http import HttpResponsePermanentRedirect
# from django.shortcuts import render
# from converter.tasks import download




# Create your views here.
from django.shortcuts import render

from converter.tasks import download


def index(request):
    if request.method == 'POST':
        url = request.POST['url']
        email = request.POST['email']

        download(url, email)

    return render(request, 'index.html', {})


