from base64 import urlsafe_b64encode
import re
import smtplib
import ssl
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from authentification.models import CustomUser, UserProfile 
from psychological_app import settings
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from email.message import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Psychologist, UserProfile
from django.shortcuts import render, get_object_or_404
from .models import Psychologist
from .forms import RatingForm, ReviewForm
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from .forms import AppointmentForm
from .models import Psychologist, Appointment
from django.shortcuts import render
from .forms import AppointmentForm
from datetime import datetime, timedelta
from .models import Review
from django.contrib.auth.decorators import login_required
import ssl
import smtplib
from django.template.loader import render_to_string
from email.message import EmailMessage
from django.shortcuts import render, redirect
from .forms import PsychologistForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm
import json
import smtplib
import ssl
from email.message import EmailMessage
from .forms import SelectTimeForm
from datetime import datetime, date, timedelta

# Create your views here.

def home(request):
    if request.method=="POST":
        username= request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            return render(request, "homepage.html")
        else:
            messages.error(request, "Username or Password not match")
            return redirect(home)


    return render(request,"login.html")

def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm=request.POST.get('password_confirm')
        country = request.POST.get('country')
        county = request.POST.get('county')
        city = request.POST.get('city')
        street = request.POST.get('street')
        postal_code = request.POST.get('postal_code')
        phone=request.POST.get('phone')

        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect(register)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email already registered")
            return redirect(register)

        if len(username)>15:
            messages.error(request,"Username must be under 15 characters")
            return redirect(register)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect(register)
        
        if not re.search(r'^(?=.*[A-Z])(?=.*\d)', password):
            messages.error(request, "Password should contain at least one capital letter and one number")
            return redirect(register)
        
        if password!=password_confirm:
            messages.error(request, "Password do not match")
            return redirect(register)
        
        if not fname[0].isupper():
            messages.error(request, "First name should start with a capital letter")
            return redirect(register)
        
        if not lname[0].isupper():
            messages.error(request, "First name should start with a capital letter")
            return redirect(register)


        user = CustomUser.objects.create_user(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            password=password,
            street=street,
            country=country,
            county=county,
            postal_code=postal_code,
            city=city,
            phone=phone
        )


        messages.success(request, "Your account has been created")
  


        email_sender='psychologyapp311@gmail.com'
        email_password = 'hajj zzse wjjs zoqw'
        email_receiver=user.email

        subject = "Welcome to Psychology app"
        body = "Hello " + user.first_name + "!! \n" + "Welcome to Psychological app! Thank you!"

        email= EmailMessage()
        email['From']=email_sender
        email['To']=email_receiver
        email['Subject']=subject
        email.set_content(body)

        context=ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,email.as_string())

        user_profile = UserProfile(user=user)
        user_profile.save()

        user.save()
        return redirect(home)

    return render(request,"register.html")

def send_password_reset_email(email_receiver, reset_link):
    email_sender = 'psychologyapp311@gmail.com'
    email_password = 'hajj zzse wjjs zoqw'  

    subject = "Password Reset for Your Account"
    body = f"Please click the following link to reset your password: {reset_link}"

    message = EmailMessage()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(message)

def reset_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()  
        if user:
       
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

    
            uid_str = force_str(uid)
            token_str = force_str(token)

   
            reset_link = f"{settings.BASE_URL}/reset_password/{uid_str}/{token_str}/"

     
            send_password_reset_email(email, reset_link)

            messages.success(request, "Password reset email sent.")
            return redirect(home)
        else:
            messages.error(request, "No user found with this email.")
    return render(request, 'reset_password.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)  
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
       
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'reset_password_confirm.html', context)
    else:
        messages.error(request, "The password reset link is invalid.")
        return redirect('home')


def password_reset_confirm_submit(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid) 
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password1 = request.POST.get('new_password')
            new_password2 = request.POST.get('confirm_password')
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                messages.success(request, "Password reset successful. You can now log in with your new password.")
                return redirect(home)  
            else:
                messages.error(request, "Passwords do not match.")
                return redirect(homepage)
        else:
            messages.error(request, "The password reset link is invalid.")
    return redirect('home')



