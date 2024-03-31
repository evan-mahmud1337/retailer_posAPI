from django.urls import path
from customer_info.api.views import *
urlpatterns = [
    path('cus',Customerview.as_view() ),
    path('sales',Salesview.as_view() ),
    path('sales/<int:pk>',Salesview.as_view() ),
]
