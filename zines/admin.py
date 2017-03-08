from django.contrib import admin

from .models import *


# # inlines
# class AuthorshipInline(admin.TabularInline):
#     model = Authorship
#     extra = 1

# class ZineAdmin(admin.ModelAdmin):
#     inlines = (AuthorshipInline,)

# class ProfileAdmin(admin.ModelAdmin):
#     inlines = (AuthorshipInline,)



admin.site.register(Profile)
admin.site.register(Zine)
admin.site.register(Issue)
admin.site.register(Page)
admin.site.register(Tag)