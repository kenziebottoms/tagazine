
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from mimetypes import MimeTypes
import urllib, os

def cover(source, dest, x, y):
    thumb = Image.open(source.path)
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

    filename, ext = os.path.splitext(source.path)
    filename = str(filename+"_"+str(x)+"x"+str(y)+ext)

    thumb.save(filename)

    dest.save(filename, File(open(filename, 'r')))