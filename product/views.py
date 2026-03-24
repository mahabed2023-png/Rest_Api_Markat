from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers

# Create your views here.


@api_view(['GET'])
def get_all_prouducts(request):
    
    products = Product.objects.all()
    
    serializer = ProductSerializers(products, many=True)
    
    print(products)
    
    return Response({"products": serializer.data})
