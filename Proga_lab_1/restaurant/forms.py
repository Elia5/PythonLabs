from django import forms


class LoginForm(forms.Form):
    login = forms.TextInput()
    password = forms.PasswordInput()