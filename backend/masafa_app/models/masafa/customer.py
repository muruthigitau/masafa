from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Customer(BaseModel):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    CHOICES_CODE = [
        ("+27", "+27"),
        ("+254", "+254"),
        ("+230", "+230"),
        ("+243", "+243"),
        ("+244", "+244"),
        ("+248", "+248"),
        ("+255", "+255"),
        ("+258", "+258"),
        ("+260", "+260"),
        ("+263", "+263"),
        ("+264", "+264"),
        ("+266", "+266"),
        ("+267", "+267"),
        ("+268", "+268"),
        ("+269", "+269"),
        ("+261", "+261"),
        ("+265", "+265"),
    ]
    code = models.CharField(choices=CHOICES_CODE, max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    suburb = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
