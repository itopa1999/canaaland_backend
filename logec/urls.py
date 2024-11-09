from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/question/', LOGECCreateQuestionView.as_view()),
    path('list/questions/', LOGECListQuestionView.as_view()),
    path('get/question/<int:pk>/', LOGECGetQuestionView.as_view()),
    path('register/member/', LOGECRegisterMemberView.as_view()),
    path('list/members/', LOGECListMemberView.as_view()),
    path('update/member/<int:pk>/', LOGECUpdateMemberView.as_view()),
    path('members/details/<int:pk>/', LOGECMemberDetailsView.as_view()),
    path('comment/sermon/<int:sermon_id>/', LOGECSermonCommentView.as_view()),
    path('comment/sermon/<int:pk>/delete/', LOGECDeleteCommentView.as_view()),

    path('register/new/member/', LOGECRegisterNewMemberView.as_view()),
    path('list/new/members/', LOGECListNewMemberView.as_view()),
    path('new/members/details/<int:pk>/', LOGECNewMemberDetailsView.as_view()),
    
    path('create/sermon/', LOGECSermonView.as_view()),
    path('delete/sermon/<int:pk>/', LOGECDeleteSermonView.as_view()),
    path('update/sermon/<int:pk>/', LOGECUpdateSermonView.as_view()),
    
    path('list/department/branch/', LOGECDepartmentBranchListView.as_view()),
    path('get/index/', LOGECIndexView.as_view()),
    path('list/sermons/', LOGECListSermonView.as_view()),
    path('get/sermon/<int:id>/', LOGECSermonDetailView.as_view()),

    path('list/donation/', LOGECListDonationView.as_view()),
    path('get/donation/<int:pk>/', LOGECDonationDetailsView.as_view()),
    

    path("paystack/deposit/", LOGECPaystackCashDepositView.as_view(), name="paystack-deposit-api"),
    path("paystack/confirm/deposit/<str:reference>", LOGECPaystackConfirmDepositView.as_view(), name="paystack-confirm-deposit"),

    
    
]