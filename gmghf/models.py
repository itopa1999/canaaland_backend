from django.db import models

# Create your models here.

class GMGHFProgram(models.Model):
    title = models.CharField(max_length=5000)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return self.title
    


class GMGHFPicture(models.Model):
    picture = models.ImageField(upload_to='pictures/')

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return f"{self.id}"
    


class GMGHFVideo(models.Model):
    video = models.FileField(upload_to='videos/')

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]


    def __str__(self):
        return f"{self.id}"