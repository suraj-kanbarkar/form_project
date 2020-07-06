from django import forms
import datetime
from .models import UserFormDetails


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    psw = forms.PasswordInput()
    psw_repeat = forms.PasswordInput()


class SignIn(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    psw = forms.PasswordInput()


class UserForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    contact = forms.IntegerField(label='Contact')
    image = forms.ImageField(label='Image', required=False)
    upload_pdf = forms.FileField(label='Upload PDF')
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    submission_date = forms.DateField(initial=datetime.date.today)

    # class Meta:
    #     model = UserFormDetails
    #     fields = ['first_name', 'last_name', 'contact', 'email', 'image', 'upload_pdf', 'date_of_birth', 'submission_date']