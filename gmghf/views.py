from django.shortcuts import render

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import *
from .serializers import  *
# Create your views here.

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class GMGHFListProgramView(generics.ListAPIView):
    queryset = GMGHFProgram.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = GMGHFProgramSerializer



class GMGHFCreateProgramView(generics.GenericAPIView):
    permission_classes =[IsAuthenticated]
    serializer_class = GMGHFProgramSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            'message': 'Program added successfully.',
        }, status=status.HTTP_201_CREATED)



class GMGHFDeleteProgramView(generics.DestroyAPIView):
    permission_classes =[IsAuthenticated]
    queryset = GMGHFProgram.objects.all()
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Program deleted successfully"},
            status=status.HTTP_200_OK
        )
    


class GMGHFUpdateProgramView(generics.UpdateAPIView):
    permission_classes =[IsAuthenticated]
    queryset = GMGHFProgram.objects.all()
    serializer_class = GMGHFProgramSerializer
    def put(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "message": "Program updated successfully",
            },
            status=status.HTTP_200_OK
        )
    

class GMGHFIndexView(APIView):
    def get(self, request):
        programs = GMGHFProgram.objects.all()[:6]
        pictures = GMGHFPicture.objects.all()[:6]
        programs_serializer = GMGHFProgramSerializer(programs, many=True)
        pictures_serializer = GMGHFPictureSerializer(pictures, many=True, context={'request': request})
        return Response({"programs":programs_serializer.data
                         ,"pictures":pictures_serializer.data})
    


class GMGHFCreatePictureView(generics.CreateAPIView):
    permission_classes =[IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = GMGHFPictureSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Picture uploaded successfully.',
        }, status=status.HTTP_201_CREATED)
    

class GMGHFListPictureView(generics.ListAPIView):
    serializer_class = GMGHFPictureSerializer
    queryset = GMGHFPicture.objects.all()
    pagination_class = CustomPageNumberPagination

    
    

class GMGHFDeletePictureView(generics.DestroyAPIView):
    permission_classes =[IsAuthenticated]
    queryset = GMGHFPicture.objects.all()
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "picture deleted successfully"},
            status=status.HTTP_200_OK
        )




class GMGHFCreateVideoView(generics.CreateAPIView):
    permission_classes =[IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = GMGHFVideoSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Video uploaded successfully.',
        }, status=status.HTTP_201_CREATED)
    

class GMGHFListVideosView(generics.ListAPIView):
    serializer_class = GMGHFVideoSerializer
    queryset = GMGHFVideo.objects.all()
    pagination_class = CustomPageNumberPagination

    
    

class GMGHFDeleteVideoView(generics.DestroyAPIView):
    permission_classes =[IsAuthenticated]
    queryset = GMGHFVideo.objects.all()
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "video deleted successfully"},
            status=status.HTTP_200_OK
        )
