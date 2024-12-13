import sys
import traceback
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from customerapp.serializer import CreateCustomerSerializer, CustomerSerializer
from django.contrib.auth import get_user_model, authenticate, logout, login

from shop.models import UserType
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.db import transaction

from customerapp.services import create_customer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _



@method_decorator(csrf_exempt, name='dispatch')
class CustomerLoginAPI(APIView):
    """API for Customer Login."""

    authentication_classes = []

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == UserType.CUSTOMER:
                # Login successful, return user data
                login(request, user)
                data = {
                   "Success": True,
                   "msg": "Login Success",
                }
                return Response(status=status.HTTP_201_CREATED, data=data)
                # return redirect("shopapp:customer_list") 
            else:
            # Login failed
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

class CustomerLogOutAPI(APIView):
    """API for Customer Logout."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user by ending the session."""
        logout(request)  # Clear the session
        return Response({"Success": True, "msg": "Logout successful."}, status=status.HTTP_200_OK)         
    

@method_decorator(csrf_exempt, name='dispatch')
class CustomerRegisterAPI(APIView):
    """API for creating User"""

    authentication_classes = []

    def post(self, request):
        try:
            serializer = CreateCustomerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                create_customer(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED, data=_("User created succesfully."))
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "User Registration Failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)    