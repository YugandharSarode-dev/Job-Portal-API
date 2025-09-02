import os
from PIL import Image
from django.db import models
from django.conf import settings
from .base import Base


class Assets(Base):
    #  Fields
    file_name = models.FileField(upload_to="media", null=True, blank=True)
    size = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "assets"
