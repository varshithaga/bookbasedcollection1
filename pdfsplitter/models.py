from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Frame(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='frames')
    prompt = models.TextField()
    frame_number = models.IntegerField()
    generated_image = models.ImageField(upload_to='generated_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
