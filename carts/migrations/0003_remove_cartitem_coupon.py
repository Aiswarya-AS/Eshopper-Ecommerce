# Generated by Django 4.1.2 on 2022-11-17 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0002_cartitem_coupon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="coupon",
        ),
    ]