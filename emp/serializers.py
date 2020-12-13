from rest_framework import serializers
from .models import Company, Intern, Job


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'logo']


class InternSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField('get_company')

    class Meta:
        model = Intern
        fields = ['company', 'designation', 'link', 'expire']

    def get_company(self, intern):
        return CompanySerializer(intern.company).data


class JobSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField('get_company')

    class Meta:
        model = Job
        fields = ['company', 'designation', 'link', 'expire']

    def get_company(self, job):
        return CompanySerializer(job.company).data
