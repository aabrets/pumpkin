# Generated by Django 2.1.7 on 2019-05-30 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(db_column='ingredient_id', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField(blank=True)),
            ],
        ),
    ]
