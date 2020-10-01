from django import forms
from django.forms import ModelChoiceField
from django.shortcuts import get_object_or_404

from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CompanyDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class CompanyEmployer(forms.ModelForm):
    password_configure = forms.CharField(widget=forms.PasswordInput)
    permission = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=settings.PERMISSIONS)

    class Meta:
        model = Employer
        fields = ('username', 'first_name', 'last_name', 'email', 'company', 'language',
                  'passport', 'phone_number', 'permission', 'department', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    #   symbol = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
    #                                      choices=REQUIREMENTS_CHOICES, )

    def clean_password_configure(self):
        password = self.cleaned_data['password']
        password_configure = self.cleaned_data['password_configure']
        if password_configure not in password:
            raise forms.ValidationError("Неверно введенный пароль, проверьте свой пароль!")
        return password

    def clean_permission(self):
        permission = self.cleaned_data['permission']
        c = []
        o = []
        for i in settings.PERMISSIONS:
            for j in permission:
                if str(i[0]) in str(j):
                    c += i
                    o += i[1].split(',')
        permission = o
        return permission

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #print(self['permission'])
        #self.fields['permission'].initial = self['permission'].value()
        #self['permission'].initial = kwargs["instance"].permission
        #if str(kwargs["instance"].permission.replace('[', '').replace(']', '').replace("'", '')) not in str(settings.PERMISSIONS[0][0]):
        #hi = self['permission'].initial = 'company.list', 'company.employer'
        #hi = kwargs["instance"].permission.replace('[', '').replace(']', '')
        if str(kwargs) not in '{}':
            if str(kwargs["instance"].permission) not in 'None':
                #count_permission = ''
                massive_count = []
                #for characters in kwargs["instance"].permission:
                    #if characters not in "[]',":
                        #count_permission += characters
                #massive_count += count_permission.split()
                for i in settings.PERMISSIONS:
                    if i[1] in kwargs["instance"].permission:
                        massive_count += i[0].split()
                self['permission'].initial = massive_count


class CompanyRegistration(forms.ModelForm):
    password_configure = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employer
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password_configure(self):
        password = self.cleaned_data['password']
        password_configure = self.cleaned_data['password_configure']
        if password_configure not in password:
            raise forms.ValidationError("Неверно введенный пароль, проверьте свой пароль!")
        return password


class CompanyClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class CompanyCurrency(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'


class CompanyExchangeRate(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        fields = '__all__'


class CompanyPayment(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class CompanyTransaction(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class CompanyExpenses(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'


class CompanyCountry(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class CompanyTour(forms.ModelForm):
    class Meta:
        model = Tour
        fields = '__all__'


class CompanyNotification(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Employer
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Employer
        fields = ('username',)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('changes', 'time')


class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ('information',)
