from django.db import models
from accounts.models import UserAccount
from django.db.models.deletion import CASCADE
# Create your models here.
class Notification_table (models.Model):
    send_user = models.ForeignKey(UserAccount, null=True,related_name="sender", blank=True, on_delete=CASCADE)
    recieve_user = models.ForeignKey(UserAccount, null=True,related_name="reciever", blank=True, on_delete=CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    message = models.CharField(max_length=10000, null=True, blank=True)
    
    
    def __str__(self):
        return self.recieve_user.user.email +" - "+self.title