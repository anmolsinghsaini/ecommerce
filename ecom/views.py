from django.http import JsonResponse
from django.shortcuts import render, redirect 
from django.views.generic import ListView, DetailView, View

from ecom.forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Customer, Product, Cart, OrderMade
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required #this is for funtion based view
from django.utils.decorators import method_decorator  #this is for class based views

#list of items
class HomeView(ListView):
    model = Product  

    template_name = "ecom/home.html"



 #we could have used DetailView but we would have to make more changes for that 
 #so we using View

class ProductDetailView(View):
    def get(self, request, pk):  #we are using pk that's why we are using pk as an argument
        product=Product.objects.get(pk=pk)

        #now we gonna check whether the product exists or not 
        item_exists_in_cart=False  #we initialized this thing False
        if request.user.is_authenticated:  #now we gonna also check whether the user is login or anonymous 
            item_exists_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists() 
            #if the item already exists filtering product id and current user
        return render(request, 'ecom/productdetail.html',{'product':product , 'item_exists_in_cart':item_exists_in_cart})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'ecom/profile.html', {'form':form, 'active':'btn-primary'})  #this active context is for button profle on the templates page that we made dynamically in the view only 
                                                                                            #and now we gonna pass it
    def post(self, request):                                                                                       #this same step we will do in the address also
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user #this value we ahve to add because we didn't write something for user 
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congrats!! Profile Updated')
        return render(request, 'ecom/profile.html', {'form':form, 'active':'btn-primary'})  #this active is passed so the Profile still remain blue only

            
@login_required
#below function is the very important get the concept based on productdetail.html and addtocart.html
 #now in this view we have to save the data over here now we have product id that we made in product detail page and the user who is buying the product
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')  #here we'll get the product id of the product which the user is gonna buy
    product=Product.objects.get(id=product_id)  #we need to get product instance and then get product with id
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
#this is to make the data to showable on the cart that is the template page to user 
#and show in the same ecom/addtocart.html page 
#now we'll make the url of this below function
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=3
        total_amount=0.0
        #we'll use list comprehension below
        cart_product = [p for p in Cart.objects.all() if p.user == user]  #in this it will get the product from the cart and then put it in p and it will check the condition and the put it in the form of list
        if cart_product: #checking if there is a product in cart 
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount

        return render(request, 'ecom/addtocart.html',{'carts':cart, 'total_amount': total_amount, 'amount': amount})

        #now we'll make else statement when there is no produvt in the cart
        # and we used pid="{{cart.product.id}} in addtocart.html for increasing and decreasing product quantity
        #whenver we need a value of plus minus remove we need the value in this form so that we get id and the page doesn't refresh pid="{{cart.product.id}}

    else:
        return render(request, 'ecom/emptycart.html')

        #we'll be writing javascript code in the static\ecomm in js in myjs that code be AJAX so that our page don't refresh when we add or delete objects

#this is for increasing the product value in the cart, before that we did as I mentioned in the above comment
def plus_cart(request):
    if request.method == 'GET':  #now we'll fetch data from ajax js
        prod_id = request.GET['prod_id']  #this is  product id i.e the prod_id we getting from AJAX and further from database
        
        #now we'll be checking for the product which is particulary selected 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) #we're checking for the product but also the current user 
        c.quantity+=1  #then increase the quantity of the product
        c.save()   #saving this to database that will be shown in the admins page
        amount=0.0  #now we have to recalculate  and for that make amount initialize for the no. of items added and then again calculate the amount
        shipping_amount=3.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:  #now all this data we'll pass it in the form of Json
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
            

        data={
            'quantity':c.quantity,    #passing the above data in the form of Json Response
            'amount':amount,
            'total_amount':amount+shipping_amount,
        }
        return JsonResponse(data)  #this data will be passed in the form of object in Javascript file msscript.js


#this is for deccreasing the product value in the cart, before that we did as I mentioned in the above comment
def minus_cart(request):
    if request.method == 'GET':  #now we'll fetch data from ajax js
        prod_id = request.GET['prod_id']  #this is  product id i.e the prod_id we getting from AJAX and further from database
        
        #now we'll be checking for the product which is particulary selected 
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)) #we're checking for the product but also the current user 
        c.quantity-=1  #then increase the quantity of the product
        c.save()   #saving this to database that will be shown in the admins page
        amount=0.0  #now we have to recalculate  and for that make amount initialize for the no. of items added and then again calculate the amount
        shipping_amount=3.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:  #now all this data we'll pass it in the form of Json
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
           

        data={
            'quantity':c.quantity,    #passing the above data in the form of Json Response
            'amount':amount,
            'total_amount':amount,
        }
        return JsonResponse(data)  #this data will be passed in the form of object in Javascript file msscript.js


#this is for removing the product  in the cart, before that we did as I mentioned in the above comment
def remove_cart(request):
    if request.method == 'GET':  #now we'll fetch data from ajax js
        prod_id = request.GET['prod_id']  #this is  product id i.e the prod_id we getting from AJAX and further from database
        
        #now we'll be checking for the product which is particulary selected 
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)) #we're checking for the product but also the current user 
        c.delete()
        amount=0.0  #now we have to recalculate  and for that make amount initialize for the no. of items added and then again calculate the amount
        shipping_amount=3.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:  #now all this data we'll pass it in the form of Json
            tempamount = (p.quantity*p.product.discounted_price)
            amount += tempamount
            

        data={
              #passing the above data in the form of Json Response
            'amount':amount,
            'total_amount':amount+shipping_amount,
        }
        return JsonResponse(data)  #this data will be passed in the form of object in Javascript file msscript.js






def buy_now(request):
 return render(request, 'ecom/buynow.html')


@login_required
def address(request):

    addr=Customer.objects.filter(user=request.user)  #addr is address
    return render(request, 'ecom/address.html', {'addr':addr, 'active':'btn-primary'})  #this active is used so that address becomes blue when pressed based on template


@login_required
def orders(request):   #here we'll show the orders which are made by user and after this step we just have to attach a payment gateway
    om=OrderMade.objects.filter(user=request.user)

    return render(request, 'ecom/orders.html', {'om':om})





#def login(request):
 #return render(request, 'ecom/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form=CustomerRegistrationForm()
        return render(request, 'ecom/customerregistration.html', {'form':form})

    def post(self, request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Done!!')
            form.save()
        return render(request, 'ecom/customerregistration.html', {'form':form})




#def customerregistration(request):
 #return render(request, 'ecom/customerregistration.html')
@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        user=request.user
        addr=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=3.0
        total_amount=0.0

        cart_product = [p for p in Cart.objects.all() if p.user == user]  #in this it will get the product from the cart and then put it in p and it will check the condition and the put it in the form of list
        if cart_product: #checking if there is a product in cart 
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount



        return render(request, 'ecom/checkout.html', {'addr':addr ,'total_amount':total_amount, 'cart_items':cart_items})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')  #we are getting this from checkout.html in the forloop in the radio button 
                                        #and then it will come to paymentdone/ and then to view.py

                                        #and based on that custid we get the customer object
    customer=Customer.objects.get(id=custid)
   

    cart=Cart.objects.filter(user=user)  #getting the product from the cart for the current user logged in

#saving the first item in the order placed
    for c in cart:   #saving data in OrderMade and deleting data from cart after payment done
        OrderMade(user=user,customer=customer, product=c.product, quantity=c.quantity).save()  

        c.delete()  #then product on the cart gets deleted and not the actual product

    return redirect("orders")  # which we ahve to implement and get directed into orders
                                #this above orders is url name