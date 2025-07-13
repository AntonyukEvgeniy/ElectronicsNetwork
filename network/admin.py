from django.contrib import admin
from django.utils.html import format_html

from .models import NetworkNode, Product, ProductAvailability


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "country", "city", "supplier_link", "debt", "level"]
    list_filter = ["type", "country", "city"]
    search_fields = ["name", "email", "country", "city"]
    actions = ["clear_debt"]
    readonly_fields = ["level"]

    def supplier_link(self, obj):
        if obj.parent:
            url = f"/admin/network/networknode/{obj.parent.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.parent.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    @admin.action(description="Очистить задолженность")  # Улучшено описание действия
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Очищена задолженность у {updated} объектов")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "model", "supplier", "price", "release_date"]
    list_filter = ["supplier", "release_date"]  # Добавлен фильтр по дате
    search_fields = ["name", "model", "supplier__name"]
    date_hierarchy = "release_date"  # Добавлена иерархия по дате


@admin.register(ProductAvailability)
class ProductAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["product", "network_node", "quantity"]
    list_filter = ["network_node", "product"]
    search_fields = ["product__name", "network_node__name"]
    autocomplete_fields = ["product", "network_node"]  # Добавлено автозаполнение
