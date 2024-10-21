from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False,blank=False)
    roll_number = models.CharField(max_length=255,null=False,blank=False,unique=True)
    age = models.IntegerField(null=True,blank=True)
    std_class = models.IntegerField(null=False,blank=False)
    
    def __str__(self):
        return f"{self.name} - {self.roll_number}"
    
    class Meta:
        ordering = ['id']