from rest_framework.viewsets import mixins, GenericViewSet
from django_filters import rest_framework as filters
from crimes.filters import CrimeFilter
from crimes.models import Crime
from crimes.serializer import CrimeSerializer


class ListCrimesViewSet(mixins.ListModelMixin, GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CrimeFilter
    serializer_class = CrimeSerializer

    def get_queryset(self):
        return Crime.objects.all().order_by('-date')
