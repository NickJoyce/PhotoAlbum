from rest_framework import serializers
from .models import Album, Photo, Tag

class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = ['id', 'name', 'time_create', 'user']