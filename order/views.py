from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import status
from .models import Order, OrderItem
from product.models import Product
from .serializers import OrderSerializer
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    order.save()
    serializer = OrderSerializer(order, many=False)
    return Response({'order': serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    return Response({'message': 'Order deleted successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']
    
    if orderItems and len(orderItems) == 0:
        return Response({'error': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount = sum(item['price'] * item['quantity'] for item in orderItems)
        order = Order.objects.create(
            user=user,
            city=data['city'],
            zip_code=data['zip_code'],
            street=data['street'],
            country=data['country'],
            total_amount=total_amount,
            phone_no=data['phone_no'],
        )
        for i in orderItems:
            product = Product.objects.get(id=i['product'])
            item = OrderItem.objects.create(
                order=order,
                product=product,
                name= product.name,
                quantity= i['quantity'],
                price= i['price']
            )
            product.stock -= item.quantity
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
        
