from django.contrib import admin
from django.urls import path
from django.urls import path,include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import contact_us, success

urlpatterns = [
    path('',views.home, name="home"),
    path('homepage/', views.homepage, name='homepage'),
    path('register/', views.register,name="register"),
    path('reset_password/', views.reset_pass,name="password_reset"),
    path('reset_password/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_submit/<str:uidb64>/<str:token>/', views.password_reset_confirm_submit, name='password_reset_confirm_submit'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('about_us/', views.about_us, name='about_us'),
    path('psychologists/', views.psychologists, name='psychologists'),       
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('appointments/', views.appointments, name='appointments'),
    path('psychologists/<int:psychologist_id>/submit_review/', views.submit_review, name='submit_review'),
    path('add_psychologist/', views.add_psychologist, name='add_psychologist'),
    path('delete_psychologist/<int:psychologist_id>/', views.delete_psychologist, name='delete_psychologist'),
    path('edit_psychologist/<int:psychologist_id>/', views.edit_psychologist, name='edit_psychologist'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('success/', success, name='success'),
    path('select_time/', views.select_time, name='select_time'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)