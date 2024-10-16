from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class regform(forms.ModelForm):
    # role_choices=[
    #     ('user','User'),
    #     ('admin','Admin'),
    # ]
    # role=forms.ChoiceField(choices=role_choices,widget=forms.Select(attrs={
    #     'class':'form-control',
    #     'style':'max-width : 300px;'
    # }))
    class Meta:
        model=register
        fields='__all__'
        # fields=['nm','ph','em','psw']
        exclude=['prf_pic']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Firstname'
                }),
            'lastname': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Lastname'
                }),
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder':'Username'
            }),   
            'email': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'email'
                }),
            'psw': forms.TextInput(attrs={
                 'class': "form-control",
                 'style': 'max-width: 300px',
                 'type': 'password',
                 'placeholder': 'password'
                }),
            'cpsw': forms.TextInput(attrs={
                 'class': "form-control",
                 'style': 'max-width: 300px',
                 'type': 'password',
                 'placeholder': 'password'
                })
        }

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = 'Old Password', widget=forms.PasswordInput(attrs={'autofocus':'True',
    'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label = 'New Password', widget=forms.PasswordInput(attrs={'autofocus':'True',
    'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={'autofocus':'True',
    'autocomplete':'current-password','class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['name','locality','district','mobile','state','zipcode']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'name'
                }),
            'locality': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'locality'
                }),
            'district': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder':'district'
            }),   
            'mobile': forms.NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 400px;',
                'placeholder': 'mobile'
                }),
            'state': forms.Select(attrs={
                 'class': "form-control",
                 'style': 'max-width: 400px',
                 'placeholder': 'state'
                }),
            'zipcode': forms.NumberInput(attrs={
                 'class': "form-control",
                 'style': 'max-width: 400px',
                 'placeholder': 'zipcode'
                })
        }
  

class UpdateStockForm(forms.ModelForm):
    class Meta:
        model = addproduct
        fields = ['qty']
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
                }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
                }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message'
                }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
                'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            }
    