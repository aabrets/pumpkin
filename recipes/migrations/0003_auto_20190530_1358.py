# Generated by Django 2.1.7 on 2019-05-30 13:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipe_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='quantities',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=100), size=None), blank=True, default=None, size=None),
        ),
    ]
