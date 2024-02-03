
from rest_framework import serializers
from .models import *


from .models import Address, PhoneNumber, Country, State, Company

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Company
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    company_details = CompanySerializer()
    phone_details = PhoneNumberSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    secondary_email = serializers.EmailField()
    gender = serializers.CharField()
    dob = serializers.DateField()
    joining_date = serializers.DateField()
    address = AddressSerializer()
    tenant_id = serializers.CharField()
    role = RoleSerializer()