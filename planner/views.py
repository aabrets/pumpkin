from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from planner.models import DayPlan
from planner.serializers import DayPlanSerializer


class DayPlanViewSet(viewsets.ModelViewSet):
    queryset = DayPlan.objects.all()
    serializer_class = DayPlanSerializer
    permission_classes = (AllowAny,)
