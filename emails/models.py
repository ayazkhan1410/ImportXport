from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class List(models.Model):
    email_list = models.CharField(max_length=50)
    
    def __str__(self):
        return self.email_list

class Subscriber(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="subscriber_list")
    email_address = models.EmailField(max_length=40)
    
    def __str__(self):
        return self.email_address

class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="list_email")
    body = models.CharField(max_length=255)
    message = RichTextUploadingField(blank=True,null=True)
    attachment = models.FileField(upload_to='email_attachments/', null=True,blank=True)
    send_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body
    
