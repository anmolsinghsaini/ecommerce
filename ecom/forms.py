from django import forms
#now we gonna use user creation form which we get by default from django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm#this authentication form is provided by django
#the authenticaton form is the we gonna use and inherit it and put some bootsrap 
#this AuthenticationForm we are using it for Login
#we use Password Change form so that we can use bootstrap 

#SetPasswordForm is for ConfirmPassword


from django.contrib.auth.models import User  #this User is we are using it for form CustomerRegistration
# we gonna import gettext and getext_lazy as '_' that we used in password filed in Login Form
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

from ecom.models import Customer

class CustomerRegistrationForm(UserCreationForm):
    #we'll apply some bootstrap so we have to write like this otherwise class Meta wold have done that
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}



class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password=forms.CharField(label=_("Password"), strip=False,widget=forms.TextInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    #we don't save information of login Form

    #we don't have to make a login view for this coz we are using default which we get form AuthenticationForm

    #but we have to make urls.py
    #for redirect login page to profile we have to use LOGIN_REDIRECT_URL = '/profile/' in settings.py


class PasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,'class':'form-control'}))
    new_password1=forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus':True,'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))
         #now we gonna make url and template for the same


class PasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control'}))



class SetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus':True,'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=_("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))


#this field is copied from source code coz we just have to set bootstap in it


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','state','zipcode']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }
#now we have to make view for this
 

