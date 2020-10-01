from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from CRMsystem import settings
from django.views.decorators.cache import cache_page

urlpatterns = [
#   path('', cache_page(60)(views.index), name="index"),
    path('', views.index, name="index"),

    path('report/', views.report, name="report"),

    path('company_create/', views.company_create, name="company"),
    path('company_list/', views.company_list, name="company_list"),
    path('company_list_edit/<int:pk>/edit/', views.company_list_edit, name='company_list_edit'),
    path('company_add/<int:pk>/', views.company_add, name='company_add'),
    path('company_delete/<int:pk>/', views.delete, name="delete_company"),

    path('company_department/', views.department, name='company_department'),
    path('company_department_list/', views.departament_list, name='company_department_list'),
    path('<int:pk>/edit_department/', views.department_list_edit, name='department_list_edit'),
    path('department_add/<int:pk>/', views.department_add, name='department_add'),
    path('delete_department/<int:pk>/', views.department_delete, name="delete_department"),

    path('company_permission_list/', views.permission_list, name='company_permission_list'),

    path('registration/', views.company_registration, name='registration'),
    path('profile/<int:pk>', views.profile, name='profiles'),
    path('profile_edit/<int:pk>', views.profile_edit, name='form_registration'),

    path('login/', views.employer_login, name='login'),
    path('logout/', views.employer_logout, name='logout'),

    path('post_email/done/<int:pk>', views.post_email, name='post_email'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('accept_done/<uidb64>/<token>/<int:pk>', views.accept_done, name='accept_done'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('company_employer/', views.employer, name='company_employer'),
    path('company_employer_list/', views.company_employer_list, name='company_employer_list'),
    path('<int:pk>/edit_employer/', views.employer_list_edit, name='employer_list_edit'),
    path('employer_add/<int:pk>/', views.employer_add, name='employer_add'),
    path('delete_employer/<int:pk>/', views.employer_delete, name="delete_employer"),

    path('company_client/', views.client, name='company_client'),
    path('company_client_list/', views.client_list, name='company_client_list'),
    path('<int:pk>/client_list_edit/', views.client_list_edit, name='client_list_edit'),
    path('client_add/<int:pk>/', views.client_add, name='client_add'),
    path('delete_client/<int:pk>/', views.client_delete, name="delete_client"),

    path('company_currency/', views.company_currency, name='company_currency'),
    path('company_currency_list/', views.currency_list, name='company_currency_list'),
    path('<int:pk>/currency_list_edit/', views.list_edit, name='currency_list_edit'),
    path('currency_add/<int:pk>/', views.currency_add, name='currency_add'),
    path('delete_currency/<int:pk>/', views.currency_delete, name="delete_currency"),

    path('company_exchange_rate/', views.exchange_rate, name='company_exchange_rate'), # noqa
    path('company_exchange_rate_list/', views.exchange_rate_list, name='company_exchange_rate_list'),
    path('<int:pk>/exchange_rate_list_edit/', views.exchange_rate_list_edit, name='exchange_rate_list_edit'),  # noqa
    path('exchange_rate_add/<int:pk>/', views.exchange_rate_add, name='exchange_rate_add'),
    path('delete_exchange_rate/<int:pk>/', views.exchange_rate_delete, name='delete_exchange_rate'), # noqa

    path('company_payment/', views.payment, name='company_payment'),
    path('company_payment_list/', views.payment_list, name='company_payment_list'),
    path('<int:pk>/payment_list_edit/', views.payment_list_edit, name='payment_list_edit'),
    path('payment_add/<int:pk>/', views.payment_add, name='payment_add'),
    path('delete_payment/<int:pk>/', views.payment_delete, name="delete_payment"),

    path('company_transaction/', views.transaction, name='company_transaction'),
    path('company_transaction_list/', views.transaction_list, name='company_transaction_list'),
    path('<int:pk>/transaction_list_edit/', views.transaction_list_edit, name='transaction_list_edit'), # noqa
    path('transaction_add/<int:pk>/', views.transaction_add, name='transaction_add'),
    path('delete_transaction/<int:pk>/', views.transaction_delete, name="delete_transaction"),

    path('company_expenses/', views.expenses, name='company_expenses'),
    path('company_expenses_list/', views.expenses_list, name='company_expenses_list'),
    path('<int:pk>/expenses_list_edit/', views.expenses_list_edit, name='expenses_list_edit'),  # noqa
    path('expenses_add/<int:pk>/', views.expenses_add, name='expenses_add'),
    path('delete_expenses/<int:pk>/', views.expenses_delete, name="delete_expenses"),

    path('company_country/', views.country, name='company_country'),
    path('company_country_list/', views.country_list, name='company_country_list'),
    path('<int:pk>/country_list_edit/', views.country_list_edit, name='country_list_edit'),
    path('country_add/<int:pk>/', views.country_add, name='country_add'),
    path('delete_country/<int:pk>/', views.country_delete, name="delete_country"),

    path('company_tour/', views.tour, name='company_tour'),
    path('company_tour_list/', views.tour_list, name='company_tour_list'),
    path('<int:pk>/tour_list_edit/', views.tour_list_edit, name='tour_list_edit'),
    path('tour_add/<int:pk>/', views.tour_add, name='tour_add'),
    path('delete_tour/<int:pk>/', views.tour_delete, name="delete_tour"),

    path('company_notification/', views.notification, name='company_notification'),
    path('company_notification_list/', views.notification_list, name='company_notification_list'),
    path('<int:pk>/notification_list_edit/', views.notification_list_edit, name='notification_list_edit'), # noqa
    path('notification_add/<int:pk>/', views.notification_add, name='notification_add'),
    path('delete_notification/<int:pk>/', views.notification_delete, name="delete_notification"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
