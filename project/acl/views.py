from rest_framework.response import Response
from rest_framework.decorators import api_view
from adrf.decorators import api_view as async_api_view
from . import models
from django.db import IntegrityError
from project.products import models as products_models
from asgiref.sync import sync_to_async

@async_api_view(['POST'])
async def register_user(request):
    user_name = request.data.get('name')    
    user_email = request.data.get('email')
    user_password = request.data.get('password')
    user_phone_number = request.data.get('phone_number')
    user_cpf = request.data.get('cpf')
    user_addresses = request.data.get('addresses')

    try:
        user = await models.User.objects.acreate(
            name=user_name,
            email=user_email,
            phone_number=user_phone_number,
            cpf=user_cpf
        )

        user.set_password(user_password)
        await user.asave()
    except IntegrityError:
        return Response('User already exists!', status=409)

    for address in user_addresses:
        await models.Address.objects.acreate(
            **address, user=user
        ) 

    return Response('User registered successfully!', status=200)

@api_view(['GET', 'POST'])
def get_user(request):
    try:
        user = models.User.objects.get(email=request.data.get('userEmail'))
    except models.User.DoesNotExist:
        return Response('User not found!', status=404)

    addresses = models.Address.objects.filter(
        user=user
    ).values('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf')

    user_data = {
        'name': user.name,
        'phone': user.phone_number,
        'email': user.email,
        'cpf': user.cpf,
        'addresses': addresses
    }

    return Response(user_data, status=200)

@api_view(['GET', 'POST'])
def purchase_history(request):
    try:
        user = models.User.objects.get(email=request.data.get('userEmail'))
    except models.User.DoesNotExist:
        return Response('No data found!', status=404)
    
    
    purchase_history = products_models.Purchase.objects.filter(
        user=user
    ).values(
        'quantity',
        'purchase_value',
        'purchase_date',
        'payment_method__method',
        'product__name',
        'product__image_link'
    )



    return Response(purchase_history, status=200)


