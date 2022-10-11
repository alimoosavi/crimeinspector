from django.urls import path
from crimes.views import ListCrimesViewSet

urlpatterns = [
    path('list/', ListCrimesViewSet.as_view({'get': 'list'}), name='crimes-list')
]
