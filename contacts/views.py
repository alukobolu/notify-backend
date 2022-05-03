from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  status
from rest_framework.permissions import IsAuthenticated
from accounts.models import User, UserAccount
from rest_framework.pagination import PageNumberPagination
from .models import Groups,Contacts
# Create your views here.

paginator = PageNumberPagination()
paginator.page_size = 30


# add contact
def addContact(request,email):
    #try:
    sender = request.user
    contact = UserAccount.objects.get(email = email)
    if Contacts.objects.filter(user = sender).exists == True:
        con  = Contacts.objects.get(user = sender)
        con.contact.add(contact)
        con.save()
    else:
        add = Contacts()
        add.user = sender
        add.save()
        add.contact.add(contact)
        add.save()
    return True
    #except:
        #return False

# create group
class CreateGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        creator = request.user
        users = request.data('emails')
        name = request.data('name')
        grp = Groups() 
        grp.creator = creator
        grp.name = name
        grp.save()
        creator_account = UserAccount.objects.get(user = creator)
        grp.group_admins.add(creator_account)
        grp.group_members.add(creator_account)
        if emails != "":
            emails = users.split(",")
            for email in emails:
                user = User.objects.get(email = email)
                user_account = UserAccount.objects.get(user = user)
                grp.group_members.add(user_account)
        grp.save()
        return Response("Created Successfully")

# get group
class GetGroup(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        context =[]
        user = request.user
        user_account = UserAccount.objects.get(user = user)
        groups = Groups.objects.filter(group_members=user_account,deleted=False)
        for grp in groups:
            data ={}
            data['name'] = grp.name
            member_list = grp.group_members.all()
            members = []
            for mem in member_list:
                mem_details = {}
                mem_details['firstname'] = mem.firstname
                mem_details['email'] = mem.email
                members.append(mem_details)
            data['members'] = members
            admin_list = grp.group_admins.all()
            admins = []
            for admin in admin_list:
                admin_details = {}
                admin_details['firstname'] = admin.firstname
                admin_details['email'] = admin.email
                admins.append(mem_details)
            data['admins'] = admins
        context.append(data)
        content = paginator.paginate_queryset(context, request)
        return paginator.get_paginated_response(content)

# get contacts
class GetContacts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        context=[]
        user = request.user
        user_account = UserAccount.objects.get(user = user)
        contacts = Contacts.objects.get(user = user_account)
        contact = contacts.contancts.all()
        for con in contact:
            data = {}
            data["firstname"] = con.firstname
            data["email"] = con.email
            context.append(data)
        return Response(context)

# make admin
# remove member from group
# delete group

