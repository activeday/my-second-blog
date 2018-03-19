from .models import *
import django_filters

class apartment_filter(django_filters.FilterSet):
    class Meta:
        model = common_detail
        fields = ['county','rent','location']