def homepage(request):
    user = request.user
    context = {'username': user.username}
    return render(request, 'homepage.html', context)


def logout_view(request):
    logout(request)
    return redirect(home)  

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
      
        user_profile.city = request.POST.get('city')
        user_profile.country = request.POST.get('country')
        user_profile.county = request.POST.get('county')
        user_profile.street = request.POST.get('street')
        user_profile.postal_code = request.POST.get('postal_code')
        user_profile.phone = request.POST.get('phone')
        user_profile.save()

        
        user = request.user
        user.city = user_profile.city
        user.country = user_profile.country
        user.county = user_profile.county
        user.postal_code = user_profile.postal_code
        user.street = request.POST.get('street')  
        user.phone = request.POST.get('phone')  

        user.save()

        return redirect('profile')  
    
    context = {'user_profile': user_profile}
    return render(request, 'edit_profile.html', context)

def about_us(request):
    return render(request, 'about_us.html')


def psychologists(request):
    psychologists_data = Psychologist.objects.all()
    content_type = ContentType.objects.get_for_model(Psychologist)
    
    context = {
        'psychologists_data': psychologists_data,
        'content_type': content_type,
    }

    return render(request, 'psychologists.html', context)



def psychologist_detail(request, psychologist_id):
    psychologist = get_object_or_404(Psychologist, id=psychologist_id)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating_value = rating_form.cleaned_data['rating_value']
       
    else:
        rating_form = RatingForm()

    context = {
        'psychologist': psychologist,
        'rating_form': rating_form,
    }

    return render(request, 'psychologist_detail.html', context)


from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Psychologist, Appointment
from .forms import AppointmentForm
import json

@login_required
def appointments(request):
    if request.user.is_superuser:  
        appointments = Appointment.objects.all()  
    else:
        appointments = Appointment.objects.filter(email=request.user.email)  
    psychologists = Psychologist.objects.all()
    initial_data = {
        'full_name': f'{request.user.last_name} {request.user.first_name}',
        'email': request.user.email,
    }
    form = AppointmentForm(initial=initial_data)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            psychologist = form.cleaned_data['psychologist']
            appointment_date = form.cleaned_data['appointment_date']
            
            request.session['appointment_data'] = {
                'full_name': full_name,
                'email': email,
                'psychologist_id': psychologist.id,
                'appointment_date': appointment_date.strftime('%Y-%m-%d'),
            }
            
            return redirect('select_time')
        else:
            messages.error(request, 'There was an error in your form. Please check and try again.')

    context = {
        'appointments': appointments,
        'psychologists': psychologists,
        'form': form,
    }

    return render(request, 'appointments.html', context)


@login_required
def select_time(request):
    appointment_data = request.session.get('appointment_data')
    if not appointment_data:
        return redirect('appointments')

    psychologist = Psychologist.objects.get(id=appointment_data['psychologist_id'])
    appointment_date = datetime.strptime(appointment_data['appointment_date'], '%Y-%m-%d').date()

    if request.method == 'POST':
        form = SelectTimeForm(request.POST)
        if form.is_valid():
            appointment_time = form.cleaned_data['appointment_time']
            conflicting_appointments = Appointment.objects.filter(
                psychologist=psychologist,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            if conflicting_appointments.exists():
                messages.error(request, 'The selected time slot is not available.')
            else:
                appointment = Appointment.objects.create(
                    full_name=appointment_data['full_name'],
                    email=appointment_data['email'],
                    psychologist=psychologist,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time
                )
                email_sender = 'psychologyapp311@gmail.com'
                email_password = 'hajj zzse wjjs zoqw'  
                email_receiver = appointment_data['email']  

                subject = "Appointment Confirmation"
                body = (
                    f"Dear {appointment_data['full_name']},\n\n"
                    "Thank you for booking an appointment with us. Here are the details of your appointment:\n\n"
                    f"Psychologist: {psychologist.name}\n"
                    f"Appointment Date: {appointment.appointment_date}\n"
                    f"Appointment Time: {appointment.appointment_time}\n\n"
                    "We look forward to seeing you.\n\n"
                    "Best regards,\n\n"
                    "Your Psychology App Team"
                )

                email = EmailMessage()
                email['From'] = email_sender
                email['To'] = email_receiver
                email['Subject'] = subject
                email.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, email.as_string())
                messages.success(request, 'Appointment successfully booked.')
                return redirect('appointments')
            messages.error(request, 'There was an error in your form. Please check and try again.')
    else:
        form = SelectTimeForm()

    appointments_on_selected_date = Appointment.objects.filter(
        psychologist=psychologist,
        appointment_date=appointment_date,
    )
    booked_times = [appointment.appointment_time for appointment in appointments_on_selected_date]

    available_time_slots = [(slot, str_val) for slot, str_val in SelectTimeForm.TIME_SLOTS if slot not in booked_times]
    form.fields['appointment_time'].choices = available_time_slots

    context = {
        'psychologist': psychologist,
        'appointment_date': appointment_date,
        'form': form,
    }

    return render(request, 'select_time.html', context)






