from django.urls import path, include
from .import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
    path('admin-dashboard', views.dashboard, name="admin-dashboard"),
    path('admin-login', views.login_user, name="admin-login"),
    
    path('admin-member', views.member, name="admin-member"),
    path('admin-question', views.question1, name="admin-question"),
    path('admin-logout', LogoutView.as_view(template_name= "users/index.html"),name='admin-logout'),
    path('question', views.question, name="question"),
    
    path('filter-results-download', views.filter_results_download, name="filter-results-download"),
    path('filter-attendance-download', views.filter_attendance_download, name="filter-attendance-download"),
    path('all-results-download', views.all_results_download, name="all-results-download"),
    path('all-attendance-download', views.all_attendance_download, name="all-attendance-download"),
    
    path('admin-attendance', views.admin_attendance, name="admin-attendance"),
    path('admin-program', views.admin_program, name="admin-program"),
    
    path('admin-disrict-details/<int:pk>', views.admin_disrict_details, name="admin-disrict-details"),
    path('admin-district', views.admin_district, name="admin-district"),
    path('admin-program', views.admin_program, name="admin-program"),
    
    path('admin-district-member', views.admin_district_member, name="admin-district-member"),
    
    path('admin_member_download', views.admin_member_download, name="admin_member_download"),
    path('admin_filter_church_results_download', views.admin_filter_church_results_download, name="admin_filter_church_results_download"),
    path('admin-district-new-member', views.admin_district_new_member, name="admin-district-new-member"),
    path('admin_new_member_download', views.admin_new_member_download, name="admin_new_member_download"),
    path('admin-district-admin', views.admin_district_admin, name="admin-district-admin"),
    path('admin-district-transaction', views.admin_district_transaction, name="admin-district-transaction"),
    path('admin_district_transaction_download', views.admin_district_transaction_download, name="admin_district_transaction_download"),
    
    path('admin-tracking', views.admin_tracking, name="admin-tracking"),

    path('admin-sermon', views.admin_sermon, name="admin-sermon"),
    path('admin-testimony', views.admin_testimony, name="admin-testimony"),
    path('admin-testimony-approve/<int:pk>', views.admin_testimony_approve, name="admin-testimony-approve"),
    path('admin-testimony-delete/<int:pk>', views.admin_testimony_delete, name="admin-testimony-delete"),
    path('send-admin-mail', views.send_admin_mail, name="send-admin-mail"),
    path('admin_filter_church_results_download', views.admin_filter_church_results_download, name="admin_filter_church_results_download"),
    path('admin_filter_church_results_download', views.admin_filter_church_results_download, name="admin_filter_church_results_download"),

    
]