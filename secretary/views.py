from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
import csv
from users.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
#from users.forms import *
from .filters import *
from .forms import *
from .models import *
from users.decorators import *
from administrator.models import Tracking
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_secretary(user):
    return user.groups.filter(name='secretary').exists()

@login_required(login_url='admin-login')
@secretary_only
def secretary_dashboard(request):
    
    district=District.objects.get(id=request.user.district.id)
    district_user = User.objects.filter(groups=Group.objects.get(name='secretary'), district=district).first()
    district_member = Church_Member.objects.filter(district = district)
    district_new_member = Church_New_Member.objects.filter(district = district)
    district_income = Income.objects.get(district = district)
    district_transaction = Transaction.objects.filter(district = district)
    district_attendance = Church_Attendance.objects.filter(district = district)
    form3=ChurchMemberForm()
    form4=ChurchNewMemberForm()
    
    return render(request, "secretary/secretary-dashboard.html",{'district':district,'district_user':district_user,'district_transaction':district_transaction,'district_member':district_member,
                            'district_income':district_income,'form3':form3,'form4':form4,'district_new_member':district_new_member,'district_attendance':district_attendance})

    


@login_required(login_url='admin-login')
def admin_add_member(request, pk):
    district=District.objects.get(id=pk)
    form = ChurchMemberForm()
    if request.method == 'POST':
        form = ChurchMemberForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.district = district
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + 'added a new member ' + str(request.POST.get('name'))
            )
            messages.success(request, 'member has been successfully added to ' + str(district) )
            if is_secretary(request.user): 
                return redirect('secretary-dashboard')
    return redirect('admin-disrict-details', district.id)


@login_required(login_url='admin-login')
def admin_add_new_member(request, pk):
    district=District.objects.get(id=pk)
    form = ChurchNewMemberForm()
    if request.method == 'POST':
        form = ChurchNewMemberForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.district = district
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + 'added a new church member ' + str(request.POST.get('name'))
            )
            messages.success(request, 'new member has been successfully added to ' + str(district) )
            if is_secretary(request.user): 
                return redirect('secretary-dashboard')
    return redirect('admin-disrict-details', district.id)


@login_required(login_url='admin-login')
def district_member(request, pk):
    district=District.objects.get(id=pk)
    district_member = Church_Member.objects.filter(district = district)
    department=Department.objects.all()
    myFilter=DistrictMemberFilter(request.GET, queryset=district_member)
    district_member=myFilter.qs
    p=Paginator(district_member, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "secretary/district-members.html",{'district':district,'district_member':page,'department':department})


@login_required(login_url='admin-login')
def filter_church_results_download(request, pk):
    district=District.objects.get(id=pk)
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + 'download ' + str(district) + ' Church Member Report'
    )
    mem=Church_Member.objects.filter(district = district)
    myFilter=DistrictMemberFilter(request.GET, queryset=mem)
    mem=myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="Church Member Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Church_Member._meta.fields]
    csv_writer.writerow(header_row)
    
    for mem in mem:
        data_row = [str(getattr(mem, field_name.name)) for field_name in Church_Member._meta.fields]
        csv_writer.writerow(data_row)
    return response


@login_required(login_url='admin-login')
def all_church_member_download(request, pk):
    district=District.objects.get(id=pk)
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + 'download ' + str(district) + ' All Church Member Report'
    )
    mem=Church_Member.objects.filter(district = district)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="All Church Member Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Church_Member._meta.fields]
    csv_writer.writerow(header_row)
    
    for mem in mem:
        data_row = [str(getattr(mem, field_name.name)) for field_name in Church_Member._meta.fields]
        csv_writer.writerow(data_row)
    return response

@login_required(login_url='admin-login')
def edit_member(request, pk):
    mem = Church_Member.objects.get(id=pk)
    form = ChurchMemberForm(instance=mem)
    if request.method == 'POST':
        form= ChurchMemberForm(request.POST,instance=mem)
        if form.is_valid():
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + 'updated ' + str(mem.name) 
            )
            messages.success(request, 'Updated Successfully')
        else:
            messages.error(request, form.errors)
    return render(request, "secretary/edit-member.html",{'form':form,'mem':mem})

@login_required(login_url='admin-login')
def district_new_member(request, pk):
    district=District.objects.get(id=pk)
    mem=Church_New_Member.objects.filter(district = district)
    myFilter=DistrictNewMemberFilter(request.GET, queryset=mem)
    mem=myFilter.qs
    p=Paginator(mem, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "secretary/district-new-member.html",{'mem':page,'district':district})


@login_required(login_url='admin-login')
def all_new_member_download(request, pk):
    district=District.objects.get(id=pk)
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + 'download ' + str(district) + ' New Member Report'
    )
    mem=Church_New_Member.objects.filter(district = district)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="New Member Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Church_Member._meta.fields]
    csv_writer.writerow(header_row)
    
    for mem in mem:
        data_row = [str(getattr(mem, field_name.name)) for field_name in Church_Member._meta.fields]
        csv_writer.writerow(data_row)
    return response


