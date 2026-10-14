from rest_framework import serializers
from .models import Schedule, Touchpoint

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'mode', 'interval_min', 'interval_max', 'next_due_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'next_due_at', 'created_at', 'updated_at']

    def validate(self, data):
        mode = data.get('mode', self.instance.mode if self.instance else 'fixed')
        if mode == 'randomized' and not data.get('interval_max'):
            raise serializers.ValidationError("interval_max is required when mode is randomized.")
        if mode == 'randomized' and data.get('interval_min', 0) >= data.get('interval_max', 0):
            raise serializers.ValidationError("interval_max must be greater than interval_min.")
        return data

class TouchpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Touchpoint
        fields = ['id', 'schedule', 'due_at', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'schedule', 'due_at', 'created_at', 'updated_at']
