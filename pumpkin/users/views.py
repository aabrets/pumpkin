from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from meals.models import Meal
from meals.serializers import MealSerializer
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class MyMealsViewSet(viewsets.ModelViewSet):
    model = Meal
    serializer_class = MealSerializer

    def get_queryset(self):
        qs = Meal.objects.all()
        qs = qs.filter(owner=self.request.user)
        return qs
