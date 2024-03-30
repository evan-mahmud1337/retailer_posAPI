from django.urls import path
from .views import InventoryCategoryView, InventoryListAPIView, InventoryDetailAPIView

urlpatterns = [
    path('categories/', InventoryCategoryView.as_view()),
    path('inventory/', InventoryListAPIView.as_view()),
    path('inventory/<int:pk>/', InventoryDetailAPIView.as_view()),
]
