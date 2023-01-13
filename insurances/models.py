import sys
sys.path.append("..")
from django.db import models
from accounts.models import User
# Create your models here.
class Insurance(models.Model):
    name = models.CharField(max_length=100)
    descript = models.TextField()
    img_url = models.TextField()
    expire_day =models.IntegerField()
    release = models.BooleanField(default=False)
    premium = models.FloatField()
    compensation = models.FloatField()
    fund = models.FloatField()
    init_fund = models.FloatField()

    def __str__(self):
        return self.name

class Invest_insure(models.Model):
    invest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created') # on_delete for when artist is deleted then it's song is deleted too
    insure = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    cost = models.FloatField(default=0)
    revenue = models.FloatField(default=0)

    def __str__(self):
        return 'invest'
    
class User_insure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created') # on_delete for when artist is deleted then it's song is deleted too
    insure = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    date_buy = models.DateField()

    def __str__(self):
        return 'user'
    
    