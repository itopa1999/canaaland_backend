from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ParseError
from django.utils import timezone


class NYSCSessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NYSCSession
        fields = '__all__'





class NYSCNewComerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NYSCNewComer
        fields = '__all__'
        
        
    def validate(self, data):
        """Check if a NYSC newcomer with the same state_code, batch, year, and stream already exists."""
        state_code = data.get('state_code')
        batch = data.get('batch')
        year = data.get('year')
        stream = data.get('stream')
        
        if not NYSCSession.objects.filter(batch=batch, stream=stream, year=year, active=True).exists():
            raise ParseError("Unavailable for this Batch, Stream, and Year.")

        # Check if a similar entry exists in the database
        if NYSCNewComer.objects.filter(state_code=state_code, batch=batch, year=year, stream=stream).exists():
            raise ParseError("Already registered for this Batch.")

        return data
    
    
    
class NYSCAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NYSCAttendance
        fields = '__all__'
        
        
    def validate(self, data):
        """Check if a NYSC newcomer with the same state_code, batch, year, and stream already exists."""
        state_code = data.get('state_code')
        batch = data.get('batch')
        year = data.get('year')
        stream = data.get('stream')
        
        if not NYSCSession.objects.filter(batch=batch, stream=stream, year=year, active=True).exists():
            raise ParseError("Unavailable for this Batch, Stream, and Year.")

        today = timezone.now().date()
        # Check if a similar entry exists in the database
        if NYSCAttendance.objects.filter(state_code=state_code, batch=batch, year=year, stream=stream, date=today).exists():
            raise ParseError("Attendance already taken for today.")

        return data