from django.db import models


class MediaIds(models.Model):
    """Storing media from chats."""
    file_id = models.CharField(
        unique=True,
        max_length=255,
        verbose_name='telegram file id'
    )
    filename = models.CharField(
        unique=True,
        max_length=255,
        verbose_name='file name'
    )
