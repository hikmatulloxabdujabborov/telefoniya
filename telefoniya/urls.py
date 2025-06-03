from django.urls import path
from .views import (
    AbonentListAPI,
    TarifListAPI,
    TolovListAPI,
    user_login,
    user_logout,
    tolovlar_view,
    tolov_qoshish,
    dashboard,
    abonentlar,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),

    # API endpointlar
    path('api/abonentlar/', AbonentListAPI.as_view(), name='api_abonentlar'),
    path('api/tariflar/', TarifListAPI.as_view(), name='api_tariflar'),
    path('api/tolovlar/', TolovListAPI.as_view(), name='api_tolovlar'),

    # JWT tokenlar uchun
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Foydalanuvchi uchun URLlar
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('abonentlar/', abonentlar, name='abonentlar'),  # abonentlar sahifasi

    path('tolovlar/', tolovlar_view, name='tolovlar'),
    path('tolov/qoshish/', tolov_qoshish, name='tolov_qoshish'),
]
