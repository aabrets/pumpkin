from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from eventbuilder.views import MealGetterView
from ingredients.views import IngredientViewSet
from planner.views import DayPlanViewSet
from pumpkin.users.views import UserViewSet, UserCreateViewSet, MyMealsViewSet
from meals.views import MealViewSet, MealDietFilterViewSet
from recipes.views import RecipeViewSet, MyRecipeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'meals', MealViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'my_recipes', MyRecipeViewSet, basename='my_recipe')
router.register(r'ingredients', IngredientViewSet)
router.register(r'my_meals', MyMealsViewSet, base_name='my_meals')
router.register(r'meal_diet', MealDietFilterViewSet, base_name='meal_diet')

router.register(r'dayplans', DayPlanViewSet)

schema_view = get_swagger_view(title="Swagger Docs")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/v1/event/', MealGetterView.as_view(), name='event'),
    path(r'api/v1/docs/', schema_view),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routconfigers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
