# Generated by Django 4.1.2 on 2022-11-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=200)),
                ("discount", models.IntegerField()),
                ("valid_from", models.DateField()),
                ("valid_to", models.DateTimeField()),
                ("min_amount", models.IntegerField(default=0)),
                ("is_valid", models.BooleanField(default=True)),
            ],
        ),
    ]
