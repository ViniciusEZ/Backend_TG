from . import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q, Min, Max
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from django.views.decorators.cache import cache_page

class CustomPagination(PageNumberPagination):
    page_size = 12  
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@cache_page(60 * 3)
def get_products(request):
    sort_option = request.query_params.get('sort', 'default')

 
    sort_mappings = {
        'Mais vendidos': '-quantity',
        'Preço decrescente': '-price',
        'Preço crescente': 'price',
        'default': '-id',
    }

    sort_field = sort_mappings.get(sort_option, '-id')

    products = models.Product.objects.filter(quantity__gte=1).order_by(sort_field)

    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@cache_page(60 * 3)
def search_products(request, search):
    sort_option = request.query_params.get('sort', 'default')
    selected_suppliers = request.query_params.getlist('suppliers')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    sort_mappings = {
        'Mais vendidos': '-quantity',
        'Preço decrescente': '-price',
        'Preço crescente': 'price',
        'default': '-id',
    }

    sort_field = sort_mappings.get(sort_option, '-id')

    products = models.Product.objects.prefetch_related('supplier').filter(
        Q(name__icontains=search) | Q(supplier__fantasy_name__icontains=search)
    )

    suppliers = products.values_list('supplier__fantasy_name', flat=True).distinct()
    
    if selected_suppliers:
        products = products.filter(supplier__fantasy_name__in=selected_suppliers)

    static_range = products.aggregate(Min('price'), Max('price'))
   
    if min_price and float(min_price) != 0:
        products = products.filter(price__gte=min_price)
    if max_price and float(max_price) != 0: 
        products = products.filter(price__lte=max_price)

    products = products.order_by(sort_field)

    price_range = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    
    
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)

    response_data = {
        'products': serializer.data,
        'suppliers': suppliers,
        'price_min': price_range['min_price'] or 0,
        'price_max': price_range['max_price'] or 0,
        'static_min': static_range['price__min'],
        'static_max': static_range['price__max']
    }

    return paginator.get_paginated_response(response_data)

@api_view(['GET'])
@cache_page(60 * 3)
def get_product(request, id):
    product = models.Product.objects.filter(id=id)
    
    if product.exists():
        details = models.ProductCategoryDetails.objects.filter(product_id=product.first().id)
        data = {
            'product': product.values('id', 'name', 'price', 'image_link'),
            'detail': {
               f'{detail.category_details.about}': detail.category_details.name for detail in details
            },
            'supplier': product.first().supplier.fantasy_name
        }

        return Response(data, status=200)
    else:
        return Response('No product found!', status=404)