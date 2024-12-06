from django.contrib import admin
from django.contrib import admin
from transactions.models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'date', 'category')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('description',)


