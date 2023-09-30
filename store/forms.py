from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile
from django import forms

class CustomUserform(UserCreationForm):
  
  username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter username'}))
  email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter Email'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2','placeholder':'Enter Password'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2','placeholder':'Comfirm Password'}))
  
  class Meta:
    model = User
    fields = ['username','email','password1', 'password2']

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter phone number'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter state'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter country'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter pincode'}))
  
    class Meta:
        model = Profile
        fields = ["phone", "address", "city", "state", "country", "pincode"]

class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control my-2'}))
    class Meta:
        model = Profile
        fields = ['image']