from django.urls import path

from .views import check_the_location

urlpatterns = [
    path('check-the-location/', check_the_location)
]
