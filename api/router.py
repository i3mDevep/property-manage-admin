from rest_framework import routers

from users.views import RegisterUserView
from coproperties.views import CopropertyAPIView, PropertyAPIView
from payments.views import ChargesGeneralAPIView


router = routers.DefaultRouter()

router.register(r'charges-general', ChargesGeneralAPIView, basename='charges-general')
router.register(r'coproperty', CopropertyAPIView, basename='coproperty')
router.register(r'property', PropertyAPIView, basename='property')
router.register(r'register', RegisterUserView, basename='register')
