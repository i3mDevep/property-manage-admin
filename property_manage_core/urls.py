from django.contrib import admin

from users.views import MyTokenObtainPairView, MyTokenRefreshView

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from api.router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
