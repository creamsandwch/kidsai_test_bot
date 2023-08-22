from media_app.models import MediaIds
from rest_framework.viewsets import ModelViewSet

from .serializers import MediaIdsSerializer


class MediaIdsViewSet(ModelViewSet):
    queryset = MediaIds.objects.all()
    serializer_class = MediaIdsSerializer
    http_method_names = ['get', 'post']

