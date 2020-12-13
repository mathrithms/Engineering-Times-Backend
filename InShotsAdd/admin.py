from django.contrib import admin
from .models import InShotsAds


@admin.register(InShotsAds)
class InShotsAdsRegister(admin.ModelAdmin):
    def has_add_permission(self, request):
        if InShotsAds.objects.count() == 0:
            return True
        else:
            return False
