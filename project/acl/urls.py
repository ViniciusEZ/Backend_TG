from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView



urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register_user, name='register_user'),
    path('get-user', views.get_user, name='get_user'),
    path('purchase-history', views.purchase_history, name="purchase_history")
]   