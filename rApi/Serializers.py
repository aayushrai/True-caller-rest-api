from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Contact,Account

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name','phoneNumber','emailId','spamCount','isRegister']


class ContactSerializerWithoutEmail(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name','phoneNumber','spamCount']


class RegistrationSerializer(serializers.ModelSerializer):


    class Meta:
        model = Account
        fields = ['phone', 'username', 'password','email']
        extra_kwargs = {
                'password': {'write_only': True},
        }	


    def	save(self):
        if "email" not in self.validated_data:
            self.validated_data["email"] = None
             
        account = Account(
                    email=self.validated_data["email"],
                    phone = self.validated_data['phone'],
                    username=self.validated_data['username']
                )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account