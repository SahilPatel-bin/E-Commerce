from rest_framework import serializers
from .models import Customer,Product,Order,OrderItem
from datetime import date

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def validate_name(self, value):
        if Customer.objects.filter(name=value).exists():
            raise serializers.ValidationError("Customer with this name already exists.")
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance
     

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =  "__all__"

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be a positive number.")
        if value > 25:
            raise serializers.ValidationError("Weight cannot exceed 25kg.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer', 'order_date', 'address', 'order_items']

    def validate_order_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value
    
    def validate(self, data):
        order_items = data.get('order_items', [])
        total_weight = 0

        for item in order_items:
            product = item['product']
            quantity = item['quantity']
            total_weight += product.weight * quantity

        if total_weight > 150:
            raise serializers.ValidationError("Total order weight cannot exceed 150kg.")

        return data
    
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')
        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        # Update order items
        for item_data in order_items_data:
            product_name = item_data['product']
            order_item = instance.order_items.get(product=product_name)
            order_item.quantity = item_data.get('quantity', order_item.quantity)
            order_item.product = item_data.get('product', order_item.product)
            order_item.save()
        return instance