
from rest_framework import  status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.db.models.query_utils import Q
from .models import Contact,AccountAndContact
from .Serializers import ContactSerializer, ContactSerializerWithoutEmail,RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.



@api_view(["Post"],)
@permission_classes(())
def Registation(request):
    if request.method == 'POST':
        # try:
            datacopy = {}
            serializer = RegistrationSerializer(data=request.data)

            data = {}
            if serializer.is_valid():
                account = serializer.save()
                data["response"] = "successfully register a new user"
                data["phoneNumber"] = account.phone
                data["name"] = account.username
                data["emailId"] = account.email
                token = Token.objects.get(user=account).key
                data["token"] = token
                
                datacopy["name"] = account.username
                datacopy["emailId"] = account.email
                datacopy["phoneNumber"] = account.phone
                datacopy["isRegister"] = True
                serializer2 = ContactSerializer(data=datacopy)
                if serializer2.is_valid():
                    serializer2.save()
                else:
                    data = serializer2.errors
                    print("2 error")
            else:
                data = serializer.errors
            
            return Response(data)
        # except:
        #     return Response({'Error':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["Post",])
@permission_classes((IsAuthenticated,))
def SearchByName(request):
  
        if request.method == 'POST':
            try:
                Error_string = {"Error" :"Require Field for Search query not mention"}
                
                if "name" in request.data:
                    Uname = request.data["name"]
                    
                    startWidth = Contact.objects.filter(name__startswith=Uname)
                    contains = Contact.objects.filter(name__contains=Uname).exclude(name__startswith=Uname)
                    
                    serializer1 = ContactSerializerWithoutEmail(startWidth,many=True)
                    serializer2 = ContactSerializerWithoutEmail(contains,many=True)
                    
                
                    return Response(serializer1.data + serializer2.data, status=status.HTTP_201_CREATED)
               
                    
                return Response(Error_string,status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'Error':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["Post",])
@permission_classes((IsAuthenticated,))
def SearchByPhoneNumber(request):
    
    Error_string = {"Error" : "Require Field for Search query not mention"}
    if request.method == 'POST':
        try:
            if "phoneNumber" in request.data:
                Pnumber = request.data["phoneNumber"]
                reqUser = request.user
                filteredResult = Contact.objects.filter(phoneNumber=Pnumber)
                registerUser = Contact.objects.filter(phoneNumber=Pnumber).filter(isRegister=True)

                serializer = ContactSerializerWithoutEmail(filteredResult,many=True)    #  not register user serializer
                print(registerUser.count())
                if(registerUser.count())==1:
                    accountOfPnumber = AccountAndContact.objects.filter(account__phone = Pnumber)
                    for acc in accountOfPnumber:
                        if str(acc.contact.phoneNumber) == str(reqUser):
                            serializer = ContactSerializer(registerUser,many=True)  # register user serializer
                            
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            
            return Response(Error_string,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Error':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
@api_view(["Post",])
@permission_classes((IsAuthenticated,))
def MarkNumberSpam(request):
    if request.method == 'POST':
        try:
            if "phoneNumber" in request.data:
                Pnumber = request.data["phoneNumber"]
                filteredResult = Contact.objects.filter(phoneNumber=Pnumber)
                existingNumber = False
                for ph in filteredResult:
                    ph.spamCount += 1
                    existingNumber = True
                    ph.save()
                
                # if any random number add the number and increment the spam counter
                if not existingNumber:
                    obj = Contact(name="SPAM",phoneNumber=Pnumber,spamCount=1)
                    obj.save()
                    
                return Response({"response" : "Number marked spam successfully!"}, status=status.HTTP_201_CREATED)
            return Response({"Error" : "Require Field for Search query not mention"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Error':"Internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    