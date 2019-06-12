from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from gcalendar.calendar_event import execute_event
from gcalendar.meal_event_builder import MEAL_CHOICES, time_handler, validate
from meals.models import Meal


class MealGetterView(APIView):

    def post(self, request):
        event_query = {}
        meal_name = request.data.get('meal_name')
        meal_detail = Meal.objects.filter(name__icontains=meal_name)[0].detail
        event_query.update({'meal_name': meal_name, 'detail': meal_detail})

        event_date = request.data.get('event_date')
        choice = request.data.get('choice')
        if choice in MEAL_CHOICES:
            event_query.update(time_handler(choice, event_date))
        else:
            raise ValueError(f'wrong choice. should be on of these: {MEAL_CHOICES}')

        if validate(event_query):
            data = execute_event(event_query)
            return Response(json.dumps(data), status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def get_extra_actions(cls):
        return []
