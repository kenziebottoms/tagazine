from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ..models import *
import json

def get_tags(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        tags = Tag.objects.filter(title__icontains = q)[:20]
        results = []
        for tag in tags:
            tag_json = {}
            tag_json['value'] = tag.id
            tag_json['label'] = tag.title
            tag_json['slug'] = tag.slug
            results.append(tag_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def add_tag(request):
    if request.is_ajax():
        title = request.POST['title']
        tag = Tag.create(title)
        data = tag.id
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def zine_reslug(request):
    if request.is_ajax():
        zine = get_object_or_404(Zine,pk=request.POST['id'])
        zine.slug = zine.genSlug()
        zine.save()
        data = json.dumps({'slug' : zine.slug})
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
