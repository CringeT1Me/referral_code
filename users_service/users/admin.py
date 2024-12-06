import string

from django import forms
from auth_core.admin import admin_site
from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'referral_code', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.referral_code:
            user.referral_code = self.generate_referral_code()
        if commit:
            user.save()
        return user

    def generate_referral_code(self):
        """Генерация уникального реферального кода."""
        while True:
            referral_code = get_random_string(6, allowed_chars=string.ascii_uppercase + string.digits)
            if not self.model.objects.filter(referral_code=referral_code).exists():
                break
        return referral_code



class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['phone_number', 'referral_code', 'refers_to']
    list_filter = ['refers_to', 'is_staff']
    search_fields = ['id', 'phone_number', 'referral_code']
    ordering = ['id']
    readonly_fields = ['id']

    fieldsets = (
        (_('Информация о пользователе'), {'fields': ('id', 'phone_number')}),
        (_('Рефераллы'), {'fields': ('referral_code', 'refers_to')}),
        (_('Привелегии'), {'fields': ('is_staff',)})
    )

    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'referral_code', 'is_staff')}
         ),
    )

admin_site.register(User, CustomUserAdmin)
