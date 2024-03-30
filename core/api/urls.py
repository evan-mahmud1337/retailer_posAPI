from django.urls import path
from .views import ExpenseCategoryView, ExpenseView

urlpatterns = [
    path('expense-categories/', ExpenseCategoryView.as_view(), name='expense-category-list-create'),
    path('expenses/', ExpenseView.as_view(), name='expense-list-create'),
]
