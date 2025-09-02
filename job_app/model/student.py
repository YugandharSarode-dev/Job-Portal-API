from django.db import models
from ..model.base import Base
                    
class Student(Base):
    ''' Model Fields '''
            
    name = models.CharField(unique=False, null=True, blank=True, max_length=200, db_index=True)
    city = models.CharField(unique=False, null=True, blank=True, max_length=200, db_index=True)
    marks = models.FloatField(null=True, blank=True, default=0.0, db_index=True)
    STATUS_BY = ((1, 'active'),(2, 'inactive'),(3, 'deleted'),)
    status = models.IntegerField(choices=STATUS_BY, default=1)
    GENDER_BY = ((1, 'male'),(2, 'female'),(3, 'other'),)
    gender = models.IntegerField(choices=GENDER_BY, default=1)
    email = models.EmailField(unique=True, null=True, blank=True, max_length=197)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return str(self.pk)
        