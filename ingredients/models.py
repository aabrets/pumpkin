from django.db import models


class Ingredient(models.Model):
    MEASURE_CHOICES = (
        ('TBSP', 'tbsp'),
        ('TSP', 'tsp'),
        ('CUP', 'cup'),
        ('OZ', 'oz'),
        ('HALF', 'half'),
        ('SERVING', 'serving'),
        ('PAT', 'pat'),
        ('SLICE', 'slice'),
        ('FL_OZ', 'fl_oz'),
        ('ITEM', 'item'),
        ('PKG', 'pkg')
    )

    id = models.AutoField(primary_key=True, db_column='ingredient_id')
    food = models.CharField(max_length=100)
    measure = models.CharField(max_length=30, choices=MEASURE_CHOICES, default='ITEM')
    quantity = models.FloatField(default=1.0)
    weight = models.FloatField(default=1.0)
    kcal = models.FloatField(null=True)
    fat = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    amount = models.FloatField(null=True)
    quantity_total = models.FloatField(null=True)
    weight_total = models.FloatField(null=True)
