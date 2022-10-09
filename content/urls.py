from django.urls import re_path
from django.conf.urls.static import static
from django.urls import include, path
from . import  views
from office_file_tracking_system import  settings

app_name='content'

urlpatterns = [
                re_path(r'^scholarships/$', views.Show_Scholarships, name=''),
                re_path(r'^scholarships/(?P<s_id>\w+)', views.Scholarship_Detail, name='Scholarship_Detail'),
                path('track_application/', views.Track_Application, name='Track_Application'),
                re_path('apply/', views.Apply, name='Apply'),
                path('add_scholarship', views.Add_Scholarship, name='Add_Scholarship'),
                path('pending_approvals/', views.Show_Pending_Approvals, name='Show_Pending_Approvals'),
                path('track_student_applications/', views.Track_Student_Applications, name='Track_Student_Applications'),
                path('approve/', views.Approve, name='Approve'),
                path('reject/', views.Reject, name='Reject'),
                path('about/', views.About, name='About'),
                path('profile/', views.Profile, name='Profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
