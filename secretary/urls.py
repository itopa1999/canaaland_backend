from django.urls import path, include
from .import views

urlpatterns = [
    path('admin-add-member/<int:pk>', views.admin_add_member, name="admin-add-member"),
    path('admin-add-new-member/<int:pk>', views.admin_add_new_member, name="admin-add-new-member"),
    
    path('district-member/<int:pk>', views.district_member, name="district-member"),

    path('filter_church_results_download/<int:pk>', views.filter_church_results_download, name="filter_church_results_download"),
    path('all_church_member_download/<int:pk>', views.all_church_member_download, name="all_church_member_download"),
    
    path('edit-member/<int:pk>', views.edit_member, name="edit-member"),
    path('district-new-member/<int:pk>/', views.district_new_member, name="district-new-member"),
    path('all_new_member_download/<int:pk>/', views.all_new_member_download, name="all_new_member_download"),
    path('add-to-member/<int:pk>', views.add_to_member, name="add-to-member"),
    path('district-income/<int:pk>', views.district_income, name="district-income"),
    path('transaction_download/<int:pk>', views.transaction_download, name="transaction_download"),
    path('add-income/<int:pk>', views.add_income, name="add-income"),
    path('tran-receipt/<int:pk>', views.tran_receipt, name="tran-receipt"),
    path('secretary-dashboard', views.secretary_dashboard, name="secretary-dashboard"),
    path('send-district-mail/<int:pk>', views.send_district_mail, name="send-district-mail"),
    path('district-attendance/<int:pk>', views.district_attendance, name="district-attendance"),
    path('add-district-attendance/<int:pk>', views.add_district_attendance, name="add-district-attendance"),
    path('district-attendance-download/<int:pk>', views.district_attendance_download, name="district-attendance-download"),
    path('add-income/<int:pk>', views.add_income, name="add-income"),
    
]