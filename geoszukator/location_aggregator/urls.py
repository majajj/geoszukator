from django.urls import path

from .views import \
    check_the_location, \
    delete_record_from_db, \
    update_record_in_db

urlpatterns = [
    path('check-the-location/', check_the_location),
    path('delete-record-from-db/', delete_record_from_db),
    path('update-record-in-db/', update_record_in_db )
]
