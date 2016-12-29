from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Zine)
admin.site.register(Authorship)
admin.site.register(Issue)