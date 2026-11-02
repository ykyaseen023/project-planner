from rest_framework import serializers

from . models import Project,AssignedProject

from authentication.serializers import ProfileSerializer

from authentication.models import profile


class ProjectField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):
        return getattr(instance,self.source_attrs[0])

    def to_representation(self, value):
        return ProjectSerializer(value).data

class ProfileField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):
        return getattr(instance,self.source_attrs[0])

    def to_representation(self, value):
        return ProfileSerializer(value).data    
    
class ProjectSerializer(serializers.ModelSerializer):

    class Meta :

        model = Project

        fields ='__all__'

        read_only_fields = ['active_status']

class AssignedProjectSerializers(serializers.ModelSerializer):

    project = ProjectField(queryset=Project.objects.all())
    coordinator = ProfileField(queryset=profile.objects.filter(role='Project'))
    developers = ProfileField(queryset=profile.objects.filter(role='Developer'),many=True)

    class Meta :

        model = AssignedProject

        fields ='__all__'

        read_only_fields = ['active_status']