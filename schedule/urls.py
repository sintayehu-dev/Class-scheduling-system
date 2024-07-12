from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.aboutus, name='aboutus'),
    path('help', views.help, name='help'),
    path('terms', views.terms, name='terms'),

    path('admin_dashboard', views.admindash, name='admindash'),

    path('add_teachers', views.addInstructor, name='addInstructors'),
    path('teachers_list/', views.inst_list_view , name='editinstructor'),
    path('delete_teacher/<int:pk>/', views.delete_instructor, name='deleteinstructor'),

    path('add_rooms', views.addRooms, name='addRooms'),
    path('rooms_list/', views.room_list, name='editrooms'),
    path('delete_room/<int:pk>/', views.delete_room, name='deleteroom'),

    path('add_timings', views.addTimings, name='addTimings'),
    path('timings_list/', views.meeting_list_view, name='editmeetingtime'),
    path('delete_meetingtime/<str:pk>/', views.delete_meeting_time, name='deletemeetingtime'),

    path('add_courses', views.addCourses, name='addCourses'),
    path('edit_tt', views.edittt, name='edit_tt'),
    path('courses_list/', views.course_list_view, name='editcourse'),
    path('delete_course/<str:pk>/', views.delete_course, name='deletecourse'),

    path('add_departments', views.addDepts, name='addDepts'),
    path('departments_list/', views.department_list, name='editdepartment'),
    path('delete_department/<int:pk>/', views.delete_department, name='deletedepartment'),
    
    path('add_batches', views.addBatches, name='addBatches'),
    path('batches_list/', views.batch_list, name='editbatch'),
    path('delete_batch/<int:pk>/', views.delete_batch, name='deletebatch'),

    path('add_sections', views.addSections, name='addSections'),
    path('sections_list/', views.section_list, name='editsection'),
    path('delete_section/<str:pk>/', views.delete_section, name='deletesection'),
    path('generate_timetable', views.generate, name='generate'),
    path('timetable_generation/', views.timetable, name='timetable'),
   
    
    path('viewer/', views.pdf_list, name='pdf_list'),
    path('viewer/about', views.about, name='about'),
    path('viewer/suggestion/', views.suggestion_view, name='suggestion'),
    path('viewer/suggestion/thanks/', views.suggestion_thanks_view, name='suggestion_thanks'),
    
    # path('viewer/', views.pdf_list, name='pdf_list'),
    path('viewer/<int:pk>/', views.view_pdf, name='view_pdf'),

    path('pdf/', views.upload_pdf, name='upload_pdf'),
    path('pdf/list', views.lists, name='lists'),
    path('delete/<int:pk>/', views.delete_pdf, name='delete_pdf'),
    path('download_pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    
    path('index1/', views.index1, name='index1'),
    path('manage/', views.admin_login, name='adminlogin'),
]
