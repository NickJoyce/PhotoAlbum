from rest_framework import generics
from .serializers import AlbumSerializer
from .models import Album
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import os
import shutil

class AlbumAPIListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(user=user).order_by('time_create')

    def post(self, request, *args, **kwargs):
        try:
            os.mkdir(f"photo_album/static/images/user_{request.user.id}/{request.data['name']}")
        except FileExistsError:
            return Response({"error": "The album name already exists"})
        return self.create(request, *args, **kwargs)


class AlbumAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsOwner, ]

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        new_album_name = request.data['name']
        old_album_name = self.get_object().name
        if new_album_name in os.listdir(f"photo_album/static/images/user_{user_id}"):
            return Response({"error": "The album name already exists"})
        os.rename(f"photo_album/static/images/user_{user_id}/{old_album_name}",
                  f"photo_album/static/images/user_{user_id}/{new_album_name}")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        shutil.rmtree(f"photo_album/static/images/user_{request.user.id}/{self.get_object().name}")
        return self.destroy(request, *args, **kwargs)






