from django import forms
from phonenumber_field.formfields import PhoneNumberField

class PhoneLoginForm(forms.Form):
    phone_number = PhoneNumberField(
        max_length=15,
        label='Номер телефона',
        required=True
    )
    code = forms.CharField(
        max_length=6,
        label='Код подтверждения',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите код'}),
    )