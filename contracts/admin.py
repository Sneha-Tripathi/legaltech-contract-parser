## .\venv\Scripts\Activate.ps1
from django.contrib import admin
from .models import Contract, ExtractedClause, RiskFlag

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'uploaded_at'
    )

    search_fields = (
        'title',
    )

admin.site.register(ExtractedClause)
admin.site.register(RiskFlag)