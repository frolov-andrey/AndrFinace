import random
import string

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from .models import Profile


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
        'select_menu': 'login'
    }


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.filter(user=self.request.user)
        if profile.exists():
            profile = profile.get()
            if profile.is_demo and profile.password != '':
                context['password'] = profile.password

        return context

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            form.add_error('email', "Такой E-mail уже существует!")
            return self.form_invalid(form)

        return super().form_valid(form)


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        profile = Profile.objects.filter(user=self.request.user)
        if profile.exists():
            profile = profile.get()
            if profile.is_demo and profile.password != '':
                profile.password = ''
                profile.is_demo = False
                profile.save()

        return response
