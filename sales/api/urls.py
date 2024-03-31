from django.urls import path
from sales.api.views import *
urlpatterns = [
    path('sales/',SaleCreateView.as_view() ),
    path('sales/<pk>/',SaleRetrieveView.as_view() ),
    path('dashboard',DashboardView.as_view() ),
]
