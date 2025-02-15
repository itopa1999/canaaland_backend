from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/newComer/', NYSCNewComerCreateView.as_view()),
    path('get/session/', GetActiveOrLatestSessionView.as_view()),
    path('create/attendance/', NYSCAttendanceCreateView.as_view()),
    path("api/contact-form/", contact_form, name="contact_form"),
    path('list/session/', NYSCSessionView.as_view()),
    path('list/attendance/', NYSCAttendanceListView.as_view()),
    
    path("mark/session/active", MarkSessionActiveView.as_view()),
    path('list/newComers/', NYSCNewComerListView.as_view()),
    path('list/session/', NYSCSessionView.as_view()),
    path('list/session/', NYSCSessionView.as_view()),
    path("api/add/session/", addSession),
    
    
    
    
    
]