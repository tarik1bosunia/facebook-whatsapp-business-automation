from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Order
from django.utils.translation import gettext_lazy as _
from messaging.models import SocialMediaUser

class SocialMediaUserInline(admin.TabularInline):
    model = SocialMediaUser
    extra = 0
    readonly_fields = ['avatar_preview']
    fields = ['platform', 'social_media_id', 'avatar_url', 'avatar_preview']

    def avatar_preview(self, obj):
        if obj.avatar_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar_url)
        return "-"

    avatar_preview.short_description = _('Avatar Preview')


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ['order_number', 'total', 'status', 'payment_status', 'created_at']
    fields = ['order_number', 'total', 'status', 'payment_status', 'created_at']
    ordering = ['-created_at']
    show_change_link = True


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'phone',
        'orders_count',
        'total_spent',
        'status',
        'channel_display',
        'avatar_display',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'social_media_users__social_media_id']
    readonly_fields = ['orders_count', 'total_spent', 'created_at', 'updated_at', 'avatar_display']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'email', 'phone', 'status')
        }),
        (_('Stats'), {
            'fields': ('orders_count', 'total_spent')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at')
        }),
        (_('Avatar Preview'), {
            'fields': ('avatar_display',)
        }),
    )
    inlines = [SocialMediaUserInline, OrderInline]
    actions = ['activate_customers', 'deactivate_customers']
    date_hierarchy = 'created_at'
    list_per_page = 20

    def channel_display(self, obj):
        platforms = set(smu.platform for smu in obj.social_media_users.all())
        if len(platforms) > 1:
            return 'both'
        return platforms.pop() if platforms else '-'

    channel_display.short_description = _('Channel')

    def avatar_display(self, obj):
        social_avatar = obj.social_media_users.filter(avatar_url__isnull=False).first()
        avatar_url = social_avatar.avatar_url if social_avatar else f"https://i.pravatar.cc/150?u={obj.id}"
        return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', avatar_url)

    avatar_display.short_description = _('Avatar')

    def activate_customers(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f"{updated} customers were activated.")

    activate_customers.short_description = _("Activate selected customers")

    def deactivate_customers(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f"{updated} customers were deactivated.")

    deactivate_customers.short_description = _("Deactivate selected customers")


class OrderStatusFilter(admin.SimpleListFilter):
    title = _('Order Status')
    parameter_name = 'order_status'

    def lookups(self, request, model_admin):
        return Order.Status.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return None


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number',
        'customer_link',
        'total',
        'status',
        'payment_status',
        'created_at',
        'updated_at'
    ]
    list_filter = [OrderStatusFilter, 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer__name', 'customer__email']
    readonly_fields = ['created_at', 'updated_at', 'customer_link']
    fieldsets = (
        (_('Order Information'), {
            'fields': ('order_number', 'customer_link', 'items', 'total')
        }),
        (_('Status'), {
            'fields': ('status', 'payment_status')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    list_select_related = ['customer']
    date_hierarchy = 'created_at'
    list_per_page = 20

    def customer_link(self, obj):
        url = f"/admin/customer/customer/{obj.customer.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.customer.name)

    customer_link.short_description = _('Customer')
