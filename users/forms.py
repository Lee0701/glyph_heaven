from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import User

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'

    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=False, widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput(), validators=[password_validation.validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
