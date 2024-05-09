from rest_framework import serializers

from polls.models import Poll

class PollSerializer(serializers.ModelSerializer):
    agreeRate = serializers.SerializerMethodField()
    disagreeRate = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', required=False)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'agree', 'disagree', 'agreeRate', 'disagreeRate', 'createdAt']

    def get_agreeRate(self, obj):
        return obj.agree_rate
    
    def get_disagreeRate(self, obj):
        return obj.disagree_rate

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)
