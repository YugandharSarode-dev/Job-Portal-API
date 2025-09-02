from django.db import models
from ..model.base import Base
from .users import User
from .job import Job
                    
class Application(Base):
    ''' Model Fields '''
            
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    STATUS_BY = ((1, 'pending'),(2, 'accepted'),(3, 'rejected'))
    status = models.IntegerField(choices=STATUS_BY, default=1)

    class Meta:
        db_table = 'application'

    def __str__(self):
        return f"{self.applicant} - {self.job}" if self.applicant and self.job else str(self.pk)
