from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    quantity_total = serializers.SerializerMethodField()
    weight_total = serializers.SerializerMethodField()

    def get_amount(self, ingredient_instance):
        recipe = ingredient_instance.recipeingredient_set.all().first()
        if recipe:
            return recipe.amount
        else:
            return None

    def get_quantity_total(self, ingredient_instance):
        recipe = ingredient_instance.recipeingredient_set.all().first()
        if recipe:
            quantity = recipe.amount * ingredient_instance.quantity
            return quantity
        else:
            return None

    def get_weight_total(self, ingredient_instance):
        recipe = ingredient_instance.recipeingredient_set.all().first()
        if recipe:
            weight = recipe.amount * ingredient_instance.weight
            return weight
        else:
            return None

    class Meta:
        model = Ingredient
        fields = ['id', 'food', 'measure', 'quantity', 'weight', 'kcal', 'fat', 'carbs', 'protein', 'amount',
                  'quantity_total', 'weight_total']
