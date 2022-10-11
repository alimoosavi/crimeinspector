from django_filters import rest_framework as filters
from crimes.models import Crime


class CrimeFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    max_date = filters.DateTimeFilter(field_name="date", lookup_expr="lte")
    primary_type = filters.CharFilter(field_name="primary_type")

    class Meta:
        model = Crime
        fields = ['date', 'primary_type']