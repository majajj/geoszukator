from django.urls import path

from .views import \
    check_the_location, \
    delete_record_from_db, \
    update_record_in_db

urlpatterns = [
    path('check-the-location/<str:ip>', check_the_location),
    path('delete-record-from-db/<str:ip>', delete_record_from_db),
    path('update-record-in-db/<str:ip>', update_record_in_db)
]
