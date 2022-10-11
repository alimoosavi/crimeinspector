from rest_framework.viewsets import mixins, GenericViewSet
from django_filters import rest_framework as filters
from crimes.filters import CrimeFilter
from crimes.models import Crime
# from crimes.authentication import CrimeListAuthentication
from crimes.serializer import CrimeSerializer


class ListCrimesViewSet(mixins.ListModelMixin, GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CrimeFilter
    # authentication_classes = (CrimeListAuthentication,)
    # def get_queryset(self):
    #     primary_type = self.request.query_params.get('primary_type')
    #     return Crime.objects.filter(primary_type=primary_type).order_by('-date')[:1000]

    serializer_class = CrimeSerializer
    queryset = Crime.objects.all()
