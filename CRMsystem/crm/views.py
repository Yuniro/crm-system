from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from django.utils import timezone

from .forms import *
from .models import *
from CRMsystem.settings import PERMISSIONS
from django.contrib.auth.views import *
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import uuid


# @cache_page(60)
def index(request):
    return render(request, 'index.html')


def email_check(user):
    return user.is_confirm


@login_required
# @user_passes_test(email_check, 'profiles')
def company_create(request):
    form = CompanyForm()
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('company_add', pk=post.pk)
    return render(request, 'company.html', {'form': form})


@login_required
# @user_passes_test(email_check, 'index')
def company_list(request):
    all_object = Company.objects.all()
    return render(request, 'company_list.html', {'all_object': all_object})


@login_required
# @user_passes_test(email_check, 'index')
def company_list_edit(request, pk):
    post = get_object_or_404(Company, pk=pk)
    form = CompanyForm(instance=post)
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('company_add', pk=post.pk)
    return render(request, 'company_list_edit.html', {'form': form})


@login_required
# @user_passes_test(email_check, 'index')
def company_add(request, pk):
    object_company = Company.objects.all().order_by('id')
    post = get_object_or_404(Company, pk=pk)
    return render(request, 'company_add.html', {'object_company': object_company, 'pk': pk, 'company_add': post})


@login_required
# @user_passes_test(email_check, 'index')
def delete(request, pk):
    delete_company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        delete_company.delete()
        return redirect('company_list')
    else:
        return render(request, 'delete.html', {'delete_company': delete_company})


@login_required
# @user_passes_test(email_check, 'index')
def department(request):
    form_department = CompanyDepartmentForm()
    if request.method == "POST":
        form_department = CompanyDepartmentForm(request.POST)
        if form_department.is_valid():
            post_company_departament = form_department.save(commit=False)
            post_company_departament.save()
            return redirect('department_add', pk=post_company_departament.pk)
    return render(request, 'company_department.html', {'form_department': form_department})


@login_required
# @user_passes_test(email_check, 'index')
def departament_list(request):
    all_department_object = Department.objects.all()
    return render(request, 'company_department_list.html', {'all_department_object': all_department_object})


@login_required
# @user_passes_test(email_check, 'index')
def department_list_edit(request, pk):
    post_company_department = get_object_or_404(Department, pk=pk)
    form_department = CompanyDepartmentForm(instance=post_company_department)
    if request.method == "POST":
        form_department = CompanyDepartmentForm(request.POST, instance=post_company_department)
        if form_department.is_valid():
            post_company_department = form_department.save(commit=False)
            post_company_department.save()
            return redirect('department_add', pk=post_company_department.pk)
    return render(request, 'department_list_edit.html', {'form_department': form_department})


@login_required
# @user_passes_test(email_check, 'index')
def department_add(request, pk):
    object_department = Department.objects.all().order_by('id')
    post = get_object_or_404(Department, pk=pk)
    context = {'object_department_company': object_department, 'pk': pk, 'department_add': post}
    return render(request, 'department_add.html', context)


@login_required
# @user_passes_test(email_check, 'index')
def department_delete(request, pk):
    delete_department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        delete_department.delete()
        return redirect('company_department_list')
    else:
        return render(request, 'delete.html', {'delete_department': delete_department})


@login_required
# @user_passes_test(email_check, 'index')
def permission_list(request):
    # permission = cache.get('permission')
    # if not permission:
    permission = PERMISSIONS
    # cache.set('permission', permission, 30)
    # print(permission)
    return render(request, 'company_permission_list.html', {'all_permission_object': permission})


def employer(request):
    form_employer = CompanyEmployer()
    if request.method == "POST":
        form_employer = CompanyEmployer(request.POST)
        if form_employer.is_valid():
            post_company_employer = form_employer.save(commit=False)
            post_company_employer.set_password(form_employer.cleaned_data['password'])
            post_company_employer.save()
            return redirect('employer_add', pk=post_company_employer.pk)
    return render(request, 'company_employer.html', {'form_employer': form_employer})


