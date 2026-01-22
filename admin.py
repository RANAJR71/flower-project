from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Flower, Order

# ---------------- Flower Admin ----------------
@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'photo_preview')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('id',)
    actions_selection_counter = True
    actions = ['delete_selected']

    def photo_preview(self, obj):
        if obj.image:
            # URLs for edit and delete
            edit_url = reverse('admin:shop_flower_change', args=[obj.id])
            delete_url = reverse('admin:shop_flower_delete', args=[obj.id])
            return format_html(
                '''
                <div style="text-align:center;">
                    <img src="{}" width="60" style="border-radius:5px;" title="Thumbnail"/>
                    <div style="margin-top:5px;">
                        <a href="{}">✏️ Edit</a> | <a href="{}">🗑 Delete</a>
                    </div>
                </div>
                ''',
                obj.image.url, edit_url, delete_url
            )
        return "(No Image)"
    photo_preview.short_description = 'Photo'

    def has_delete_permission(self, request, obj=None):
        return True


# ---------------- Order Admin ----------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'flower', 'quantity', 'order_type', 'address', 'total_price')
    list_display_links = ('customer_name', 'flower')
    search_fields = ('customer_name', 'flower__name', 'order_type')
    list_filter = ('order_type',)
    ordering = ('-id',)
    actions_selection_counter = True
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True
