from rest_framework import serializers


class CustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateCustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()    
    email = serializers.CharField()   