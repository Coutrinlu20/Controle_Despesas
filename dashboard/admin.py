from django.contrib import admin
from .models import DashboardSummary, DashboardChart, DashboardNotification

@admin.register(DashboardSummary)
class DashboardSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_income', 'total_expense', 'balance', 'period_start', 'period_end')
    list_filter = ('user', 'period_start', 'period_end')

@admin.register(DashboardChart)
class DashboardChartAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'chart_type', 'created_at')
    list_filter = ('user', 'chart_type')

@admin.register(DashboardNotification)
class DashboardNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
