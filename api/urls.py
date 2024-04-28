from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import SignUpCreateAPIView, EventsListAPIView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('sign-up/', SignUpCreateAPIView.as_view(), name='sign-up'),
    path('events/', EventsListAPIView.as_view(), name='events')
]