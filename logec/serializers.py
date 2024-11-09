from rest_framework import serializers
from .models import *
from django.db.models import Q

class LOGECCreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECQuestion
        fields = '__all__'

    def validate(self, data):
        name = data.get('name')

        if LOGECQuestion.objects.filter(name=name).exists():
            raise serializers.ValidationError("you have already have your info")

        return data
    

class LOGECListQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECQuestion
        fields = ['id','email','name']


class LOGECRegisterMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECMember
        fields = "__all__"

    def validate(self, data):
        email = data.get('email')
        phone = data.get('phone')
        name = data.get('name')

        if LOGECMember.objects.filter(Q(email=email), Q(phone=phone) , Q(name=name)).exists():
            raise serializers.ValidationError("you have already registered.")

        return data
    


class LOGECListMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECMember
        fields = ['id','name','phone','branch','gender']


class LOGECSermonCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECSermonComment
        exclude = ['sermon']

    


class LOGECSermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECSermon
        fields = "__all__"


    def validate(self, data):
        title = data.get('title')
        preacher = data.get('preacher')

        if LOGECSermon.objects.filter(Q(title=title), Q(preacher=preacher)).exists():
            raise serializers.ValidationError("This already exists.")

        return data



class LOGECListSermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECSermon
        exclude = ['sermon','bible_text']


class DepositSerializer(serializers.Serializer):
    title = serializers.CharField()
    amount = serializers.IntegerField()
    name = serializers.CharField()



class LOGECListDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECDonation
        fields = ['id','name','title','amount']


class LOGECDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECDonation
        fields = "__all__"



class LOGECListNewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECNewMember
        fields = ['id','name','phone','branch']


class LOGECNewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LOGECNewMember
        fields = "__all__"