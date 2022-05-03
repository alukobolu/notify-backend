from django.db import models
from accounts.models import UserAccount
from django.db.models.deletion import CASCADE

# Create your models here.
class Groups (models.Model):
    creator = models.ForeignKey(UserAccount, null=True,related_name="creator", blank=True, on_delete=CASCADE)
    group_members = models.ManyToManyField(UserAccount, related_name="group_members",null=True)
    group_admins = models.ManyToManyField(UserAccount, related_name="group_admins",null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    deleted = models.BooleanField(default=False)
      
    def __str__(self):
        return self.creator.user.email +" - "+self.name
    
class Contacts (models.Model):
    user = models.OneToOneField(UserAccount, null=True,related_name="contact_user", blank=True, on_delete=CASCADE)
    contact = models.ManyToManyField(UserAccount, related_name="contact",null=True)
    deleted = models.BooleanField(default=False)
    
    
    def __str__(self): 
        return self.user.user.email 
    