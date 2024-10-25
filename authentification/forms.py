from datetime import time
from django import forms
from django import forms
from .models import Psychologist
from django import forms
from .models import Psychologist
from django import forms


class RatingForm(forms.Form):
    rating_value = forms.IntegerField(min_value=1, max_value=5)


from django import forms
from django.forms import ModelChoiceField
from .models import Psychologist

class AppointmentForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'readonly':'readonly'}))
    psychologist = forms.ModelChoiceField(queryset=Psychologist.objects.all(), label='Psychologist')
    appointment_date = forms.DateField(label='Appointment Date', widget=forms.DateInput(attrs={'type':'date'}))
    
   


class SelectTimeForm(forms.Form):
    TIME_SLOTS = [
        (time(9, 0), '09:00-10:00'),
        (time(10, 0), '10:00-11:00'),
        (time(11, 0), '11:00-12:00'),
        (time(12, 0), '12:00-13:00'),
        (time(13, 0), '13:00-14:00'),
        (time(14, 0), '14:00-15:00'),
        (time(15, 0), '15:00-16:00'),
        (time(16, 0), '16:00-17:00'),
        (time(17, 0), '17:00-18:00'),
        (time(18, 0), '18:00-19:00'),
        (time(19, 0), '19:00-20:00'),
    ]

    appointment_time = forms.ChoiceField(choices=TIME_SLOTS, label='Appointment Time')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_time'].widget = forms.Select(choices=self.TIME_SLOTS)

class ReviewForm(forms.Form):
    content = forms.CharField(label='Your review', widget=forms.Textarea)

class PsychologistForm(forms.ModelForm):
    class Meta:
        model = Psychologist
        fields = ['name', 'therapy_type', 'cv', 'image']   


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
