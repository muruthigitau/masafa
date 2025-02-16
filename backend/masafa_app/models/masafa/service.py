from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Service(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
