from django.urls import path
from core.views import categories, balance_n_transactions, filters, income, auth, expense

urlpatterns = [
    path('auth/', auth.LoginView.as_view(), name='auth'),
    path('register/', auth.UserRegistrationView.as_view(), name='register'),
    path('logout/', auth.LogOutView.as_view(), name='logout'),
    path('refresh/', auth.RefreshTokenView.as_view(), name='refresh_token'),

    path('income/', income.IncomeView.as_view(), name='income'),
    path('income/<int:pk>/', income.IncomeView.as_view(), name='income'),
    path('income/filter/', filters.IncomeFilter.as_view(), name='income_filter'),

    path('expense/', expense.ExpenseView.as_view(), name='expense'),
    path('expense/<int:pk>/', expense.ExpenseView.as_view(), name='expense'),
    path('categories/', categories.Categories.as_view(), name='add_category'),
    path('expense/filter/', filters.ExpenseFilter.as_view(), name='expense_filter'),

    path('current_balance/', balance_n_transactions.CurrentBalance.as_view(), name='current_balance'),

    path('recent_transactions/', balance_n_transactions.RecentTransactions.as_view(), name='recent_transactions'),
]
