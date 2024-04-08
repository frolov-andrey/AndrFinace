import random
import string

from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.shortcuts import redirect

from .models import Profile


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            # Меняем логин после входа
            new_username = f'{username}_{random.randint(1, 1000)}'
            user.username = new_username
            user.save()

            # Генерируем новый пароль
            new_password = self.generate_random_password()
            user.set_password(new_password)
            user.save()

            # Авторизуем пользователя
            login(self.request, user)

            # Перенаправляем на профиль
            return redirect('profile')
        else:
            # Неверный логин или пароль
            form.add_error(None, 'Неправильный логин или пароль')
            return self.form_invalid(form)

    def generate_random_password(length=12):
      """Generates a random password of the given length.

      Args:
          length (int, optional): Length of the desired password. Defaults to 12.

      Returns:
          str: A random password containing lowercase letters, uppercase letters,
              digits, and special characters.
      """
      # Define character sets for different types
      lowercase = string.ascii_lowercase
      uppercase = string.ascii_uppercase
      digits = string.digits
      special_chars = string.punctuation

      # Combine all character sets
      all_chars = lowercase + uppercase + digits + special_chars

      # Use random.sample to generate a random password
      password = ''.join(random.sample(all_chars, length))

      return password

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
