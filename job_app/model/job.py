from django.db import models
from job_app.model.skill import Skill
from ..model.base import Base
from .users import User
                    
class Job(Base):
    ''' Model Fields '''
            
    title = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(unique=False, null=True, blank=True, max_length=100, db_index=True)
    skills = models.TextField(null=True, blank=True, help_text='Comma-separated list of skills')
    location = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs', null=True, blank=True)
    
    STATUS_BY = ((1, 'active'),(2, 'inactive'),(3, 'deleted'),)
    status = models.IntegerField(choices=STATUS_BY, default=1)
    skills = models.ManyToManyField(Skill, blank=True)
    
    class Meta:
        db_table = 'job'

    def __str__(self):
        return str(self.title) if self.title else str(self.pk)
