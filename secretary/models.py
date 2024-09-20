from django.db import models
from django.utils import timezone
from users.models import District
from administrator.models import Department
import django
from django.db.models import Sum
# Create your models here.


class Church_Attendance(models.Model):
    district = models.ForeignKey(District,on_delete=models.SET_NULL,null=True, blank=True)
    children_boy = models.IntegerField(blank=True)
    children_girl = models.IntegerField(blank=True)
    men = models.IntegerField(blank=True)
    women = models.IntegerField(blank=True)
    date = models.DateField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['date']
        indexes = [
            models.Index(fields=['date']),
        ]
        
        
    def __str__(self):
        return f"{self.district}"
    
    

class Transaction(models.Model):
    type =(('Debit', 'Debit'),('Credit', 'Credit'))
    district = models.ForeignKey(District,on_delete=models.SET_NULL,null=True, blank=True)
    amount = models.IntegerField(blank=True)
    description = models.CharField(max_length=500, blank=True)
    type = models.CharField(max_length=500,default='Credit', choices=type)
    date = models.DateField(default=django.utils.timezone.now)

    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]
        
    def __str__(self):
        return f"{self.district}"
    
    

class Income(models.Model):
    district = models.ForeignKey(District, on_delete=models.SET_NULL,null=True, blank=True)
    income = models.IntegerField(blank=True)
    
    
    def total_income():
        total_income = Income.objects.all().aggregate(Sum('income'))['income__sum'] or 0
        
        return total_income

    class Meta:
        ordering = ['district']
        indexes = [
            models.Index(fields=['district']),
        ]
        
    def __str__(self):
        return f"{self.district}"
    

class Church_Member(models.Model):
    sex =(('Male', 'Male'),('Female', 'Female'),)
    district = models.ForeignKey(District,on_delete=models.SET_NULL,null=True, blank=True)
    name = models.CharField(max_length=200, blank=True,null=True)
    email = models.EmailField(max_length=200, null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    address= models.CharField(max_length=200, blank=True,null=True)
    gender = models.CharField(max_length=200, blank=True,null=True,choices=sex,default='Male')
    age = models.IntegerField(null=True,blank=True)
    country = models.CharField(max_length=200, blank=True,null=True, default='Nigeria')
    LGA= models.CharField(max_length=200, blank=True,null=True)
    department= models.ForeignKey(Department,blank=True, null=True, on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add=True,null=True)
    
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]
        
    def __str__(self):
        return f"{self.district}"
    
    

class Church_New_Member(models.Model):
    sex =(('Male', 'Male'),('Female', 'Female'),)
    district = models.ForeignKey(District,on_delete=models.SET_NULL,null=True, blank=True)
    name = models.CharField(max_length=200, blank=True,null=True)
    email = models.EmailField(max_length=200, null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    address= models.CharField(max_length=200, blank=True,null=True)
    gender = models.CharField(max_length=200, blank=True,null=True,choices=sex,default='Male')
    age = models.IntegerField(null=True,blank=True)
    date= models.DateTimeField(auto_now_add=True,null=True)
    is_member = models.BooleanField(default=False, null=True,blank=True)
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]
        
    def __str__(self):
        return f"{self.district}"
    


   
class Sermon(models.Model):
    title = models.CharField(max_length=200, blank=True,null=True) 
    paragraph1 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph2 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph3 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph4 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph5 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph6 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph7 = models.TextField(max_length=5000, blank=True,null=True)
    paragraph8 = models.TextField(max_length=5000, blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    img = models.ImageField(blank=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True,null=True)
    
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]
        
    def __str__(self):
        return self.title
    


class Testimony(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    testimony = models.TextField(max_length=1600, blank=True, null=True)
    approve = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True,null=True)
    
        
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]
    def __str__(self):
        return str(self.name)