from rest_framework import serializers

from meals.serializers import MealSerializer
from recipes.serializers import RecipeSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True)
    recipes = RecipeSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'meals', 'recipes')


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
