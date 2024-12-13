import sys
import traceback
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

from customerapp.serializer import CreateCustomerSerializer, CustomerSerializer, ProductListSerializer
from django.contrib.auth import get_user_model, authenticate, logout, login

from shop.models import CustomUser, UserType
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.db import transaction

from customerapp.services import create_customer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from customerapp.models import Order, Product



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

            # Check if the username already exists
            username = serializer.validated_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                return Response(
                    {"Success": False, "msg": "Username already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                create_customer(**serializer.validated_data)

            return Response(
                status=status.HTTP_201_CREATED,
                data={"Success": True, "msg": "User created successfully."}
            )
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
        

class ProductListAPI(APIView):
    """API for getting Product list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = Product.objects.all().values("id", "name", "description", "price").order_by("-created_at")
            serializer = ProductListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)     


class OrdersListAPI(APIView):
    """API to retrieve the list of orders for the authenticated user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch orders for the authenticated user
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            
            # Manually construct the response data without using a serializer
            orders_list = [
                {
                    "id": order.id,
                    "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "total_amount": str(order.total_price),
                    "status": order.status
                }
                for order in orders
            ]
            
            return Response(
                {"Success": True, "orders": orders_list},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"Success": False, "msg": "Failed to retrieve orders.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )           