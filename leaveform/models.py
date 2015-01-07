from django.db import models
from datetime import date
from django.contrib.auth.models import User


class user_leave(models.Model):
     user=models.CharField(max_length=50)
     leave_type=models.CharField(max_length=50)
     From_date = models.CharField(max_length=50)
     To_date = models.CharField(max_length=50)
     Timeoff=models.CharField(max_length=20)
     # date=models.IntegerField(max_length=50)
     # month=models.IntegerField(max_length=50)
     # year=models.IntegerField(max_length=50)
     # date1=models.IntegerField(max_length=50)
     # month1=models.IntegerField(max_length=50)
     # year1=models.IntegerField(max_length=50)
     WDay_apply=models.IntegerField(max_length=4)
     
     
     Remarks=models.CharField(max_length=200)
# class form_data(month.Model):
	

class Leave_status(models.Model):
     
     user = models.CharField(max_length=50)
     LeaveID=models.IntegerField('user_leave')
     From_date = models.CharField(max_length=50)
     To_date = models.CharField(max_length=50)
     Status = models.CharField(max_length=50)
     leave_type=models.CharField(max_length=50)


class new_user(models.Model):
     available_leave=models.CharField(max_length=200)
     auth = models.OneToOneField(User)
     username=models.CharField(max_length=500)
     password = models.CharField(max_length=500)
     gender= models.CharField(max_length=500)
     dob=models.CharField(max_length=200)
     mail=models.CharField(max_length=500)
     mob=models.CharField(max_length=2000)

    