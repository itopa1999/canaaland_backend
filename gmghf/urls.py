from django.urls import path, include
from .views import *

urlpatterns = [
    path('list/programs/', GMGHFListProgramView.as_view()),
    path('add/programs/', GMGHFCreateProgramView.as_view()),
    path('delete/programs/<int:pk>/', GMGHFDeleteProgramView.as_view()),
    path('update/programs/<int:pk>/', GMGHFUpdateProgramView.as_view()),
    path('index/', GMGHFIndexView.as_view()),

    path('list/pictures/', GMGHFListPictureView.as_view()),
    path('add/picture/', GMGHFCreatePictureView.as_view()),
    path('delete/picture/<int:pk>/', GMGHFDeletePictureView.as_view()),


    path('list/videos/', GMGHFListVideosView.as_view()),
    path('add/video/', GMGHFCreateVideoView.as_view()),
    path('delete/video/<int:pk>/', GMGHFDeleteVideoView.as_view()),
    
    
    
    
]