from django.shortcuts import render

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend


from .models import *
from .serializers import  *
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
# Create your views here.

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    
    

class GetActiveOrLatestSessionView(APIView):
    """API view to retrieve active or latest session."""

    def get(self, request):
        session = NYSCSession.objects.filter(active=True).first()  # Get active session
        
        if not session:
            session = NYSCSession.objects.order_by('-id').first()  # Get latest session if no active one exists

        if session:
            serializer = NYSCSessionSerializer(session)  # Pass actual instance
            return Response(serializer.data)

        return Response(None)


class NYSCSessionView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = NYSCSessionSerializer
    queryset = NYSCSession.objects.all()
    
    

class MarkSessionActiveView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self, request):
        session_id = request.query_params.get("id") 

        if not session_id:
            return Response({"detail": "Session ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        session = get_object_or_404(NYSCSession, id=session_id)

        NYSCSession.objects.update(active=False)

        session.active = True
        session.save()

        return Response({"message": f"Session {session.batch} marked as active."}, status=status.HTTP_200_OK)
    
    


class NYSCNewComerCreateView(generics.GenericAPIView):
    serializer_class = NYSCNewComerSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': 'Successfully.',
        }, status=status.HTTP_201_CREATED)
        
        

class NYSCAttendanceCreateView(generics.GenericAPIView):
    serializer_class = NYSCAttendanceSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': 'Successfully.',
        }, status=status.HTTP_201_CREATED)
        
        


class NYSCNewComerListView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    queryset = NYSCNewComer.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = NYSCNewComerSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['year', 'batch', 'stream', 'date']
    search_fields = ['name', 'email', 'phone','year', 'batch', 'stream','department','state_code']
    
    
class NYSCAttendanceListView(generics.ListAPIView):
    permission_classes =[IsAuthenticated]
    queryset = NYSCAttendance.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = NYSCAttendanceSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['year', 'batch', 'stream', 'date']
    search_fields = ['name', 'email', 'phone','year', 'batch', 'stream','department','state_code', 'date']
    
    


@api_view(["POST"])
def contact_form(request):
    """
    API endpoint to handle contact form submission and send an email.
    """
    data = request.data
    name = data.get("name")
    email = data.get("email", "No Email Provided")
    phone = data.get("phone")
    question = data.get("question")

    subject = "New Contact Form Submission"
    message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{question}"
    recipient_email = email

    try:
        # Send email
        send_mail(subject, message, email, [recipient_email])
        return Response({"message": "Message received successfully!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": f"Failed to send email! {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addSession(request):
    if request.method == 'POST':
        # Extract form data
        year = request.data.get('year')
        batch = request.data.get('batch')
        stream = request.data.get('stream')
        active = request.data.get('active')
        
        existing_session = NYSCSession.objects.filter(year=year, batch=batch, stream=stream).first()
        if existing_session:
            if active == 'yes':
                NYSCSession.objects.update(active=False)

                # Set the existing session as active
                existing_session.active = True
                existing_session.save()
            return Response({"message": "Session already exists.", "session_name": existing_session.batch}, status=status.HTTP_200_OK)

        
        session = NYSCSession.objects.create(
            year = year,
            batch = batch,
            stream = stream,
        )   
        if active == 'yes':
            NYSCSession.objects.update(active=False)
            session.active = True
            session.save()

        # Return a JSON response
        return Response({'message': 'Form submitted successfully'}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)