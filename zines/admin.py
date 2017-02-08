from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Zine)
admin.site.register(Authorship)
admin.site.register(Issue)
admin.site.register(Page)
admin.site.register(Tag)