from django.contrib import admin

# Register your models here.
from .models import Album, Photo, Tag

admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Tag)