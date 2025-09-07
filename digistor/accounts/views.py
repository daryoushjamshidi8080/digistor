from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        print(request.POST)

        return True
