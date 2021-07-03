from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=0)
    mobile = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.user.first_name

    @property
    def get_fullName(self):
        return self.user.first_name + " "+self.user.last_name
