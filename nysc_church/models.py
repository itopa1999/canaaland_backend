from django.db import models

# Create your models here.




class NYSCSession(models.Model):
    batch = models.CharField(max_length=200)
    stream = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return f"{self.batch} {self.stream} {self.year}"



class NYSCNewComer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True,blank=True)
    phone= models.IntegerField()
    batch = models.CharField(max_length=200)
    stream = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    state_code = models.CharField(max_length=200)
    dob = models.DateField()
    department = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return f"{self.name} {self.batch} {self.stream} {self.year}"
    
    



class NYSCAttendance(models.Model):
    name = models.CharField(max_length=200)
    phone= models.IntegerField()
    batch = models.CharField(max_length=200)
    stream = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    state_code = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return f"{self.name} {self.batch} {self.stream} {self.year}"