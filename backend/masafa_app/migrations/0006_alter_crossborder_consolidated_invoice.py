# Generated by Django 4.2.5 on 2025-02-25 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("masafa_app", "0005_item_paid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crossborder",
            name="consolidated_invoice",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