def get_available_time_slots(psychologist, appointment_date):
    appointments = Appointment.objects.filter(
        psychologist=psychologist, 
        appointment_date=appointment_date
    )
    unavailable_times = [appointment.appointment_time.strftime('%H:%M-%H:%M') for appointment in appointments]
    available_time_slots = [time_slot for time_slot in AppointmentForm.TIME_SLOTS if time_slot[0] not in unavailable_times]
    return available_time_slots



def submit_review(request, psychologist_id):
    psychologist = get_object_or_404(Psychologist, id=psychologist_id)
    reviews = Review.objects.filter(psychologist=psychologist)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user
            review = Review(psychologist=psychologist, user=user, content=content)
            review.save()
            return redirect('psychologists')
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form, 'psychologist': psychologist, 'reviews': reviews})

def add_psychologist(request):
    if request.method == 'POST':
        form = PsychologistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('psychologists')  
    else:
        form = PsychologistForm()
    
    context = {'form': form}
    return render(request, 'add_psychologist.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Psychologist

def delete_psychologist(request, psychologist_id):
    psychologist = get_object_or_404(Psychologist, id=psychologist_id)
    if request.method == 'POST':
        psychologist.delete()
        return redirect('psychologists')  
    return render(request, 'delete_psychologist.html', {'psychologist': psychologist})

def edit_psychologist(request, psychologist_id):
    psychologist = get_object_or_404(Psychologist, id=psychologist_id)
    if request.method == 'POST':
        form = PsychologistForm(request.POST, request.FILES, instance=psychologist)
        if form.is_valid():
            form.save()
            return redirect('psychologists') 
    else:
        form = PsychologistForm(instance=psychologist)
    
    context = {'form': form, 'psychologist': psychologist}
    return render(request, 'edit_psychologist.html', context)

from django.shortcuts import get_object_or_404, redirect

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointments')

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(email=request.user.email)
    return render(request, 'my_appointments.html', {'appointments': appointments})


from django.contrib.auth.models import User

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            message_to_admin = f"Message from {name}, {email}\n\n{message}"

            email_sender = 'psychologyapp311@gmail.com'
            email_password = 'hajj zzse wjjs zoqw'
            
           
            superusers = CustomUser.objects.filter(is_superuser=True)
            email_receiver = [superuser.email for superuser in superusers]

           
            email_to_admin = EmailMessage()
            email_to_admin['From'] = email_sender
            email_to_admin['To'] = email_receiver
            email_to_admin['Subject'] = subject
            email_to_admin.set_content(message_to_admin)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
                smtp.login(email_sender, email_password)
                smtp.send_message(email_to_admin)

            email_receiver = email
            confirmation_subject = 'Message Received - Psychology App'
            confirmation_body = (
                f"Dear {name},\n\n"
                "Your message has been sent successfully. We will get back to you as soon as possible.\n\n"
                "Best regards,\n\n"
                "Your Psychology App Team"
            )

            confirmation_email = EmailMessage()
            confirmation_email['From'] = email_sender
            confirmation_email['To'] = email_receiver
            confirmation_email['Subject'] = confirmation_subject
            confirmation_email.set_content(confirmation_body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, confirmation_email.as_string())
            
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})



def success(request):
    return render(request, 'success.html')



