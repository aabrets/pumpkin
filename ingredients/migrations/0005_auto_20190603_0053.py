# Generated by Django 2.1.7 on 2019-06-03 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0004_ingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]