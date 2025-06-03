from rest_framework import serializers
from .models import Abonent, Tarif, Tolov

class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = '__all__'

class AbonentSerializer(serializers.ModelSerializer):
    tarif = TarifSerializer(read_only=True)

    class Meta:
        model = Abonent
        fields = '__all__'

class TolovSerializer(serializers.ModelSerializer):
    abonent = AbonentSerializer(read_only=True)

    class Meta:
        model = Tolov
        fields = '__all__'
