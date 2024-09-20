from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from .filters import *
from django.http import HttpResponse
import csv
from datetime import datetime, date
from secretary.models import *
from users.models import *
from django.db.models import Sum
from users.forms import *
from secretary.forms import *
from users.decorators import *
# Create your views here.


def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_secretary(user):
    return user.groups.filter(name='secretary').exists()


def login_user(request):
    if request.method == "POST":
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            mail_subject = 'LOGIN NOIFICATION'
            message = render_to_string(
                'email_template/login_email.html',
                {
                    'name':user.first_name,
                },
            )
            email = EmailMessage(mail_subject, message, to=[request.POST.get('email')])
            email.content_subtype = "html"
            email.send(fail_silently=False)
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + ' Logged in ' 
            )
            if is_admin(user):
                return redirect('admin-dashboard')
            elif is_secretary(user):
                return redirect('secretary-dashboard')
            else:
                messages.info(request, 'No account found')
            
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('admin-login')


    return render(request, "adm/login.html")


@login_required(login_url='admin-login')
@admin_only
def dashboard(request):
    year = datetime.now()
    attend=Attendance.objects.filter(date__year=year.year).count()
    member_count=Member.objects.filter(date__year=year.year).count()
    question_count=Question.objects.filter(date__year=year.year).count()
    district = District.objects.count()
    district_member = Church_Member.objects.count()
    district_new_member = Church_New_Member.objects.count()
    district_user = User.objects.filter(groups=Group.objects.get(name='secretary')).count()
    income = Income.total_income()
    transaction = Transaction.objects.all()[:5]
    church_member = Church_Member.objects.all()[:5]
    track = Tracking.objects.all()[:6]
    sermon = Sermon.objects.count()
    testimony = Testimony.objects.filter(approve=True).count()
    return render(request, "adm/dashboard.html", {'year':year,'member_count':member_count,'attend':attend,'question_count':question_count,
                        'district':district,'district_member':district_member, 'district_user':district_user,'income':income,'transaction':transaction,
                        'church_member':church_member,'track':track,'district_new_member':district_new_member,'sermon':sermon,'testimony':testimony})




@login_required(login_url='admin-login')
def member(request):
    mem=Member.objects.all()
    department=Department.objects.all()
    myFilter=MemberFilter(request.GET, queryset=mem)
    mem=myFilter.qs
    count = len(mem)
    p=Paginator(mem, 40)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    
    return render(request, "adm/member.html",  {"mem":page,"department":department,'count':count})



@login_required(login_url='admin-login')
def filter_results_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' Downloaded Program Register Member Report' 
    )
    mem=Member.objects.all()
    myFilter=MemberFilter(request.GET, queryset=mem)
    mem=myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="Register Member Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Member._meta.fields]
    csv_writer.writerow(header_row)
    
    for mem in mem:
        data_row = [str(getattr(mem, field_name.name)) for field_name in Member._meta.fields]
        csv_writer.writerow(data_row)
    return response


@login_required(login_url='admin-login')
def all_results_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' Downloaded Program All Register Member Report' 
    )
    mem=Member.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="All Register Member Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Member._meta.fields]
    csv_writer.writerow(header_row)
    
    for mem in mem:
        data_row = [str(getattr(mem, field_name.name)) for field_name in Member._meta.fields]
        csv_writer.writerow(data_row)
    return response



@login_required(login_url='admin-login')
def question1(request):
    que=Question.objects.all()
    count=que.count()
    return render(request, "adm/question1.html",  {"que":que,"count":count})


@login_required(login_url='admin-login')
def admin_attendance(request):
    attend=Attendance.objects.all()
    department=Department.objects.all()
    myFilter=AttendanceFilter(request.GET, queryset=attend)
    attend=myFilter.qs
    count = len(attend)
    p=Paginator(attend, 40)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "adm/attendance.html",  {"attend":page,"count":count,'department':department})


@login_required(login_url='admin-login')
def filter_attendance_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' Downloaded Program Attendance Report' 
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Fltered Attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone','Gender', 'Day','Assembly', 'District','Department',' Date and Time'])
    attend=Attendance.objects.all()
    myFilter=AttendanceFilter(request.GET, queryset=attend)
    attend=myFilter.qs
    for attend in attend:
        writer.writerow([attend.member.name, attend.member.email, attend.member.phone,attend.member.gender,attend.day,attend.member.assembly,attend.member.district,attend.member.department,attend.date])

    return response

