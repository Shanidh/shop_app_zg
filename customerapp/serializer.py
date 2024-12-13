from rest_framework import serializers

from shop.models import CustomUser


class CustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateCustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value  
    

class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)   
    price = serializers.CharField(read_only=True)      