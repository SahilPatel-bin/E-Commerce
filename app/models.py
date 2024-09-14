from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.contact_number} {self.email}"
    
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.weight}"
    
class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.all().order_by('id').last()
            if last_order:
                order_number = int(last_order.order_number.split('ORD')[-1]) + 1
            else:
                order_number = 1
            self.order_number = f'ORD{order_number:05d}'
       
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

