# Generated by Django 4.1.2 on 2022-12-03 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0004_remove_variations_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="variations",
            name="size",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="category.size",
            ),
        ),
    ]