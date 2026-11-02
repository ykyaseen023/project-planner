from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .models import Project

from .models import AssignedProject

from . serializers import ProjectSerializer,AssignedProjectSerializers

from rest_framework.response import Response

# Create your views here.

class ProjectListCreateView(ListCreateAPIView):

    queryset = Project.objects.filter(active_status=True)

    serializer_class = ProjectSerializer

class ProjectRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Project.objects.filter(active_status=True)

    serializer_class = ProjectSerializer

    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()

        # data ={'msg':'project deleted successfully'}

        # return Response(data,status=203)

class AssignedProjectsListCreateView(ListCreateAPIView):

    queryset = AssignedProject.objects.filter(active_status=True)
    
    serializer_class = AssignedProjectSerializers