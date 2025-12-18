from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="تأكيد كلمة المرور",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'phone_number',
            'location',
            'role',
            'password1',
            'password2',
        )

        labels = {
            'username': 'اسم المستخدم',
            'full_name': 'الاسم الكامل',
            'phone_number': 'رقم الهاتف',
            'location': 'السكن',
            'role': 'الدور',
        }

        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين")

        return p2

class CustomUserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label="كلمة المرور الجديدة",
        required=False,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'phone_number',
            'location',
            'role',
            'password',
        )

        labels = {
            'username': 'اسم المستخدم',
            'full_name': 'الاسم الكامل',
            'phone_number': 'رقم الهاتف',
            'location': 'السكن',
            'role': 'الدور',
            'password': 'كلمة المرور الجديدة',
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
