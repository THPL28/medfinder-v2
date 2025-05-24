from rest_framework import serializers
from .models import Receita

class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['id', 'pdf', 'data_upload', 'texto_extraido']
