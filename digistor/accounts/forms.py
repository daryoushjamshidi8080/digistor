from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput, min_length=8, max_length=16)
    password2 = forms.CharField(
        label='confirm password', widget=forms.PasswordInput, min_length=8, max_length=16)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change the password using <a href="../password/">this form</a>.')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name',
                  'last_name', 'is_active', 'is_admin', 'last_login')


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'شماره مبایل'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith('09') or len(phone_number) != 11 or not phone_number.isdigit():
            raise ValidationError('شماره موبایل وارد شده معتبر نمی باشد!')
        return phone_number


class UserLoginForm(forms.Form):
    password = forms.CharField(required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'پسورد'}))
    code = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        code = cleaned_data.get('code')
        print('password :', password)
        print('code :', code, type(code), code == '')

        if (password == '' and code == ''):
            raise ValidationError('مقدار پسورد یا کد نمی‌تواند خالی باشد!')
        elif (len(password) < 8 and len(code) < 5):
            raise ValidationError(
                'مقدار کد یا پسورد از مقدار مشخص شده کم میباشد')
        return cleaned_data
