from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), max_length=32, help_text='First name')
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), max_length=32, help_text='Last name')
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email','accept':'image/*'}), max_length=64, help_text='Enter a valid email address')
    class Meta:
        model = User
        fields=["first_name","last_name","email","username","password1","password2"]

class StudentProfileForm(forms.ModelForm):
    """Form definition for StudentProfile."""
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={'type':'tel','placeholder':'Phone Number','pattern':'[7-9]{1}[0-9]{9}','class':'form-control'}))
    class Meta:
        model = Student
        fields=["mobile"]

    