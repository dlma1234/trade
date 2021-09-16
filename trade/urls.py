"""trade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import OrderView, StockView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authenticate/', obtain_auth_token, name='authentication'),
    path('order/', OrderView.as_view(), name='order_view'),
    path('stock/', StockView.as_view(), name='stock_view'),
    path(
        'user/<int:user_id>/stock/<int:stock_id>/total', 
        OrderView().get_total_value_by_user_and_stock, 
        name='total_value_stock_user'
    )
]
