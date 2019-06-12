from rest_framework import viewsets
from .models import Meal
from .serializers import MealSerializer
from .utils import IsOwnerOrReadOnly


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class MealDietFilterViewSet(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        queryset = Meal.objects.all()
        diet_category = self.request.query_params.get('diet_category', None)
        if diet_category is not None:

            queryset = queryset.filter(diet_category=diet_category)
        return queryset

    serializer_class = MealSerializer
    permission_classes = (IsOwnerOrReadOnly,)
