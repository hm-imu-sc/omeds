from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('registration_page/', views.registration_page, name='registration_page'),
    path('registration/', views.registration, name='registration'),
    path('successfull_page/', views.successfull_page, name='successfull_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account_settings_page/', views.manage_account_page, name='manage_account_page'),
    path('account_deactivation_page/', views.account_deactivation_page, name='account_deactivation_page'),
    path('account_deactivation/', views.account_deactivation, name='account_deactivation'),
    path('account_deletion_page/', views.account_deletion_page, name='account_deletion_page'),
    path('account_deletion/', views.account_deletion, name='account_deletion'),
    path('patient_home_page/', views.patient_home_page, name='patient_home_page'),
    path('patient_profile_page/', views.patient_profile_page, name='patient_profile_page'),
    path('doctor_home_page/', views.doctor_home_page, name='doctor_home_page'),
    path('doctor_profile_page/', views.doctor_profile_page, name='doctor_profile_page'),
    path('home_page/', views.home_page, name='home_page'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('change_data_page/<str:data_name>/<str:current_data>/', views.change_data_page, name='change_data_page'),
    path('change_data/', views.change_data, name='change_data'),
    path('view_database_page/', views.view_database_page, name='view_database_page'),
    path('view_table_page/<str:table_name>', views.view_table_page, name='view_table_page'),
    path('test_page/', views.test_page, name='test_page'),
]
