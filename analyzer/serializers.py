from rest_framework import serializers


class MatchRequestSerializer(serializers.Serializer):
    linkedin_url = serializers.URLField(required=True)
    job_description = serializers.CharField(required=True)
    company_values = serializers.CharField(required=True)  # New field for company values


class MatchResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    match_score = serializers.CharField()
    cultural_fit_analysis = serializers.DictField()  # For nested analysis results
