from django.db import models
from ..model.base import Base
                    
class Products(Base):
    ''' Model Fields '''
            
    title = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    description = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    quantity = models.IntegerField(unique=False, null=True, blank=True, db_index=True)
    STATUS_BY = ((1, '55'),)
    status = models.IntegerField(choices=STATUS_BY, default=1)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return str(self.pk)
        