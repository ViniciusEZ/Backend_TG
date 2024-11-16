from django.urls import path
from . import views



urlpatterns = [
    path('get-products', views.get_products, name='get_products'),
    path('search/<str:search>', views.search_products, name='search_products'),
    path('product/<int:id>', views.get_product, name='get_product')
]   