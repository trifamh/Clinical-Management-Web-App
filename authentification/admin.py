from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
from .models import Psychologist
from django.contrib import admin
from .models import Psychologist, Appointment

admin.site.register(Appointment)

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Psychologist)
class PsychologistAdmin(admin.ModelAdmin):
    list_display = ('name', 'therapy_type', 'cv', 'image') 

