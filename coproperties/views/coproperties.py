from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from utils.permission_required import HasRequiredPermissionForMethod

from payments.models import ChargesGeneral, ChargesSpecific
from coproperties.models import Coproperty, Property
from coproperties.serializers import CopropertiesSerializer


class CopropertyAPIView(viewsets.ModelViewSet):

    permission_classes = [HasRequiredPermissionForMethod]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Coproperty.objects.all()

        return Coproperty.objects.filter(user_coproperty=self.request.user)

    def contains(self, list, filter):
        for x in list:
            if filter(x):
                return True
        return False

    @action(detail=True, methods=['get'])
    def generate_report_charges(self, request, pk=None):

        coproperty_ = self.get_object()

        charges_general = ChargesGeneral.objects.get(coproperty=coproperty_)
        properties = Property.objects.filter(coproperty=coproperty_)
        charges_specific = ChargesSpecific.objects.filter(
            property__in=properties)

        chagers_for_property = {}

        for property in properties:

            quote = float(charges_general.money) * \
                property.clustering_coefficient

            chagers_for_property[property.client.username] = {
                'id': property.client.id,
                'email': property.client.email,
                'name': property.client.first_name + ' ' + property.client.last_name,
                'quotes': [
                    *chagers_for_property.get(property.client.username, {'quotes': []})['quotes'],
                    {
                        'reason': charges_general.name,
                        'description': charges_general.description,
                        'quote': quote,
                        'type': property.type_property
                    },
                ]
            }

            if self.contains(list(charges_specific), lambda x: x.property.id == property.id):
                for specific in charges_specific:
                    chagers_for_property[property.client.username]['quotes'].append(
                        {'reason': specific.reason, 'description': specific.description, 'quote': float(specific.money), 'type': 'INDIVIDUAL'})

        return JsonResponse({'total_money_general': charges_general.money, 'report_administration': chagers_for_property}, safe=True)

    serializer_class = CopropertiesSerializer
