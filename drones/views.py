from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from drones.models import Drone, DroneCategory, Pilot, Competition

from drones.serializers import DroneSerializer, DroneCategorySerializer, PilotSerializer, PilotCompetitionSerializer

import django_filters
from rest_framework import filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet


from rest_framework import permissions
from drones import custompermission


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from rest_framework.throttling import ScopedRateThrottle


class DroneCategoryList(ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'

    filter_fields = (
        'name',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )

class DroneCategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'


class DroneList(ListCreateAPIView):
    throttle_scope='drones'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'

    filter_fields = (
        'name',
        'drone_category',
        'manufacturing_date',
        'has_it_completed'
    )

    search_fields = (
        '^name',
    )

    ordering_fields = (
        'name',
        'manufacturing_date',
    )
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentOwnerUserOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DroneDetail(RetrieveUpdateDestroyAPIView):
    throttle_scope = 'drones'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentOwnerUserOrReadOnly,
    )

class PilotList(ListCreateAPIView):
    throttle_scope = 'pilots'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'

    filter_fields = (
        'name',
        'gender',
        'races_count',
    )

    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
        'races_count',
    )
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated,
    )


class PilotDetail(RetrieveUpdateDestroyAPIView):
    throttle_scope = 'pilots'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'

    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsAuthenticated,
    )


class CompetitionFilter(django_filters.FilterSet):
    from_achievement_date = django_filters.DateTimeFilter(field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = django_filters.DateTimeFilter(field_name='distance_achievement_date', lookup_expr='lte')

    min_distance_in_feet = django_filters.NumberFilter(field_name='distance_in_feet', lookup_expr = 'gte')
    max_distance_in_feet = django_filters.NumberFilter(field_name='distance_in_feet', lookup_expr='lte')

    drone_name = django_filters.AllValuesFilter(field_name='drone__name')
    pilot_name = django_filters.AllValuesFilter(field_name='pilot__name')

    class Meta:
        model = Competition
        fields = (
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            'drone_name',
            'pilot_name',
        )



class CompetitionList(ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'

    filter_class = CompetitionFilter
    ordering_fields = (
        'distance_in_feet',
        'distance_achievement_date',
    )

class CompetitionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class ApiRoot(GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competition': reverse(CompetitionList.name, request=request),
        })


