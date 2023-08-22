from media_app.models import MediaIds
from rest_framework.serializers import ModelSerializer


class MediaIdsSerializer(ModelSerializer):
    class Meta:
        model = MediaIds
        fields = [
            'id',
            'file_id',
            'filename'
        ]
