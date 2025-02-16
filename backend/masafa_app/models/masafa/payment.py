from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Payment(BaseModel):
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source = models.ForeignKey("masafa_app.Paymentdetails", related_name="PaymentSource", on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey("masafa_app.Invoice", related_name="PaymentInvoice", on_delete=models.CASCADE, null=True, blank=True)
    transaction_no = models.CharField(max_length=255, null=True, blank=True)
    CHOICES_CURRENCY = [
        ("$", "$"),
        ("R", "R"),
        ("Kes", "Kes"),
    ]
    currency = models.CharField(choices=CHOICES_CURRENCY, max_length=255, null=True, blank=True)
