from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.permission_required import HasRequiredPermissionForMethod
from coproperties.models import Property
from coproperties.serializers import PropertySerializer


class PropertyAPIView(viewsets.ModelViewSet):

    permission_classes = [HasRequiredPermissionForMethod]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['apto']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Property.objects.all()

        return Property.objects.filter(coproperty__user_coproperty=self.request.user)

    serializer_class = PropertySerializer
