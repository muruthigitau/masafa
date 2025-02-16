from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Dispatch(BaseModel):
    customer = models.ForeignKey("masafa_app.Customer", related_name="DispatchCustomer", on_delete=models.CASCADE, null=True, blank=True)
    receiver_name = models.CharField(max_length=255, null=True, blank=True)
    CHOICES_STATUS = [
        ("New", "New"),
        ("Adding Items", "Adding Items"),
        ("Dispatched", "Dispatched"),
    ]
    status = models.CharField(choices=CHOICES_STATUS, max_length=255, default='New', null=True, blank=True)
    receiver_phone = models.CharField(max_length=255, null=True, blank=True)
    items = models.ManyToManyField("masafa_app.Item", related_name="DispatchItems", )
    date = models.DateField(null=True, blank=True)
