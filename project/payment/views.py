from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def checkout(request):
    return Response('To implement...', status=200)
    

