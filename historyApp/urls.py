
from django.urls import path
from .views import HomeView,filter_history_results

urlpatterns = [
    path('', HomeView),
    path('filter', filter_history_results),
]