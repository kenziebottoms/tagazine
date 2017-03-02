
from PIL import Image
from cStringIO import StringIO
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.core.files import File
from mimetypes import MimeTypes
import urllib, os
from django.contrib import messages
from django.contrib.messages import constants as message_constants

def crop(source, dest, x, y):
    
    thumb = Image.open(StringIO(source.read()))

    width, height = thumb.size

    if width > height:
        THUMB_SIZE = [int(x*width/float(height)), y]
    else:
        THUMB_SIZE = [x,int(y*height/float(width))]

    mid_x = THUMB_SIZE[0] / 2
    mid_y = THUMB_SIZE[1] / 2
    # shrinks it down to at most 150x150 but keeps aspect ratio
    thumb = thumb.resize(THUMB_SIZE,Image.ANTIALIAS)
    # crops it down to a square from that
    thumb = thumb.crop((mid_x-(x/2),mid_y-(y/2),mid_x+(x/2),mid_y+(y/2)))

    filename, ext = os.path.splitext(source.name)
    filename = str(filename+"_150x150"+ext)
    
    f = BytesIO()
    try:
        thumb.save(f, format='png')
        dest.save(filename, ContentFile(f.getvalue()))
    finally:
        f.close()
