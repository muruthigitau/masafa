from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class ItemGroup(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
