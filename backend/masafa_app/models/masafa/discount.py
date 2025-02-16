from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Discount(BaseModel):
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
