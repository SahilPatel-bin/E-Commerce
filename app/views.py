from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *


@api_view(['GET','POST'])
def customers(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializers = CustomerSerializer(customers,many=True)
        return Response(serializers.data)
    
    else:
        serializers = CustomerSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "Customer created successfully","data":serializers.data},status=status.HTTP_201_CREATED)
    
        return Response({"message": "Customer creation failed", "errors": serializers.errors},status=status.HTTP_400_BAD_REQUEST)

    
@api_view(["PUT"])
def update_customer(request, id):
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist :
        return Response({"message": "Customer not found"},status=status.HTTP_404_NOT_FOUND)
    
    serializers = CustomerSerializer(customer,data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({"message": "Customer updated successfully","data":serializers.data},status=status.HTTP_205_RESET_CONTENT)
    
    return Response({"message": "Customer update failed", "errors": serializers.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","POST"])
def products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializers = ProductSerializer(products,many=True)
        return Response(serializers.data)
    
    else :
        serializers = ProductSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "Product created successfully","data":serializers.data},status=status.HTTP_201_CREATED)
        
        return Response({"message": "Product creation failed", "errors": serializers.errors},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET","POST"])
def orders(request):
    if request.method == 'GET':
        product_names = request.GET.get('products',None)
        customer_name = request.GET.get('customer',None)
    
        orders = Order.objects.all()

        if product_names:
            product_list = [name.strip() for name in product_names.split(',')]
            products = Product.objects.filter(name__in=product_list)

            if not products.exists():
                return Response({"message": "No products found with the given input names"}, status=status.HTTP_404_NOT_FOUND)

            orders = orders.filter(order_items__product__in=products).distinct()

        if customer_name:
            try:
                customer = Customer.objects.get(name=customer_name)        
                orders = orders.filter(customer=customer)
                if not orders.exists():
                    return Response({"message": "The customer has not placed any orders."},status=status.HTTP_200_OK)
            
            except Customer.DoesNotExist :
                return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if orders.exists():
            serializers = OrderSerializer(orders, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)

        else :
            orders = Order.objects.all()
            serializers = OrderSerializer(orders,many=True)
            return Response(serializers.data)
    
    else :
        serializers = OrderSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "Order created successfully","data":serializers.data},status=status.HTTP_201_CREATED)
        
        return Response({"message": "Order creation failed", "errors": serializers.errors},status=status.HTTP_400_BAD_REQUEST)

   
@api_view(["PUT"])
def update_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist :
        return Response({"message": "Order not found"},status=status.HTTP_404_NOT_FOUND)
    
    serializers = OrderSerializer(order, data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response({"message": "Order updated successfully","data":serializers.data},status=status.HTTP_205_RESET_CONTENT)
    
    return Response({"message": "Order update failed", "errors": serializers.errors},status=status.HTTP_400_BAD_REQUEST)
