# Generated by Django 2.1.7 on 2019-06-03 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0008_auto_20190603_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='carbs',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='fat',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='kcal',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='protein',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity_total',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='weight_total',
            field=models.FloatField(null=True),
        ),
    ]