from django.contrib import admin
from .models import Company, Intern, Job


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']

    class Meta:
        model = Company


class InternAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    list_display = ['designation', 'company']

    class Meta:
        model = Intern


class JobAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    list_display = ['designation', 'company']

    class Meta:
        model = Job


admin.site.register(Company, CompanyAdmin)
admin.site.register(Intern, InternAdmin)
admin.site.register(Job, JobAdmin)
