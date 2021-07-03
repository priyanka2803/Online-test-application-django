from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import ModelState


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=0)
    mobile = models.PositiveIntegerField(null=False)
    pending=models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name

    @property
    def get_fullName(self):
        return self.user.first_name + " " +self.user.last_name
