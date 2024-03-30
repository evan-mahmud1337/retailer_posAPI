from django.urls import path
from inventory.api.views import *
urlpatterns = [
    path('InventoryCategory/', InventoryCategoryView.as_view(), name='inventory-category'),
]
