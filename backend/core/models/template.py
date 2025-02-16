import random
import string
import uuid

from django.conf import settings
from django.db import models

def generate_random_slug(length=10):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

def generate_by_hash():
    """Generate a random hash-based name."""
    return str(uuid.uuid4())

class BaseModel(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=generate_by_hash, editable=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who created this record."
    )
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_modified",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who last modified this record."
    )
    
    class Meta:
        abstract = True

class Series(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    current = models.IntegerField(default=0)