@login_required(login_url='admin-login')
def all_attendance_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' Downloaded Program All Attendance Report' 
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="All Attendance Report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone','Gender', 'Day','Assembly', 'District','Department',' Date and Time'])
    attend=Attendance.objects.all()
    for attend in attend:
        writer.writerow([attend.member.name, attend.member.email, attend.member.phone,attend.member.gender,attend.day,attend.member.assembly,attend.member.district,attend.member.department,attend.date])

    return response


@login_required(login_url='admin-login')
def question(request):
    if request.method=='POST':
        name = request.POST['name']
        email1 = request.POST['email']
        subject = request.POST['subject']
        question = request.POST['question']


        Question.objects.create(
            name=name,
            email=email1,
            subject=subject,
            question=question,
        )

        messages.success(request, "Hi " +name+ ", your question has been submitted,  we will contact you")
        return redirect('index')
    
@login_required(login_url='admin-login')
def admin_program(request):
    attend_2024=Attendance.objects.filter(date__year=2024).count()
    count_2024=Member.objects.filter(date__year=2024).count()
    question_count_2023=Question.objects.filter(date__year=2023).count()
    count_2023=Member.objects.filter(date__year=2023).count()
    question_count_2024=Question.objects.filter(date__year=2024).count()
    return render(request, "adm/program.html", {"count_2023":count_2023,'count_2024':count_2024,'attend_2024':attend_2024,
                    "question_count_2023":question_count_2023,'question_count_2024':question_count_2024})



@login_required(login_url='admin-login')
@admin_only
def admin_district(request):
    form = DistrictForm()
    district=District.objects.all()
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + ' Added ' + str(request.POST.get('name') + ' to District') 
            )
            messages.success(request, 'District added successfully')
        else:
            messages.error(request, form.errors)
    return render(request, "adm/district.html",{'district':district,'form':form})



@login_required(login_url='admin-login')
@admin_only
def admin_disrict_details(request, pk):
    district=District.objects.get(id=pk)
    district_user = User.objects.filter(groups=Group.objects.get(name='secretary'), district=district).first()
    district_member = Church_Member.objects.filter(district = district)
    district_new_member = Church_New_Member.objects.filter(district = district)
    district_income = Income.objects.get(district = district)
    district_transaction = Transaction.objects.filter(district = district)
    district_attendance = Church_Attendance.objects.filter(district = district)
    form1 = UserCreationForm()
    form2 = UserChangeForm(instance=district_user)
    form3=ChurchMemberForm()
    form4=ChurchNewMemberForm()
    form = DistrictForm(instance=district)
    if request.method == 'POST':
        form = DistrictForm(request.POST,instance=district)
        if form.is_valid():
            form.save()
            Tracking.objects.create(
                user= request.user.first_name,
                action = str(request.user.first_name) + ' Updated ' + str(district) 
            )
            messages.success(request, str(district) + ' has been updated sccessfully')
    return render(request, "adm/district-details.html",{'district':district,'district_user':district_user,'district_transaction':district_transaction,'district_member':district_member,
                            'district_income':district_income,'form':form,'form1':form1,'form2':form2,'form3':form3,'form4':form4,'district_new_member':district_new_member,
                            'district_attendance':district_attendance})


@login_required(login_url='admin-login')
@admin_only
def admin_district_member(request):
    district_member = Church_Member.objects.all()
    district = District.objects.all()
    department = Department.objects.all()
    myFilter=AdminMemberFilter(request.GET, queryset=district_member)
    district_member=myFilter.qs
    p=Paginator(district_member, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "adm/admin-district-member.html",{'district_member':page,'district':district,'department':department})

