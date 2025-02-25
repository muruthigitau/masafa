from django.db import models
from multiselectfield import MultiSelectField
from core.models.template import BaseModel
import uuid
import os
from django.conf import settings

class Crossborder(BaseModel):
    CHOICES_STATUS = [
        ("New", "New"),
        ("Loading", "Loading"),
        ("In Transit", "In Transit"),
        ("Offloading", "Offloading"),
        ("Offloaded", "Offloaded"),
    ]
    status = models.CharField(choices=CHOICES_STATUS, max_length=255, default='New', null=True, blank=True)
    vehicle = models.ForeignKey("masafa_app.Vehicle", related_name="CrossborderVehicle", on_delete=models.CASCADE, null=True, blank=True)
    CHOICES_LOADING_POINT = [
        ("Kenya", "Kenya"),
        ("South Africa", "South Africa"),
        ("Angola", "Angola"),
        ("Botswana", "Botswana"),
        ("Comoros", "Comoros"),
        ("Democratic Republic of the Congo", "Democratic Republic of the Congo"),
        ("Eswatini (Swaziland)", "Eswatini (Swaziland)"),
        ("Lesotho", "Lesotho"),
        ("Madagascar", "Madagascar"),
        ("Malawi", "Malawi"),
        ("Mauritius", "Mauritius"),
        ("Mozambique", "Mozambique"),
        ("Namibia", "Namibia"),
        ("Seychelles", "Seychelles"),
        ("Tanzania", "Tanzania"),
        ("Zambia", "Zambia"),
        ("Zimbabwe", "Zimbabwe"),
    ]
    loading_point = models.CharField(choices=CHOICES_LOADING_POINT, max_length=255, null=True, blank=True)
    CHOICES_DESTINATION = [
        ("Nairobi", "Nairobi"),
        ("Johannesburg", "Johannesburg"),
    ]
    destination = models.CharField(choices=CHOICES_DESTINATION, max_length=255, null=True, blank=True)
    driver = models.ForeignKey("masafa_app.Driver", related_name="CrossborderDriver", on_delete=models.CASCADE, null=True, blank=True)
    loaded_at = models.DateField(null=True, blank=True)
    offloaded_at = models.DateField(null=True, blank=True)
    items = models.ManyToManyField("masafa_app.Item", related_name="CrossborderItems", )
    consolidated_invoice = models.CharField(max_length=255, null=True, blank=True)
