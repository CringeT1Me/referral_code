from django.contrib.admin import AdminSite
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from .forms import PhoneLoginForm
from phonenumber_field.phonenumber import PhoneNumber


class CustomAdminSite(AdminSite):
    login_template = 'registration/admin_login.html'

    def login(self, request, extra_context=None):
        if request.method == 'POST':
            form = PhoneLoginForm(request.POST)
            if form.is_valid():
                phone_number = form.cleaned_data['phone_number']
                phone_number_obj = PhoneNumber.from_string(phone_number=str(phone_number.national_number))
                UserModel = get_user_model()
                user = UserModel.objects.filter(phone_number=phone_number_obj, is_staff=True).first()
                if user:
                    login(request, user)
                    return redirect('admin:index')
                form.add_error(None, "Вам недоступна админ панель.")
        else:
            form = PhoneLoginForm()
        return render(request, self.login_template, {'form': form})

admin_site = CustomAdminSite(name='custom_admin')

