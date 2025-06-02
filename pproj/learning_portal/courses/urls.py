from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('take_quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('discussions/<int:course_id>/', views.discussion_list, name='discussion_list'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('add_comment/<int:discussion_id>/', views.add_comment, name='add_comment'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
] 