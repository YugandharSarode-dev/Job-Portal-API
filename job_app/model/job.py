from django.db import models
from job_app.model.skill import Skill
from ..model.base import Base
from .users import User
from .category import Category
from .location import Location

class Job(Base):
    title = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    
    # Foreign keys instead of CharField
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True)
    
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs', null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    
    STATUS_BY = ((1, 'active'), (2, 'inactive'), (3, 'deleted'))
    status = models.IntegerField(choices=STATUS_BY, default=1)
    
    class Meta:
        db_table = 'job'

    def __str__(self):
        return str(self.title) if self.title else str(self.pk)
