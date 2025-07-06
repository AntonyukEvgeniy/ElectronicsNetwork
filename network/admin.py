from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from .models import NetworkNode, Product, ProductAvailability

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "city", "supplier_link", "debt"]
    list_filter = ["type", "city"]
    search_fields = ["name", "email"]
    actions = ["clear_debt"]
    def supplier_link(self, obj):
        if obj.parent:
            url = f"/admin/network/networknode/{obj.parent.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.parent.name)
        return "-"
    supplier_link.short_description = "Поставщик"
    def clear_debt(self, request, queryset):
        queryset.update(debt=0)
    clear_debt.short_description = "Очистить задолженность"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(id__in=request.user.networknode_set.all()) |
            Q(parent__in=request.user.networknode_set.all())
        )
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "model", "supplier", "price"]
    list_filter = ["supplier"]
    search_fields = ["name", "model"]
@admin.register(ProductAvailability)
class ProductAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['product', 'network_node', 'quantity']
    list_filter = ['network_node', 'product']
    search_fields = ['product__name', 'network_node__name']