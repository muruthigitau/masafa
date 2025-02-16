from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Invoice(BaseModel):
    CHOICES_TYPE = [
        ("Invoice", "Invoice"),
        ("Quote", "Quote"),
    ]
    type = models.CharField(choices=CHOICES_TYPE, max_length=255, default='Invoice', null=True, blank=True)
    supplier = models.ForeignKey("masafa_app.Supplier", related_name="InvoiceSupplier", on_delete=models.CASCADE, null=True, blank=True)
    CHOICES_CURRENCY = [
        ("$", "$"),
        ("R", "R"),
        ("Kes", "Kes"),
    ]
    currency = models.CharField(choices=CHOICES_CURRENCY, max_length=255, null=True, blank=True)
    date_placed = models.DateField(null=True, blank=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    CHOICES_STATUS = [
        ("Sent", "Sent"),
        ("Not Paid", "Not Paid"),
        ("Paid", "Paid"),
    ]
    status = models.CharField(choices=CHOICES_STATUS, max_length=255, default='Sent', null=True, blank=True)
    customer = models.ForeignKey("masafa_app.Customer", related_name="InvoiceCustomer", on_delete=models.CASCADE, null=True, blank=True)
    date_sent = models.DateField(null=True, blank=True)
    bank = models.ForeignKey("masafa_app.Paymentdetails", related_name="InvoiceBank", on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    items = models.ManyToManyField("masafa_app.Item", related_name="InvoiceItems", )
    discounts = models.ManyToManyField("masafa_app.Discount", related_name="InvoiceDiscounts", )
    services = models.ManyToManyField("masafa_app.Service", related_name="InvoiceServices", )
    barcode = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.CharField(max_length=255, null=True, blank=True)
