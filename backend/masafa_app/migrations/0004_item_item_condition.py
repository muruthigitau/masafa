# Generated by Django 4.2.5 on 2025-02-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("masafa_app", "0003_item_exclude_in_inventory_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="item_condition",
            field=models.CharField(
                blank=True,
                choices=[("New", "New"), ("Used", "Used")],
                default="Used",
                max_length=255,
                null=True,
            ),
        ),
    ]
