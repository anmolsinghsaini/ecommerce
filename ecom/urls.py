from re import template
from django.urls import path
from ecom import views
from django.conf import settings
from django.conf.urls.static import static
#for login we are making this login
from django.contrib.auth import views as auth_views  #we gonna use it for login, password change , resert password
from .forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

urlpatterns = [
   
    path('', views.HomeView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/', views.plus_cart, name='plus_cart'), #this url is for increasing quantity of the product in the cart page
     
    path('minuscart/', views.minus_cart, name='minus_cart'), #this url is for deccreasing quantity of the product in the cart page

    path('removecart/', views.remove_cart, name='remove_cart'),



    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    

    #below 8 path are part of all authentication

    path('account/login/', auth_views.LoginView.as_view(template_name='ecom/login.html', authentication_form= LoginForm), name='login'),  #account/login so we get less errors
                            #LoginView is already built in django
                         #auth_view is the class that we use, and we gonna give template as ours so we have to define it, and we also made LoginForm which we get from Authentication but 
                         #we used our coz we had to use bootstrap
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), #we don't need to make funcstion logout either its in built and is same as Login 
    #we gonna put logout in base.html
    #now we gonna pass a next_page parameter so that it don't pass on admin logout

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='ecom/passwordchange.html', form_class=PasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange' ),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='ecom/passwordchangedone.html'), name='passwordchangedone'),
    #after password change we gonna redirect to a our desired template
    #and we gonna make template for this
    #well after password change its still asking for error password_change_done and no reverse so we gonna make a success in the url 
    #and this gonna be done in the url passwordchange/


    #now we gonna do for password reset in case of Forgot password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='ecom/password_reset.html', form_class=PasswordResetForm), name='password_reset'),
    #for email we have to write code in email backends

    #now for the page password reset done page
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='ecom/password_reset_done.html'), name='password_reset_done'),
    #here will be no form

    #this below is for password reset confirm
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='ecom/password_reset_confirm.html', form_class=SetPasswordForm), name='password_reset_confirm'),
    #we have to form for this otherwise it will show default form

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='ecom/password_reset_complete.html'), name='password_reset_complete'),

                  
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#this is above our image related configuration so that we can show our image uploaded on the frontend good and dynamic
