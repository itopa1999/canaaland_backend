from django.urls import path, include
from .views import *
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('admin/dashboard/', AdminDashboard.as_view()),
    path('create/question/', CreateQuestionView.as_view()),
    path('take/attendance/', TakeAttendanceView.as_view()),
    path('register/member/', RegisterMemberView.as_view()),
    path('get/department/', GetDepartmentView.as_view()),
    path('list/member/', GetMembersView.as_view())

    # path('admin-question', GetMemberSerializer.sa_view(), name="admin-question"),
    # path('admin-logout', LogoutView.as_view(template_name= "users/index.html"),name='admin-logout'),
    # path('question', question, name="question"),
    
    # path('filter-results-download', filter_results_download, name="filter-results-download"),
    # path('filter-attendance-download', filter_attendance_download, name="filter-attendance-download"),
    # path('all-results-download', all_results_download, name="all-results-download"),
    # path('all-attendance-download', all_attendance_download, name="all-attendance-download"),
    
    # path('admin-attendance', admin_attendance, name="admin-attendance"),
    # path('admin-program', admin_program, name="admin-program"),
    
    # path('admin-disrict-details/<int:pk>', admin_disrict_details, name="admin-disrict-details"),
    # path('admin-district', admin_district, name="admin-district"),
    # path('admin-program', admin_program, name="admin-program"),
    
    # path('admin-district-member', admin_district_member, name="admin-district-member"),
    
    # path('admin_member_download', admin_member_download, name="admin_member_download"),
    # path('admin_filter_church_results_download', admin_filter_church_results_download, name="admin_filter_church_results_download"),
    # path('admin-district-new-member', admin_district_new_member, name="admin-district-new-member"),
    # path('admin_new_member_download', admin_new_member_download, name="admin_new_member_download"),
    # path('admin-district-admin', admin_district_admin, name="admin-district-admin"),
    # path('admin-district-transaction', admin_district_transaction, name="admin-district-transaction"),
    # path('admin_district_transaction_download', admin_district_transaction_download, name="admin_district_transaction_download"),
    
    # path('admin-tracking', admin_tracking, name="admin-tracking"),

    # path('admin-sermon', admin_sermon, name="admin-sermon"),
    # path('admin-testimony', admin_testimony, name="admin-testimony"),
    # path('admin-testimony-approve/<int:pk>', admin_testimony_approve, name="admin-testimony-approve"),
    # path('admin-testimony-delete/<int:pk>', admin_testimony_delete, name="admin-testimony-delete"),
    # path('send-admin-mail', send_admin_mail, name="send-admin-mail"),
    # path('admin_filter_church_results_download', admin_filter_church_results_download, name="admin_filter_church_results_download"),
    # path('admin_filter_church_results_download', admin_filter_church_results_download, name="admin_filter_church_results_download"),

    
]