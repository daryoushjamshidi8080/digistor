from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, VerifyCodeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string


User = get_user_model()


class UserRegisterView(View):
    form = UserRegisterForm
    form_loing = UserLoginForm

    def get(self, request):
        form = self.form()
        return render(request, 'accounts/index.html', {'form': form})

    def post(self, request):
        print('*' * 60)
        form = self.form(request.POST)

        if form.is_valid():

            phone_number = form.cleaned_data.get('phone_number')
            user = User.objects.filter(phone_number=phone_number).first()

            if user:
                request.session['user_phone_number'] = {
                    'phone_number': phone_number,
                    'status': 'login'
                }
            else:
                request.session['user_phone_number'] = {
                    'phone_number': phone_number,
                    'status': 'register'
                }
            verfiy_view = VerifyView()
            return verfiy_view.post(request)
        html = render_to_string('accounts/index.html',
                                {'form': form}, request=request)
        return JsonResponse({'status': 500, 'html': html, 'error': form.errors})


class VerifyView(View):

    def post(self, request):

        form_login = UserLoginForm()
        form_verify_code = VerifyCodeForm()
        print('=' * 60)
        info_session = request.session.get('user_phone_number')

        if info_session['status'] == 'login':
            html = render_to_string(
                'accounts/login_form.html', {'form': form_login}, request=request)
            return JsonResponse({'sucsses': True, 'html': html})
        else:
            html = render_to_string(
                'accounts/verify_code_form.html', {'form': form_verify_code}, request=request)
            return JsonResponse({'sucsses': True, 'html': html})
