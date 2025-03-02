from django.db import models

# Create your models here.


class LOGECNewMember(models.Model):
    sex =(('Male', 'Male'),('Female', 'Female'),)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True,blank=True)
    phone = models.IntegerField()
    address = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, blank=True,null=True,choices=sex,default='Male')
    office_address = models.CharField(max_length=200,null=True,blank=True)
    branch = models.CharField(max_length=200,default="Akure")
    is_single = models.BooleanField(default=True)
    is_member = models.BooleanField(default=True)
    age = models.IntegerField()
    date= models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]

    def __str__(self):
        return self.name
    

class LOGECMember(models.Model):
    sex =(('Male', 'Male'),('Female', 'Female'),)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True,blank=True)
    phone = models.IntegerField()
    gender = models.CharField(max_length=200, blank=True,null=True,choices=sex,default='Male')
    address= models.CharField(max_length=200)
    branch = models.CharField(max_length=200,default="Akure")
    department= models.CharField(max_length=200)
    date= models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['-name']),
        ]

    def __str__(self):
        return self.name






class LOGECSermon(models.Model):
    title  = models.CharField(max_length=200)
    bible_text = models.CharField(max_length=200)
    preacher  = models.CharField(max_length=200)
    sermon = models.TextField()
    posted_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]

    def __str__(self):
        return self.title
    



class LOGECSermonComment(models.Model):
    sermon  = models.ForeignKey(LOGECSermon,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True,blank=True)
    comment= models.TextField()
    date= models.DateTimeField(auto_now_add=True,null=True)

    def save(self, *args, **kwargs):
        self.comment = self.comment.strip()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]

    def __str__(self):
        return self.name
    



class LOGECDonation(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=200)
    ref = models.CharField(max_length=50)
    posted_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]

    def __str__(self):
        return self.title
    


class LOGECQuestion(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True,blank=True)
    phone= models.IntegerField()
    question = models.CharField(max_length=200)
    date= models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return self.name