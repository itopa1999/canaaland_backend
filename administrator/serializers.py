from django import forms
from django.contrib.auth.models import Group  
from users.models import User
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from datetime import datetime, date
from rest_framework import status
from rest_framework.response import Response

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=50,
        required=True,
        allow_blank=False
    )
    password = serializers.CharField(max_length=50)



class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'



class TakeAttendanceSerializer(serializers.Serializer):
    day = serializers.CharField(
        required = True,
        allow_blank = False
    )
    member = serializers.CharField(
        required = True,
        allow_blank = False
    )



class RegisterMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

    def validate(self, data):
        year = datetime.now()
        email = data.get('email')
        phone = data.get('phone')
        name = data.get('name')
        date = data.get('date')

        if Member.objects.filter(Q(email=email)| Q(phone=phone) | Q(name=name),date__year =year.year ).exists():
            raise serializers.ValidationError("you have already registered for this year conference.")

        return data




class GetDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


    
class GetMemberSerializer(serializers.ModelSerializer):
    department = GetDepartmentSerializer()
    class Meta:
        model = Member
        fields = "__all__" 


class GetAttendanceSerializer(serializers.ModelSerializer):
    member = GetMemberSerializer()
    class Meta:
        model = Attendance
        fields = "__all__"      
        


class GetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"  