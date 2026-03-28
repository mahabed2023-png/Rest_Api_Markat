from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializers
from .filters import ProductsFilter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.


@api_view(['GET'])
def get_all_prouducts(request):
    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    
    count = filterset.qs.count()
    resPage = 3
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    
    query_set = paginator.paginate_queryset(filterset.qs, request)
    
    # products = Product.objects.all()
    # serializer = ProductSerializers(products, many=True)
    
    serializer = ProductSerializers(query_set, many=True)
    
    # print(products)
    
    return Response({"products": serializer.data, "per page": resPage, "count": count})


@api_view(['GET'])
def get_id_prouducts(request, pk):
    
    products = get_object_or_404(Product, id=pk)
    
    serializer = ProductSerializers(products, many=False)
    
    return Response({"product": serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])

def new_prouduct(request):
    data = request.data
    serializer = ProductSerializers(data=data)
    
    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializers(product, many=False)
        return Response({"product": res.data})
    else:
        return Response(serializer.errors)
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def update_prouduct(request, pk):
    
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"error": "You can not update this product"} , 
                            status= status.HTTP_403_FORBIDDEN )

    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']
    
    product.save()
    serializer = ProductSerializers(product, many=False)
    return Response({"product": serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def Delete_prouduct(request, pk):
    
    product = get_object_or_404(Product, id=pk)
    
    if product.user != request.user:
        return Response({"error": "You can not Delete this product"} , 
                            status= status.HTTP_403_FORBIDDEN )

    product.delete()
    return Response({"details":"Delete action it done"}, status=status.HTTP_200_OK)