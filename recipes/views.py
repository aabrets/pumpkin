from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Cast
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):

        queryset = Recipe.objects.public_recipes().annotate(
            total_ingredients=Count('ingredients'),
            total_kcals=Cast(Sum('ingredients__kcal'), FloatField()),
        )
        return queryset

    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)


class MyRecipeViewSet(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):

        queryset = Recipe.objects.private_recipes(owner=self.request.user).annotate(
            total_ingredients=Count('ingredients'),
            total_kcals=Cast(Sum('ingredients__kcal'), FloatField()),
        )
        return queryset

    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
