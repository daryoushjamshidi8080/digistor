from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterView(View):
    form = UserRegisterForm
    form_loing = UserLoginForm

    def get(self, request):
        form = self.form()

        return render(request, 'accounts/register.html', {'form': form, 'status': None})

    def post(self, request):
        status = request.POST.get('status')

        if status in ['login', 'not_found']:

            form = self.form_loing(request.POST)

            if form.is_valid():
                if status == 'login':
                    password = form.cleaned_data.get('password')

                    return HttpResponse(f'login with password: {password}')
                else:
                    code = form.cleaned_data.get('code')

                    return HttpResponse(f'login with code: {code}')
            return render(request, 'accounts/register.html', {'form_login': form, 'status': status})
        else:
            form = self.form(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data.get('phone_number')
                user = User.objects.filter(phone_number=phone_number).first()
                if user:
                    return render(request, 'accounts/register.html', {'form_login': self.form_loing(), 'status': 'login'})
                else:
                    return render(request, 'accounts/register.html', {'form_login': self.form_loing(), 'status': 'not_found'})

        return render(request, 'accounts/register.html', {'form': form, 'status': None})
