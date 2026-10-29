from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('budget/', views.manage_budget, name='manage_budget'),
    path('charts/', views.expense_charts, name='expense_charts'),
    path('analysis/', views.expense_analysis, name='expense_analysis'),
]