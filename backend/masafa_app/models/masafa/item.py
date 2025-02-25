from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Item(BaseModel):
    item_group = models.ForeignKey("masafa_app.ItemGroup", related_name="ItemItemGroup", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    packaging_type = models.CharField(max_length=255, null=True, blank=True)
    CHOICES_TYPE = [
        ("Invoice", "Invoice"),
        ("Quote", "Quote"),
    ]
    type = models.CharField(choices=CHOICES_TYPE, max_length=255, default='Invoice', null=True, blank=True)
    customer = models.ForeignKey("masafa_app.Customer", related_name="ItemCustomer", on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey("masafa_app.Supplier", related_name="ItemSupplier", on_delete=models.CASCADE, null=True, blank=True)
    CHOICES_STATUS = [
        ("Received", "Received"),
        ("In Transit", "In Transit"),
        ("Ready For Collection", "Ready For Collection"),
        ("Dispatched", "Dispatched"),
    ]
    status = models.CharField(choices=CHOICES_STATUS, max_length=255, default='Received', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    received_at = models.ForeignKey("core.Branch", related_name="ItemReceivedAt", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.CharField(max_length=255, null=True, blank=True)
    exclude_in_inventory_list = models.BooleanField(null=True, blank=True)
    CHOICES_ITEM_CONDITION = [
        ("New", "New"),
        ("Used", "Used"),
    ]
    item_condition = models.CharField(choices=CHOICES_ITEM_CONDITION, max_length=255, default='Used', null=True, blank=True)
    paid = models.BooleanField(null=True, blank=True)