def company_registration(request):
    form_registration = CompanyRegistration()
    if request.method == "POST":
        form_registration = CompanyRegistration(request.POST)
        if form_registration.is_valid():
            post_company_employer = form_registration.save(commit=False)
            post_company_employer.set_password(form_registration.cleaned_data['password'])
            post_company_employer.save()
            return redirect('profiles', pk=post_company_employer.pk)
    return render(request, 'registration.html', {'registration': form_registration})


def profile(request, pk):
    profiles = get_object_or_404(Employer, pk=pk)
    return render(request, 'profile.html', {'profiles': profiles, 'pk': pk})


def post_email(request, pk):
    protocol = request.scheme
    user = Employer.objects.get(pk=pk)
    domain = request.get_host()
    token = PasswordResetTokenGenerator()
    token = token.make_token(user)
    send_mail('Код подтверждения', render_to_string('activate.html', {'token': token, 'code': uuid.uuid4(),
                                                                      'protocol': protocol, 'domain': domain,
                                                                      'user': user, 'pk': pk}),
              settings.EMAIL_HOST_USER,
              ['keya9711@gmail.com'],
              fail_silently=False)
    return render(request, "post_email.html")


def activate(request, token, code, protocol, domain, user, pk, *args, **kwargs):
    return render(request, 'activate.html', {'token': token, 'code': code, 'protocol': protocol, 'domain': domain,
                                             'user': user, 'pk': pk})


def accept_done(request, pk, *args, **kwargs):
    user = Employer.objects.get(pk=pk)
    user.is_confirm = True
    user.save()
    return render(request, 'accept_done.html')


def profile_edit(request, pk):
    post_company_registration = get_object_or_404(Employer, pk=pk)
    form_registration = CompanyRegistration(instance=post_company_registration)
    if request.method == "POST":
        form_registration = CompanyRegistration(request.POST, instance=post_company_registration)
        if form_registration.is_valid():
            post_company_registration = form_registration.save(commit=False)
            post_company_registration.set_password(form_registration.cleaned_data['password'])
            post_company_registration.save()
            return redirect('profiles', pk=post_company_registration.pk)
    return render(request, 'profile_edit.html', {'form_registration': form_registration})


