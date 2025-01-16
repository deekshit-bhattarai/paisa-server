"""
URL configuration for drftracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core.views import add_category, current_balance, filters, income, auth, expense
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('auth/', auth.LoginView.as_view(), name='auth'),
    path('logout/', auth.LogOutView.as_view(), name='logout'),
    path('refresh/', auth.RefreshTokenView.as_view(), name='refresh_token'),

    path('income/', income.IncomeView.as_view(), name='income'),
    path('income/<int:pk>/', income.IncomeView.as_view(), name='income'),
    path('income/filter/', filters.IncomeFilter.as_view(), name='income_filter'),

    path('expense/', expense.ExpenseView.as_view(), name='expense'),
    path('expense/<int:pk>/', expense.ExpenseView.as_view(), name='expense'),
    path('add_category/', add_category.AddCategory.as_view(), name='add_category'),
    path('expense/filter/', filters.IncomeFilter.as_view(), name='expense_filter'),

    path('current_balance/', current_balance.CurrentBalance.as_view(), name='current_balance'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
    # path("__reload__/", include("django_browser_reload.urls")),
]
