from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='',  
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='',  
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password", 'class': 'form-control',
                                          'style': 'width: 70%;  display: flex;'})
    )
    password2 = forms.CharField(
        label='',  
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password again", 'class': 'form-control',
                                          'style': 'width: 70%; display: flex;'})
    )
    username = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={"placeholder": "Enter username", 'class': 'form-control',
                                      'style': 'width: 70%; display: inline-block;'})
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name', 'class': 'form-control',
                                                 'style': 'width: 70%;  display: inline-block;'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control',
                                             'style': 'width: 70%;  display: inline-block;'}),
        }
        labels = {
            'first_name': '', 
            'email': '', 
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


