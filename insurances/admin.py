from django.contrib import admin
from .models import Insurance,Invest_insure,User_insure
# Register your models here.
admin.site.register(Insurance)
admin.site.register(Invest_insure)
admin.site.register(User_insure)