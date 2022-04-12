from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

STATE_CHOICES =(
    ('British Columbia','British Columbia'),
    ('Nava Scotia','Nava Scotia'),
    ('Ontario','Ontario'),
) 

class Customer(models.Model):  #we creating many to one relation with user that is the reason we imported User above
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES, max_length=50)  #we made this a choice field which is from above 

    def __str__(self):
        return str(self.id) #we'll be seen with id


class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    brand=models.CharField(max_length=100)
    product_image=models.ImageField(upload_to='productimg')  #this productsimg folder is saved in media\productimg

    def __str__(self):
        return str(self.id)


class Cart(models.Model):  #foreign key is used
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)  #this cannot be less than 0 and can be more but not negative

    def __str__(self):
        return str(self.id)
    
    #here we have to show the totol of each product one by one so we gonna do that in models.py and in Cart class in @property-->
    #we gonna build a property but it's gonna workon a function

    @property
    def total_cost_product(self):
        return self.quantity * self.product.discounted_price



class OrderMade(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)       
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)

#here we have to show the totol of each product one by one so we gonna do that in models.py and in Order class in @property-->
    #we gonna build a property but it's gonna workon a function

    @property
    def total_cost_product(self):
        return self.quantity * self.product.discounted_price

   




    