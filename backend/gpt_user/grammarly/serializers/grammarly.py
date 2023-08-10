from rest_framework import serializers

class GrammarlySerializer(serializers.Serializer):
    text = serializers.CharField()
    status =  serializers.BooleanField()
    suggestion = serializers.CharField()