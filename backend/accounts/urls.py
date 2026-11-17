from django.urls import path
from .views import login_view,profile_view,logout_view,register_view,doctor_dashboard,patient_dashboard,clinic_dashboard,administrator_dashboard,update_user_role,change_password,forgot_password,reset_password

urlpatterns = [
    path('login/',login_view,name='login'),
    path('profile/',profile_view,name='profile'),
    path('logout/',logout_view,name='logout'),
    path('register/',register_view,name='register'),

    path('doctor/dashboard/',doctor_dashboard,name='doctor_dashboard'),
    path('patient/dashboard/',patient_dashboard,name='patient_dashboard'),
    path('clinic/dashboard/',clinic_dashboard,name='clinic_dashboard'),
    path('administrator/dashboard/',administrator_dashboard,name='administrator_dashboard'),
    path('users/<int:user_id>/role/',update_user_role,name='update_user_role'),
    path('change-password/',change_password,name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
]