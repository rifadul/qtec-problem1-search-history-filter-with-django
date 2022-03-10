from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.keyword

    def __unicode__(self):
        return 
