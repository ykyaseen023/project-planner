from django.urls import path

from . import views

urlpatterns = [

    path('projects/',views.ProjectListCreateView.as_view()),
    path('projects/<str:uuid>/',views.ProjectRetriveUpdateDestroyView.as_view()),
    path('assigned-projects/',views.AssignedProjectsListCreateView.as_view())

]