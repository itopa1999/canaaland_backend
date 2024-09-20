import django_filters
from django_filters import DateFilter
from .models import *

class DistrictMemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    state = django_filters.CharFilter(field_name='state', lookup_expr='icontains')
    district = django_filters.CharFilter(field_name='district', lookup_expr='icontains')
    age__lte = django_filters.NumberFilter(field_name='age', lookup_expr='lte')
    age__gte = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    class Meta:
        model = Church_Member
        fields = ['gender','name','email','department','age__lte','age__gte']




class DistrictNewMemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    age__lte = django_filters.NumberFilter(field_name='age', lookup_expr='lte')
    age__gte = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    class Meta:
        model = Church_New_Member
        fields = ['gender','name','email','age__lte','age__gte']
        
        
class DistrictTransactionFilter(django_filters.FilterSet):
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    class Meta:
        model = Transaction
        fields = ['type','date__lte','date__gte']
        
        
class DistrictAttendanceFilter(django_filters.FilterSet):
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    class Meta:
        model = Transaction
        fields = ['date__lte','date__gte']