@login_required(login_url='admin-login')
def add_to_member(request, pk):
    mem=Church_New_Member.objects.get(id = pk)
    Church_Member.objects.create(
        district = mem.district,
        name = mem.name,
        email = mem.email,
        phone = mem.phone,
        address = mem.address,
        gender = mem.gender,
        age = mem.age   
    )
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + 'Changes ' + str(mem.name) +' to ' + str(mem.district) + ' Church Member Report'
    )
    messages.success(request, 'successfully added to '+ str(mem.district))
    mem.delete()
    return redirect('district-new-member', mem.district.id)

@login_required(login_url='admin-login')
def district_income(request, pk):
    district=District.objects.get(id=pk)
    district_income = Income.objects.get(district = district)
    tran = Transaction.objects.filter(district =district)
    myFilter=DistrictTransactionFilter(request.GET, queryset=tran)
    form = TransactionForm()
    tran=myFilter.qs
    credit_total = tran.filter(type='Credit').aggregate(Sum('amount'))['amount__sum'] or 0
    debit_total = tran.filter(type='Debit').aggregate(Sum('amount'))['amount__sum'] or 0
    p=Paginator(tran, 20)
    page_num = request.GET.get('page',1) 
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1) 
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "secretary/district-income.html",{'tran':page,'district':district,'district_income':district_income,
                        'debit_total':debit_total,'credit_total':credit_total,'form':form})

@login_required(login_url='admin-login')
def transaction_download(request, pk):
    district=District.objects.get(id=pk)
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + 'download ' + str(district) + ' Transaction Report'
    )
    tran = Transaction.objects.filter(district =district)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="Transaction Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Transaction._meta.fields]
    csv_writer.writerow(header_row)
    
    for tran in tran:
        data_row = [str(getattr(tran, field_name.name)) for field_name in Transaction._meta.fields]
        csv_writer.writerow(data_row)
    return response

@login_required(login_url='admin-login')
@secretary_only
def add_income(request, pk):
    district=District.objects.get(id=pk)
    if request.method == 'POST':
        try:
            if request.POST.get('type') == 'Debit':
                district_income = Income.objects.get(district = district)
                if district_income.income < int(request.POST.get('amount')):
                    messages.info(request, ' Insufficient Fund')
                    return redirect('district-income', district.id)
                else:
                    district_income.income -=  int(request.POST.get('amount'))
                    district_income.save()
                    form = TransactionForm(request.POST)
                    form=form.save(commit=False)
                    form.district = district
                    form.save()
                    Tracking.objects.create(
                        user= request.user.first_name,
                        action = str(request.user.first_name) + 'deducted ' + str(request.POST.get('amount')) + ' from ' + str(district) + ' Account'
                    )
            else:
                district_income = Income.objects.get(district = district)
                district_income.income +=  int(request.POST.get('amount'))
                district_income.save()
                form = TransactionForm(request.POST)
                form=form.save(commit=False)
                form.district = district
                form.save()
                Tracking.objects.create(
                    user= request.user.first_name,
                    action = str(request.user.first_name) + 'added ' + str(request.POST.get('amount')) + ' to ' + str(district) + ' Account'
                )
            messages.success(request, 'Income has been updated for ' + str(district) )
        except:
            messages.error(request, 'please make sure all fields are filled correctly')
        return redirect('district-income', district.id)

@login_required(login_url='admin-login')
def tran_receipt(request, pk):
    
    return render(request, "secretary/tran-receipt.html",{})

@login_required(login_url='admin-login')
def send_district_mail(request, pk):
    district=District.objects.get(id=pk)
    if request.method == 'POST':
        member = Church_Member.objects.filter(district=district)
        for i in member:
            mail_subject = request.POST.get('subject').upper()
            message = render_to_string(
                'email_template/send_members_email.html',
                {
                    'message':request.POST.get('message')
                },
            )
            email = EmailMessage(mail_subject, message, to=[i.email])
            email.content_subtype = "html"
            email.send(fail_silently=False)
        messages.success(request, 'email has been sent successfully')
        return redirect('district-member', district.id)


@login_required(login_url='admin-login')
def district_attendance(request, pk): 
    district=District.objects.get(id=pk)
    form = DistrictAttendanceForm()
    district_attendance = Church_Attendance.objects.filter(district = district)
    myFilter=DistrictAttendanceFilter(request.GET, queryset=district_attendance)
    district_attendance=myFilter.qs
    p=Paginator(district_attendance, 20)
    page_num = request.GET.get('page',1) 
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1) 
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "secretary/district-attendance.html",{'district':district,'district_attendance':page,'form':form})

@login_required(login_url='admin-login')
@secretary_only
def add_district_attendance(request, pk):
    district=District.objects.get(id=pk)
    form = DistrictAttendanceForm()
    if request.method == 'POST':
        form = DistrictAttendanceForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.district = district
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + 'takes attendance for ' + str(district) + ' Church',
            )
            messages.success(request, 'Attecndance successfully taken for ' + str(district) )
    return redirect('district-attendance', district.id)



@login_required(login_url='admin-login')
def district_attendance_download(request, pk):
    district=District.objects.get(id=pk)
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + 'download ' + str(district) + ' Attendance Report'
    )
    attendance = Church_Attendance.objects.filter(district =district)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="Attendance Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Church_Attendance._meta.fields]
    csv_writer.writerow(header_row)
    
    for attendance in attendance:
        data_row = [str(getattr(attendance, field_name.name)) for field_name in Church_Attendance._meta.fields]
        csv_writer.writerow(data_row)
    return response