from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import *
from .serializers import *
from django.http import HttpResponse
import csv
from datetime import datetime, date
from users.models import *
from django.db.models import Sum
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q



from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination




# Create your views here.


def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_secretary(user):
    return user.groups.filter(name='secretary').exists()


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    @swagger_auto_schema(tags=['Auth'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        
        if not User.objects.filter(email=email).exists():
            return Response(
                {"detail": "No user associated with provided detail"},
                status=status.HTTP_400_BAD_REQUEST,
            )  
        user = get_object_or_404(User, Q(email=email))
        
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            decoded_token = AccessToken(access_token)
            expiration_time = datetime.fromtimestamp(decoded_token["exp"])

            if user.is_active == False:
                return Response(
                    {
                        "detail": "Account is inactive"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # send_login_successful_email(user)

            return Response(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "group":user.groups.values_list('name', flat=True),
                    "refresh": str(refresh),
                    "access": access_token,
                    "expiry": expiration_time,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"detail": "Credentials is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        


class AdminDashboard(APIView):
    permission_classes =[IsAuthenticated]
    @swagger_auto_schema(tags=['ApiRequests'])
    def get(self, request, *args, **kwargs):
        year = datetime.now()
        attend=Attendance.objects.filter(date__year=year.year).count()
        member_count=Member.objects.filter(date__year=year.year).count()
        question_count=Question.objects.filter(date__year=year.year).count()

        attend_2024=Attendance.objects.filter(date__year=2024).count()
        count_2024=Member.objects.filter(date__year=2024).count()
        question_count_2023=Question.objects.filter(date__year=2023).count()
        count_2023=Member.objects.filter(date__year=2023).count()
        question_count_2024=Question.objects.filter(date__year=2024).count()
        return Response(
            {
                "year": year,
                "attend": attend,
                "member_count": member_count,
                "question_count": question_count,
                "count_2023":count_2023,
                'count_2024':count_2024,
                'attend_2024':attend_2024,
                "question_count_2023":question_count_2023,
                'question_count_2024':question_count_2024
                
            },
            status=status.HTTP_200_OK,
        )



class CreateQuestionView(generics.GenericAPIView):
    serializer_class = CreateQuestionSerializer
    @swagger_auto_schema(tags=['ApiRequests'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Question submitted successfully!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class TakeAttendanceView(generics.GenericAPIView):
    serializer_class = TakeAttendanceSerializer
    @swagger_auto_schema(tags=['ApiRequests'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date1 = datetime(2025, 3, 27).date()
        date2 = datetime(2025, 3, 28).date()
        date3 = datetime(2025, 3, 29).date()
        date4 = datetime(2025, 3, 30).date()
        member = serializer.validated_data.get("member")
        day = serializer.validated_data.get("day")
        if day == 'day1':
            if datetime.now().date() == date1:
                mem = Validation(member)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 1').exists():
                        return Response({
                            'detail': 'You have already mark your attendance for Day 1.',
                        }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 1'
                        )
                        return Response({
                            'message': 'Congratulations you have mark your attendance for Day 1.',
                        }, status=status.HTTP_201_CREATED)

                return Response({
                    'detail': f'We cannot find any member that is associate with this {member}, Check for typo error or Register',
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'detail': 'Sorry Attendance for "Day 1" is invalid.',
                }, status=status.HTTP_400_BAD_REQUEST)
            
        elif day == 'day2':
            if datetime.now().date() == date2:
                mem = Validation(member)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 2').exists():
                        return Response({
                            'detail': 'You have already mark your attendance for Day 2.',
                        }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 2'
                        )
                        return Response({
                            'message': 'Congratulations you have mark your attendance for Day 2.',
                        }, status=status.HTTP_201_CREATED)
                return Response({
                    'detail': f'We cannot find any member that is associate with this {member}, Check for typo error or Register',
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'detail': 'Sorry Attendance for "Day 2" is invalid.',
                }, status=status.HTTP_400_BAD_REQUEST)

        elif day == 'day3':
            if datetime.now().date() == date3:
                mem = Validation(member)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 3').exists():
                        return Response({
                            'detail': 'You have already mark your attendance for Day 3.',
                        }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 3'
                        )
                        return Response({
                            'message': 'Congratulations you have mark your attendance for Day 3.',
                        }, status=status.HTTP_201_CREATED)
                return Response({
                    'detail': f'We cannot find any member that is associate with this {member}, Check for typo error or Register',
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'detail': 'Sorry Attendance for "Day 3" is invalid.',
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if datetime.now().date() == date4:
                mem = Validation(member)
                if mem is not None:
                    if Attendance.objects.filter(member__name = mem, day='Day 4').exists():
                        return Response({
                            'detail': 'You have already mark your attendance for Day 4.',
                        }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        Attendance.objects.create(
                            member = mem,
                            day='Day 4'
                        )
                        return Response({
                            'message': 'Congratulations you have mark your attendance for Day 4.',
                        }, status=status.HTTP_201_CREATED)
                return Response({
                    'detail': f'We cannot find any member that is associate with this {member}, Check for typo error or Register',
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'detail': 'Sorry Attendance for "Day 4" is invalid.',
                }, status=status.HTTP_400_BAD_REQUEST)




def Validation(member):
    if member.isdigit() and len(member) <=12:
        member = member[1:]
    else:
        member= member
    mem = Member.objects.filter(Q(email__icontains=member) | Q(phone__icontains=member),date__year=2025).first()
    if mem is None:
        pass
    else:
        return mem


class RegisterMemberView(generics.GenericAPIView):
    serializer_class = RegisterMemberSerializer
    @swagger_auto_schema(tags=['ApiRequests'])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': f'Hi {instance.name}, your registration was successful',
        }, status=status.HTTP_201_CREATED)



class GetDepartmentView(APIView):
    @swagger_auto_schema(tags=['ApiRequests'])
    def get(self, request):
        department = Department.objects.all()
        serializer_department = GetDepartmentSerializer(department, many=True)
        return Response({
            'department': serializer_department.data,
        }, status=status.HTTP_201_CREATED)



class GetMembersView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    queryset = Member.objects.all()
    serializer_class = GetMemberSerializer

    filter_backends = (SearchFilter, OrderingFilter)
    
    search_fields = ['name', 'email','phone','gender','assembly','department__name',
                     'district','denomination','country','date']  # Fields for searching
    ordering_fields = ['name', 'department','date']



class DownloadMemberCSView(APIView):
    permission_classes =[IsAuthenticated]
    @swagger_auto_schema(tags=['ApiRequests'])
    def get(self, request):
        mem=Member.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="All_Register_Member_Report.csv"'

        
        csv_writer = csv.writer(response)
        header_row = [field_name.verbose_name for field_name in Member._meta.fields]
        csv_writer.writerow(header_row)
        
        for mem in mem:
            data_row = [str(getattr(mem, field_name.name)) for field_name in Member._meta.fields]
            csv_writer.writerow(data_row)
        return response




class GetAttendanceView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = GetAttendanceSerializer

    filter_backends = (SearchFilter, OrderingFilter)
    
    search_fields = ['member__name', 'member__email','member__phone','member__gender','member__assembly','member__department__name',
                     'member__district','date','day']
    ordering_fields = ['member__name', 'member__department','date','day']



class DownloadAttendanceCSView(APIView):
    permission_classes =[IsAuthenticated]
    @swagger_auto_schema(tags=['ApiRequests'])
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="All_Attendance_Report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone','Gender', 'Day','Assembly', 'District','Department',' Date and Time'])
        attend=Attendance.objects.all()
        for attend in attend:
            writer.writerow([attend.member.name, attend.member.email, attend.member.phone,attend.member.gender,attend.day,attend.member.assembly,attend.member.district,attend.member.department,attend.date])

        return response




class GetQuestionView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = GetQuestionSerializer

