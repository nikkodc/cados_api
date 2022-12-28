from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.endpoints),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('advocates/', views.advocate_list, name='advocates'),
    # path('advocates/<str:username>/', views.advocate_detail)
    path('advocates/<str:username>/', views.AdvocateDetail.as_view()),

    #companies/
    path('companies/', views.companies_list)
]
