import datetime

import pytz

DT_FORMAT = '%Y-%m-%d %H:%M:%S'
MEAL_CHOICES = ['BREAKFAST', 'LUNCH', 'DINNER']


def time_handler(choice, chosen_date: datetime.datetime.date):
    try:
        chosen_date = datetime.datetime.strptime(chosen_date, DT_FORMAT)
    except ValueError(f'should be of format {DT_FORMAT}'):
        return False
    today_date = datetime.datetime.now(pytz.UTC)
    days = (chosen_date-datetime.datetime.today()).days
    if days > 7 or days < 0:
        chosen_date = today_date
    if choice == 'BREAKFAST':
        chosen_date.replace(hour=8, minute=0, second=0, microsecond=0)
    elif choice == 'LUNCH':
        chosen_date.replace(hour=12, minute=0, second=0, microsecond=0)
    elif choice == 'DINNER':
        chosen_date.replace(hour=17, minute=0, second=0, microsecond=0)

    return {'start_date': chosen_date.isoformat(),
            'end_date': (chosen_date + datetime.timedelta(minutes=40)).isoformat()}


def validate(data):
    if isinstance(data, dict):
        if not data.get('start_date'):
            raise Exception('start_date should be present')
        elif not data.get('end_date'):
            raise Exception('end_date should be present')
        meal_name = data.get('meal_name')
        if meal_name:
            if not isinstance(meal_name, str):
                raise TypeError(f'meal name should be of type str not {type(meal_name)}')
            meal_detail = data.get('meal')
            if meal_detail and len(meal_detail) < 10:
                raise Exception('meal detail is too short, should be at least 10 characters')
    return data
