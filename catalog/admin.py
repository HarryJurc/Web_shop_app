from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name', 'description')
