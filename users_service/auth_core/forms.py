from django import forms
from phonenumber_field.formfields import PhoneNumberField

class PhoneLoginForm(forms.Form):
    phone_number = PhoneNumberField(
        max_length=15,
        label='Номер телефона',
        required=True
    )