def employer_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            employer_user = authenticate(username=cd['username'], password=cd['password'])
            if employer_user is not None:
                if employer_user.is_active:
                    login(request, employer_user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def employer_logout(request):
    logout = auth.logout(request)
    return render(request, 'index.html', {'logout': logout})


@login_required
# @user_passes_test(email_check, 'index')
def company_employer_list(request):
    # all_employer_object = cache.get('employer_list')
    # это я пытался реализовать что то на подобие обновления кэша когда меняются данные
    # if all_employer_object:
    # if str(all_employer_object) not in str(Employer.objects.all()):
    # cache.delete('employer_list')
    # if not all_employer_object:
    all_employer_object = Employer.objects.all()
    # cache.set('employer_list', all_employer_object, 30)
    return render(request, 'company_employer_list.html', {'all_employer_object': all_employer_object})


@login_required
# @user_passes_test(email_check, 'index')
def employer_list_edit(request, pk):
    post_company_employer = get_object_or_404(Employer, pk=pk)
    form_employer = CompanyEmployer(instance=post_company_employer)
    if request.method == "POST":
        form_employer = CompanyEmployer(request.POST, instance=post_company_employer)
        if form_employer.is_valid():
            post_company_employer = form_employer.save(commit=False)
            post_company_employer.set_password(form_employer.cleaned_data['password'])
            post_company_employer.save()
            return redirect('employer_add', pk=post_company_employer.pk)
    return render(request, 'employer_list_edit.html', {'form_employer': form_employer})


@login_required
# @user_passes_test(email_check, 'index')
def employer_add(request, pk):
    post = cache.get('add_employer')
    if post:
        if post not in Employer.objects.all():
            cache.delete('add_employer')
    if not post:
        post = get_object_or_404(Employer, pk=pk)
        cache.set('add_employer', post, 30)

    return render(request, 'employer_add.html', {'pk': pk, 'employer_add': post})


@login_required
# @user_passes_test(email_check, 'index')
def employer_delete(request, pk):
    delete_employer = get_object_or_404(Employer, pk=pk)
    if request.method == "POST":
        delete_employer.delete()
        return redirect('company_employer_list')
    else:
        return render(request, 'delete.html', {'delete_employer': delete_employer})


@login_required
# @user_passes_test(email_check, 'index')
def client(request):
    form_client = CompanyClient()
    if request.method == "POST":
        form_client = CompanyClient(request.POST, request.FILES)
        if form_client.is_valid():
            post_company_client = form_client.save(commit=False)
            post_company_client.save()
            return redirect('client_add', pk=post_company_client.pk)
    return render(request, 'company_client.html', {'form_client': form_client})


@login_required
# @user_passes_test(email_check, 'index')
def client_list(request):
    all_client_object = Client.objects.all()
    return render(request, 'company_client_list.html', {'all_client_object': all_client_object})


@login_required
# @user_passes_test(email_check, 'index')
def client_list_edit(request, pk):
    post_company_client = get_object_or_404(Client, pk=pk)
    form_client = CompanyClient(instance=post_company_client)
    if request.method == "POST":
        form_client = CompanyClient(request.POST, request.FILES, instance=post_company_client)
        if form_client.is_valid():
            post_company_client = form_client.save(commit=False)
            post_company_client.save()
            return redirect('client_add', pk=post_company_client.pk)
    return render(request, 'client_list_edit.html', {'form_client': form_client})


@login_required
# @user_passes_test(email_check, 'index')
def client_add(request, pk):
    post = get_object_or_404(Client, pk=pk)
    return render(request, 'client_add.html', {
        'pk': pk,
        'client_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def client_delete(request, pk):
    delete_client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        delete_client.delete()
        return redirect('company_client_list')
    else:
        return render(request, 'delete.html', {'delete_client': delete_client})


@login_required
# @user_passes_test(email_check, 'index')
def company_currency(request):
    form_currency = CompanyCurrency()
    if request.method == "POST":
        form_currency = CompanyCurrency(request.POST)
        if form_currency.is_valid():
            post_company_currency = form_currency.save(commit=False)
            post_company_currency.save()
            return redirect('currency_add', pk=post_company_currency.pk)
    return render(request, 'company_currency.html', {'form_currency': form_currency})


@login_required
# @user_passes_test(email_check, 'index')
def currency_list(request):
    all_currency_object = Currency.objects.all()
    return render(request, 'company_currency_list.html', {'all_currency_object': all_currency_object})


@login_required
# @user_passes_test(email_check, 'index')
def list_edit(request, pk):
    post_company_currency = get_object_or_404(Currency, pk=pk)
    form_currency = CompanyCurrency(instance=post_company_currency)
    if request.method == "POST":
        form_currency = CompanyCurrency(request.POST, instance=post_company_currency)
        if form_currency.is_valid():
            post_company_currency = form_currency.save(commit=False)
            post_company_currency.save()
            return redirect('currency_add', pk=post_company_currency.pk)
    return render(request, 'currency_list_edit.html', {'form_currency': form_currency})


@login_required
# @user_passes_test(email_check, 'index')
def currency_add(request, pk):
    post = get_object_or_404(Currency, pk=pk)
    return render(request, 'currency_add.html', {
        'pk': pk,
        'currency_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def currency_delete(request, pk):
    delete_currency = get_object_or_404(Currency, pk=pk)
    if request.method == "POST":
        delete_currency.delete()
        return redirect('company_currency_list')
    else:
        return render(request, 'delete.html', {'delete_client': delete_currency})


@login_required
# @user_passes_test(email_check, 'index')
def exchange_rate(request):
    form_exchange_rate = CompanyExchangeRate()
    if request.method == "POST":
        form_exchange_rate = CompanyExchangeRate(request.POST)
        if form_exchange_rate.is_valid():
            post_company_exchange_rate = form_exchange_rate.save(commit=False)
            post_company_exchange_rate.save()
            return redirect('exchange_rate_add', pk=post_company_exchange_rate.pk)
    return render(request, 'company_exchange_rate.html', {'form_exchange_rate': form_exchange_rate})


@login_required
# @user_passes_test(email_check, 'index')
def exchange_rate_list(request):
    all_exchange_rate_object = ExchangeRate.objects.all()
    return render(request, 'company_exchange_rate_list.html', {'all_exchange_rate_object': all_exchange_rate_object})


@login_required
# @user_passes_test(email_check, 'index')
def exchange_rate_list_edit(request, pk):
    post_company_exchange_rate = get_object_or_404(ExchangeRate, pk=pk)
    form_exchange_rate = CompanyExchangeRate(instance=post_company_exchange_rate)
    if request.method == "POST":
        form_exchange_rate = CompanyExchangeRate(request.POST, instance=post_company_exchange_rate)
        if form_exchange_rate.is_valid():
            post_company_exchange_rate = form_exchange_rate.save(commit=False)
            post_company_exchange_rate.save()
            return redirect('exchange_rate_add', pk=post_company_exchange_rate.pk)
    return render(request, 'exchange_rate_list_edit.html', {'form_exchange_rate': form_exchange_rate})


@login_required
# @user_passes_test(email_check, 'index')
def exchange_rate_add(request, pk):
    post = get_object_or_404(Currency, pk=pk)
    return render(request, 'exchange_rate_add.html', {
        'pk': pk,
        'exchange_rate_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def exchange_rate_delete(request, pk):
    delete_exchange_rate = get_object_or_404(ExchangeRate, pk=pk)
    if request.method == "POST":
        delete_exchange_rate.delete()
        return redirect('company_exchange_rate_list')
    else:
        return render(request, 'delete.html', {'delete_exchange_rate': delete_exchange_rate})


@login_required
# @user_passes_test(email_check, 'index')
def payment(request):
    form_payment = CompanyPayment()
    if request.method == "POST":
        form_payment = CompanyPayment(request.POST)
        if form_payment.is_valid():
            post_company_payment = form_payment.save(commit=False)
            post_company_payment.save()
            return redirect('payment_add', pk=post_company_payment.pk)
    return render(request, 'company_payment.html', {'form_payment': form_payment})


@login_required
# @user_passes_test(email_check, 'index')
def payment_list(request):
    all_payment_object = Payment.objects.all()
    return render(request, 'company_payment_list.html', {'all_payment_object': all_payment_object})


@login_required
# @user_passes_test(email_check, 'index')
def payment_list_edit(request, pk):
    post_company_payment = get_object_or_404(Payment, pk=pk)
    form_payment = CompanyPayment(instance=post_company_payment)
    if request.method == "POST":
        form_payment = CompanyPayment(request.POST, instance=post_company_payment)
        if form_payment.is_valid():
            post_company_payment = form_payment.save(commit=False)
            post_company_payment.save()
            return redirect('payment_add', pk=post_company_payment.pk)
    return render(request, 'payment_list_edit.html', {'form_payment': form_payment})


@login_required
# @user_passes_test(email_check, 'index')
def payment_add(request, pk):
    post = get_object_or_404(Payment, pk=pk)
    return render(request, 'payment_add.html', {
        'pk': pk,
        'payment_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def payment_delete(request, pk):
    delete_payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        delete_payment.delete()
        return redirect('company_payment_list')
    else:
        return render(request, 'delete.html', {'delete_payment': delete_payment})


@login_required
# @user_passes_test(email_check, 'index')
def transaction(request):
    form_transaction = CompanyTransaction()
    if request.method == "POST":
        form_transaction = CompanyTransaction(request.POST)
        if form_transaction.is_valid():
            post_company_transaction = form_transaction.save(commit=False)
            post_company_transaction.save()
            return redirect('transaction_add', pk=post_company_transaction.pk)
    return render(request, 'company_transaction.html', {'form_transaction': form_transaction})


@login_required
# @user_passes_test(email_check, 'index')
def transaction_list(request):
    all_transaction_object = Payment.objects.all()
    return render(request, 'company_transaction_list.html', {'all_transaction_object': all_transaction_object})


@login_required
# @user_passes_test(email_check, 'index')
def transaction_list_edit(request, pk):
    post_company_transaction = get_object_or_404(Transaction, pk=pk)
    form_transaction = CompanyTransaction(instance=post_company_transaction)
    if request.method == "POST":
        form_transaction = CompanyTransaction(request.POST, instance=post_company_transaction)
        if form_transaction.is_valid():
            post_company_transaction = form_transaction.save(commit=False)
            post_company_transaction.save()
            return redirect('payment_add', pk=post_company_transaction.pk)
    return render(request, 'transaction_list_edit.html', {'form_transaction': form_transaction})


@login_required
# @user_passes_test(email_check, 'index')
def transaction_add(request, pk):
    post = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transaction_add.html', {
        'pk': pk,
        'transaction_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def transaction_delete(request, pk):
    delete_transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        delete_transaction.delete()
        return redirect('company_transaction_list')
    else:
        return render(request, 'delete.html', {'delete_transaction': delete_transaction})


@login_required
# @user_passes_test(email_check, 'index')
def expenses(request):
    form_expenses = CompanyExpenses()
    if request.method == "POST":
        form_expenses = CompanyExpenses(request.POST)
        if form_expenses.is_valid():
            post_company_expenses = form_expenses.save(commit=False)
            post_company_expenses.save()
            return redirect('expenses_add', pk=post_company_expenses.pk)
    return render(request, 'company_expenses.html', {'form_expenses': form_expenses})


@login_required
# @user_passes_test(email_check, 'index')
def expenses_list(request):
    all_expenses_object = Expenses.objects.all()
    return render(request, 'company_expenses_list.html', {'all_expenses_object': all_expenses_object})


@login_required
# @user_passes_test(email_check, 'index')
def expenses_list_edit(request, pk):
    post_company_expenses = get_object_or_404(Expenses, pk=pk)
    form_expenses = CompanyExpenses(instance=post_company_expenses)
    if request.method == "POST":
        form_expenses = CompanyExpenses(request.POST, instance=post_company_expenses)
        if form_expenses.is_valid():
            post_company_expenses = form_expenses.save(commit=False)
            post_company_expenses.save()
            return redirect('expenses_add', pk=post_company_expenses.pk)
    return render(request, 'expenses_list_edit.html', {'form_expenses': form_expenses})


@login_required
# @user_passes_test(email_check, 'index')
def expenses_add(request, pk):
    post = get_object_or_404(Expenses, pk=pk)
    return render(request, 'expenses_add.html', {
        'pk': pk,
        'expenses_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def expenses_delete(request, pk):
    delete_expenses = get_object_or_404(Expenses, pk=pk)
    if request.method == "POST":
        delete_expenses.delete()
        return redirect('company_expenses_list')
    else:
        return render(request, 'delete.html', {'delete_expenses': delete_expenses})


@login_required
# @user_passes_test(email_check, 'index')
def country(request):
    form_country = CompanyCountry()
    if request.method == "POST":
        form_country = CompanyCountry(request.POST)
        if form_country.is_valid():
            post_company_country = form_country.save(commit=False)
            post_company_country.save()
            return redirect('country_add', pk=post_company_country.pk)
    return render(request, 'company_country.html', {'form_country': form_country})


@login_required
# @user_passes_test(email_check, 'index')
def country_list(request):
    all_country_object = Country.objects.all()
    return render(request, 'company_country_list.html', {'all_country_object': all_country_object})


@login_required
# @user_passes_test(email_check, 'index')
def country_list_edit(request, pk):
    post_company_country = get_object_or_404(Country, pk=pk)
    form_country = CompanyCountry(instance=post_company_country)
    if request.method == "POST":
        form_country = CompanyCountry(request.POST, instance=post_company_country)
        if form_country.is_valid():
            post_company_country = form_country.save(commit=False)
            post_company_country.save()
            return redirect('country_add', pk=post_company_country.pk)
    return render(request, 'country_list_edit.html', {'form_country': form_country})


@login_required
# @user_passes_test(email_check, 'index')
def country_add(request, pk):
    post = get_object_or_404(Country, pk=pk)
    return render(request, 'country_add.html', {
        'pk': pk,
        'country_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def country_delete(request, pk):
    delete_country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        delete_country.delete()
        return redirect('company_country_list')
    else:
        return render(request, 'delete.html', {'delete_country': delete_country})


@login_required
# @user_passes_test(email_check, 'index')
def tour(request):
    form_tour = CompanyTour()
    if request.method == "POST":
        form_tour = CompanyTour(request.POST)
        if form_tour.is_valid():
            post_company_tour = form_tour.save(commit=False)
            post_company_tour.save()
            return redirect('tour_add', pk=post_company_tour.pk)
    return render(request, 'company_tour.html', {'form_tour': form_tour})


@login_required
# @user_passes_test(email_check, 'index')
def tour_list(request):
    all_tour_object = Tour.objects.all()
    return render(request, 'company_tour_list.html', {'all_tour_object': all_tour_object})


@login_required
# @user_passes_test(email_check, 'index')
def tour_list_edit(request, pk):
    post_company_tour = get_object_or_404(Tour, pk=pk)
    form_tour = CompanyTour(instance=post_company_tour)
    if request.method == "POST":
        form_tour = CompanyTour(request.POST, instance=post_company_tour)
        if form_tour.is_valid():
            post_company_tour = form_tour.save(commit=False)
            post_company_tour.save()
            return redirect('tour_add', pk=post_company_tour.pk)
    return render(request, 'tour_list_edit.html', {'form_tour': form_tour})


@login_required
# @user_passes_test(email_check, 'index')
def tour_add(request, pk):
    post = get_object_or_404(Tour, pk=pk)
    return render(request, 'tour_add.html', {
        'pk': pk,
        'tour_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def tour_delete(request, pk):
    delete_tour = get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        delete_tour.delete()
        return redirect('company_tour_list')
    else:
        return render(request, 'delete.html', {'delete_tour': delete_tour})


@login_required
# @user_passes_test(email_check, 'index')
def notification(request):
    form_notification = CompanyNotification()
    if request.method == "POST":
        form_notification = CompanyNotification(request.POST)
        if form_notification.is_valid():
            post_company_notification = form_notification.save(commit=False)
            post_company_notification.save()
            return redirect('notification_add', pk=post_company_notification.pk)
    return render(request, 'company_notification.html', {'form_notification': form_notification})


@login_required
# @user_passes_test(email_check, 'index')
def notification_list(request):
    all_notification_object = Notification.objects.all()
    return render(request, 'company_notification_list.html', {'all_notification_object': all_notification_object})


@login_required
# @user_passes_test(email_check, 'index')
def notification_list_edit(request, pk):
    post_company_notification = get_object_or_404(Notification, pk=pk)
    form_notification = CompanyNotification(instance=post_company_notification)
    if request.method == "POST":
        form_notification = CompanyNotification(request.POST, instance=post_company_notification)
        if form_notification.is_valid():
            post_company_notification = form_notification.save(commit=False)
            post_company_notification.save()
            return redirect('notification_add', pk=post_company_notification.pk)
    return render(request, 'notification_list_edit.html', {'form_notification': form_notification})


@login_required
# @user_passes_test(email_check, 'index')
def notification_add(request, pk):
    post = get_object_or_404(Notification, pk=pk)
    return render(request, 'notification_add.html', {
        'pk': pk,
        'notification_add': post
    })


@login_required
# @user_passes_test(email_check, 'index')
def notification_delete(request, pk):
    delete_notification = get_object_or_404(Notification, pk=pk)
    if request.method == "POST":
        delete_notification.delete()
        return redirect('company_notification_list')
    else:
        return render(request, 'delete.html', {'delete_notification': delete_notification})


def report(request):
    reports = Report.objects.all()
    return render(request, 'report.html', {'reports': reports})
