from django.shortcuts import render, redirect
from administrator.forms import MemberForm
from django.contrib import messages
from administrator.models import Member, Department,Attendance
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from datetime import datetime, date
from django.contrib.auth.decorators import login_required,user_passes_test
from users.models import *
from .forms import *
from .decorators import *
from administrator.models import Tracking
import secrets
import requests
from secretary.models import Transaction, Income
# Create your views here.


def index(request):
    form=MemberForm()
    return render(request, 'users/index.html',{'form':form})


def register_form(request):
    if request.method=="POST":
        form= MemberForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.department=department
            form.save()
            if request.POST.get('email'):
                mail_subject = 'REGISTRATION FOR YOUTH POWER EXPLOSION 2024 SUCCESSFULLY'
                message = render_to_string(
                    'email_template/registration_email.html',
                    {
                        'name':request.POST.get('name')
                    },
                )
                email = EmailMessage(mail_subject, message, to=[request.POST.get('email')])
                email.content_subtype = "html"
                email.send(fail_silently=False)
            messages.success(request, "Hi " +str(request.POST.get('name'))+ ", your registration was successful and we have emailed you.")
            return redirect('index')
        

@login_required(login_url='admin-login')
@admin_only
def admin_addadm(request, pk):
    district=District.objects.get(id=pk)
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.district = district
            form.save()
            group= Group.objects.get(name='secretary')
            form.groups.add(group)
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + 'create admin ' + str(request.POST.get('first_name')) + ' to ' + str(district) + ' District'
            )
            messages.success(request, str(district) + ' admin has been created')
    return redirect('admin-disrict-details', district.id)

@login_required(login_url='admin-login')
@admin_only
def admin_edit_admin(request, pk):
    district=District.objects.get(id=pk)
    district_user = User.objects.filter(groups=Group.objects.get(name='secretary'), district=district).first()
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=district_user)
        if form.is_valid():
            form=form.save(commit=False)
            form.district = district
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + 'updated ' + str(request.POST.get('first_name'))
            )
            messages.success(request, str(district) + ' admin has been updated successfully')
    return redirect('admin-disrict-details', district.id)


def Validation(value, request):
    if value.isdigit() and len(value) <=12:
        value1 = value[1:]
    else:
        value1= value
    mem = Member.objects.filter(Q(email__icontains=value1) | Q(phone__icontains=value1),date__year=2024).first()
    if mem is None:
        pass
    else:
        return mem


def attendance(request):
    if request.method=="POST":
        date1 = datetime(2024, 3, 27).date()
        date2 = datetime(2024, 3, 28).date()
        date3 = datetime(2024, 3, 29).date()
        date4 = datetime(2024, 3, 30).date()
        value= request.POST.get('member')
        if request.POST.get('day') == 'day1':
            if datetime.now().date() == date1:
                mem = Validation(value, request)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 1').exists():
                        messages.info(request, 'You have already mark your attendance for Day 1.')
                        return redirect('index')
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 1'
                        )
                        messages.success(request, 'Congratulations you have mark your attendance for Day 1.')
                        return redirect('index')
                else:
                    messages.error(request, 'We cannot find any member that is associate with this ' + str(value) + ', Check for typo error or Register')
                    return redirect('index') 
            else:
                messages.error(request, 'Sorry Attendance for "Day 1" is invalid.')
            
        elif request.POST.get('day') == 'day2':
            if datetime.now().date() == date2:
                mem = Validation(value, request)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 2').exists():
                        messages.info(request, 'You have already mark your attendance for Day 2.')
                        return redirect('index')
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 2'
                        )
                        messages.success(request, 'Congratulations you have mark your attendance for Day 2.')
                        return redirect('index')
                else:
                    messages.error(request, 'We cannot find any member that is associate with this ' + str(value) + ', Check for typo error or Register')
                    return redirect('index') 
            else:
                messages.error(request, 'Sorry Attendance for "Day 2" is invalid.')
        elif request.POST.get('day') == 'day3':
            if datetime.now().date() == date3:
                mem = Validation(value, request)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 3').exists():
                        messages.info(request, 'You have already mark your attendance for Day 3.')
                        return redirect('index')
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 3'
                        )
                        messages.success(request, 'Congratulations you have mark your attendance for Day 3.')
                        return redirect('index')
                else:
                    messages.error(request, 'We cannot find any member that is associate with this ' + str(value) + ', Check for typo error or Register')
                    return redirect('index') 
            else:
                messages.error(request, 'Sorry Attendance for "Day 3" is invalid.')
        else:
            if datetime.now().date() == date4:
                mem = Validation(value, request)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 4').exists():
                        messages.info(request, 'You have already mark your attendance for Day 4.')
                        return redirect('index')
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 4'
                        )
                        messages.success(request, 'Congratulations you have mark your attendance for Day 4.')
                        return redirect('index')
                else:
                    messages.error(request, 'We cannot find any member that is associate with this ' + str(value) + ', Check for typo error or Register')
                    return redirect('index') 
            else:
                messages.error(request, 'Sorry Attendance for "Day 4" is invalid.')
        return redirect('index')
    return redirect('index')



def rules(request):
    form = MemberForm()
    return render(request, 'users/rules.html',{'form':form})


def tenets(request):
    form = MemberForm()
    return render(request, 'users/tenets.html',{'form':form})


def vision(request):
    form = MemberForm()
    return render(request, 'users/vision.html',{'form':form})


def fft(request):
    form = MemberForm()
    return render(request, 'users/fft.html',{'form':form})



def hymns(request):
    form = MemberForm()
    return render(request, 'users/hymns.html',{'form':form})



def offerings(request):
    form = MemberForm()
    return render(request, 'users/offerings.html',{'form':form})


def payment(request):
    if request.method == 'POST':
        ref = secrets.token_urlsafe(15)
        amount = request.POST.get('amount')
        url = 'https://api.flutterwave.com/v3/payments'
        headers = {
            "Authorization": f"Bearer {settings.FLUTTER_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "tx_ref": ref,
            "amount": amount,
            "currency": "NGN",
            "payment_type": 'card',
            "redirect_url": "http://localhost:8000/client/api/confirm_deposit/?amount=" + amount,
            "customer": {
                "email": request.POST.get('email'),
                "phonenumber": request.POST.get('phone'),
                "name": request.POST.get('name')
            },
            "customizations": {
                "title": "Paying for " + str(request.POST.get('title')),
                "description": "Deposit Account",
                "logo": "https://your_logo_url.com",
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            print(response.status_code)
            print(response.content)
            if response.status_code == 200:
                district_income = Income.objects.get(id=1)
                district_income.income += 200
                district_income.save()

                # Create a transaction record for the client (CREDIT)
                Transaction.objects.create(
                    user=user,
                    description='Deposited ' + str(amount),
                    amount=amount,
                    ref=secrets.token_urlsafe(15),
                    type='credit',
                )
            return response.status_code
        except requests.exceptions.RequestException as err:
            print(str(err)) 
    return redirect('offerings')
                
           
def ConfirmDeposit(request):    
    
    return Response({"message":"Deposit was successful"}, status=status.HTTP_202_ACCEPTED)

