from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Driver(BaseModel):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, null=True, blank=True)
    passport = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    next_of_kin = models.CharField(max_length=255, null=True, blank=True)
