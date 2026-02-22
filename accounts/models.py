from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser): # using custom user model becuse it conatains name,email.. and we can add more fields
    
    PRIORTIY_CHOICES =[
        ('normal', 'Normal'),
        ('elderly', 'Elderly'),
        ('disabled', 'Disabled'),
        ('pregnant', 'Pregnant'),
        ('vip', 'VIP')
    ]

    
    phone = models.CharField(max_length=10,blank=True,null=True)


    priority_type = models.CharField(
        max_length=20,
        choices=PRIORTIY_CHOICES,
        default='normal',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'users'

