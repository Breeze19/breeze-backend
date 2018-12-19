from django import forms
from django.contrib.auth import authenticate, login

class UserRegistrationForm(forms.Form):
    name = forms.CharField(
        required = True,
        label = 'Name',
        max_length = 32
    )
    email = forms.EmailField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    contact = forms.CharField(
        required = True,
        label = 'Contact',
        min_length = 10,
        max_length = 10
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 320,
        widget = forms.PasswordInput()
    )
    confirmpass = forms.CharField(
        required=True,
        label='Confirm Password',
        max_length=320,
        widget=forms.PasswordInput()
    )



class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    # email = forms.EmailField(
    #     required=True,
    #     label='Email',
    #     max_length=32,
    # )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=320,
        widget=forms.PasswordInput()
    )
    #
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     # email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     # user = authenticate(username=email , password=password)
    #     if not user or not user.is_active:
    #         raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
    #     print("Cleaned data Object is : -",self.cleaned_data)
    #     return self.cleaned_data
    #
    # def login(self, request):
    #     username = self.cleaned_data.get('username')
    #     # email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     # user = authenticate(username=email , password=password)
    #     print(user.username, user.email)
    #     return user


class EventRegisterForm(forms.Form):
    email = forms.EmailField(
        required = True,
        label = 'Email',
        max_length = 32,
    )



class ForgotPassForm(forms.Form):
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=320,
        widget=forms.PasswordInput()
    )
    confirmpass = forms.CharField(
        required=True,
        label='Confirm Password',
        max_length=320,
        widget=forms.PasswordInput()
    )


class ForgotPassMailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Email',
        max_length=32,
    )
