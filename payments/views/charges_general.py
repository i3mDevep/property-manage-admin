from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.permission_required import HasRequiredPermissionForMethod
from payments.models import ChargesGeneral
from payments.serializers import ChargesGeneralSerializer


class ChargesGeneralAPIView(viewsets.ModelViewSet):

    permission_classes = [HasRequiredPermissionForMethod]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ChargesGeneral.objects.all()

        return ChargesGeneral.objects.filter(coproperty__user_coproperty=self.request.user)

    serializer_class = ChargesGeneralSerializer
