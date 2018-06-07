
from django.db import models

#create your models here
class Songs(models.Model):
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published')
        )
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    content = models.TextField()

    def __str__(self):
        return self.title