@login_required(login_url='admin-login')
@admin_only
def admin_member_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' downloaded All Church Member Report' 
    )
    mem=Church_Member.objects.all()
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
@admin_only
def admin_filter_church_results_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' downloaded Filtered Church Member Report' 
    )
    mem=Church_Member.objects.all()
    myFilter=AdminMemberFilter(request.GET, queryset=mem)
    mem=myFilter.qs
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="Filtered Church Member Report.csv"'
    
    csv_writer = csv.writer(response)
    header_row = [field_name.verbose_name for field_name in Church_Member._meta.fields]
    csv_writer.writerow(header_row)
    
    for mem in mem:
        data_row = [str(getattr(mem, field_name.name)) for field_name in Church_Member._meta.fields]
        csv_writer.writerow(data_row)
    return response

@login_required(login_url='admin-login')
@admin_only
def admin_district_new_member(request):
    mem=Church_New_Member.objects.all()
    district = District.objects.all()
    myFilter=AdminNewMemberFilter(request.GET, queryset=mem)
    mem=myFilter.qs
    p=Paginator(mem, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "adm/admin-district-new-member.html",{'mem':page,'district':district})
    
@login_required(login_url='admin-login')
@admin_only
def admin_new_member_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' downloaded New Member Report' 
    )
    mem=Church_New_Member.objects.all()
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
@admin_only
def admin_district_admin(request):
    district_user = User.objects.filter(groups=Group.objects.get(name='secretary'))
    form = UserCreationForm1()
    if request.method == 'POST':
        if User.objects.filter(district=request.POST.get('district')).exists():
            messages.info(request, 'District can only have 1 admin')
        else:
            form = UserCreationForm1(request.POST)
            if form.is_valid():
                form=form.save(commit=False)
                form.save()
                group= Group.objects.get(name='secretary')
                form.groups.add(group)
                messages.success(request, 'Add successfully')
                Tracking.objects.create(
                    user= request.user.first_name,
                    action = str(request.user.first_name) + ' created a new district ' + str(request.POST.get('name')) 
                )
            else:
                messages.error(request, form.errors)
    return render(request, "adm/admin-district-admin.html",{'district_user':district_user,'form':form})


@login_required(login_url='admin-login')
@admin_only
def admin_district_transaction(request):
    tran = Transaction.objects.all()
    district = District.objects.all()
    district_income = Income.objects.all().aggregate(Sum('income'))['income__sum'] or 0
    myFilter=AdminTransactionFilter(request.GET, queryset=tran)
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
    return render(request, "adm/admin-district-transaction.html",{'district':district,'tran':page,'debit_total':debit_total,'credit_total':credit_total,'district_income':district_income})


@login_required(login_url='admin-login')
@admin_only
def admin_district_transaction_download(request):
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' download Transaction Report'
    )
    tran = Transaction.objects.all()
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
@admin_only
def admin_tracking(request):
    track = Tracking.objects.all()
    myFilter=TrackingFilter(request.GET, queryset=track)
    track=myFilter.qs
    p=Paginator(track, 20)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    return render(request, "adm/admin-tracking.html",{'track':page})


@login_required(login_url='admin-login')
@admin_only
def admin_sermon(request):
    sermon = Sermon.objects.all()
    return render(request, "adm/admin-sermon.html",{'sermon':sermon})


@login_required(login_url='admin-login')
@admin_only
def admin_testimony(request):
    testimony = Testimony.objects.all()
    return render(request, "adm/admin-testimony.html",{'testimony':testimony})

@login_required(login_url='admin-login')
@admin_only
def admin_testimony_approve(request, pk):
    testimony = Testimony.objects.get(id=pk)
    testimony.approve = True
    testimony.save()
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' Approves ' + str(testimony.name) + ' Testimony'
    )
    messages.success(request, 'Testimony has been approved')
    return redirect('admin-testimony')
    
@login_required(login_url='admin-login')
@admin_only  
def admin_testimony_delete(request, pk):
    testimony = Testimony.objects.get(id=pk)
    Tracking.objects.create(
        user= request.user.first_name,
        action = str(request.user.first_name) + ' deletes ' + str(testimony.name) + ' Testimony'
    )
    testimony.delete()
    messages.success(request, 'Testimony has been deleted successfully')
    return redirect('admin-testimony')


@login_required(login_url='admin-login')
@admin_only 
def send_admin_mail(request):
    if request.method == 'POST':
        admin = User.objects.filter(groups=Group.objects.get(name='secretary'))
        for i in admin:
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
        return redirect('admin-district-admin')