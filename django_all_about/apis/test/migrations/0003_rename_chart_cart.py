# Generated by Django 4.0.5 on 2023-01-16 23:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("test", "0002_product_chart"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Chart",
            new_name="Cart",
        ),
    ]
