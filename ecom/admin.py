from django.contrib import admin
from .models import Customer, Product, Cart, OrderMade


# Register your models here.


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','brand','product_image']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product', 'quantity']


@admin.register(OrderMade)
class OderMadeModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity']


