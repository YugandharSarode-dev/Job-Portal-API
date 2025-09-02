from django.db import models
from ..model.base import Base

class Skill(Base):
    name = models.CharField(max_length=100, unique=True)
    status_choices = ((1, 'active'), (2, 'inactive'), (3, 'deleted'))
    status = models.IntegerField(choices=status_choices, default=1)

    class Meta:
        db_table = 'skill'

    def __str__(self):
        return self.name
