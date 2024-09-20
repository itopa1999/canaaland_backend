from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('register_form', views.register_form, name="register_form"),
    path('attendance', views.attendance, name="attendance"),
    
    path('rules', views.rules, name="rules"),
    path('tenets', views.tenets, name="tenets"),
    path('vision', views.vision, name="vision"),
    path('fft', views.fft, name="fft"),
    path('hymns', views.hymns, name="hymns"), 
    path('hymns', views.hymns, name="hymns"), 
    path('offerings', views.offerings, name="offerings"), 
    
    path('admin-addadm/<int:pk>', views.admin_addadm, name="admin-addadm"), 
    path('admin-edit-admin/<int:pk>', views.admin_edit_admin, name="admin-edit-admin"), 
]