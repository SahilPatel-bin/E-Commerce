from django.urls import path
from app.views import *

urlpatterns = [
    path('customers/',customers),
    path('customers/<int:id>/',update_customer),
    path('products/',products),
    path('orders/',orders),
    path('orders/<int:id>/',update_order),
   
]