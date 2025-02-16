from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Paymentdetails(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    account_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    CHOICES_CURRENCY = [
        ("Dollar", "Dollar"),
        ("Rand", "Rand"),
        ("KES", "KES"),
    ]
    currency = models.CharField(choices=CHOICES_CURRENCY, max_length=255, null=True, blank=True)
    branch = models.CharField(max_length=255, null=True, blank=True)
    swift_code = models.CharField(max_length=255, null=True, blank=True)
