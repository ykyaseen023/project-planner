from django.db import models

# Create your models here.

import uuid

from django_ckeditor_5.fields import CKEditor5Field


class BaseClass (models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta : 
         abstract = True


class Project(BaseClass):

    name = models.CharField(max_length=100)

    desciption = CKEditor5Field()

    document = models.FileField(upload_to='project-documents')

    class Meta :

        verbose_name = 'projects'

        verbose_name_plural = 'projects'

    def __str__(self):
        return self.name

class AssignedProject(BaseClass):

    project = models.ForeignKey('project',on_delete=models.PROTECT,related_name='project')

    coordinator = models.ForeignKey('authentication.profile',on_delete=models.PROTECT,related_name='coordinator')

    devolopers = models.ManyToManyField('authentication.profile')

    project_duration = models.IntegerField()

    project_start_date = models.DateField()

    project_end_date = models.DateField()

    completed = models.BooleanField(default=False)

    completed_date = models.DateField(null=True,blank=True)


    class Meta :
    
            verbose_name = 'Assigned projects'
    
            verbose_name_plural = 'Assigned projects'
    
    def __str__(self):
            return f'{self.project.name}-{self.project_start_date}'
    


