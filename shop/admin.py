from django.contrib import admin

from shop.models import Section, Product, Discount, Order, OrderLine

admin.site.register(Section)


# admin.site.register(Product)
# admin.site.register(Discount)
# admin.site.register(Order)
# admin.site.register(OrderLine)

class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price'
    round_value = 1000
    def lookups(self, request, model_admin):
        filters = []
        product = Product.objects.order_by('price').last()

        if product:
            max_price = round(product.price / self.round_value) * self.round_value + self.round_value
            price = self.round_value
            while price <= max_price:
                start = price
                start_price = price - self.round_value
                if start_price != 0:
                    start_price += 1
                end = '{0} - {1}'.format(start_price, price)
                filters.append((start, end))
                price += self.round_value
        return filters

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        value = int(self.value())
        return queryset.filter(price__gte=(value - self.round_value + 1), price__lte=value)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'image', 'price', 'date')
    list_filter = ('section', PriceFilter)
    list_per_page = 10
    search_fields = ('title', 'section')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'value_percent')


class OrderLineAdmin(admin.ModelAdmin):
    list_display = 'order', 'product', 'price', 'count'
    list_filter = ('order',)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'display_products', 'display_amount',
        'name', 'discount', 'phone',
        'email', 'address', 'notice',
        'date_order', 'date_send', 'status'
    )
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('need_delivery', 'discount')
        }),
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'email', 'address'),
            'description': 'Контактная информация'
        }),
        ('Доставка и оплата', {
            'fields': ('date_send', 'status')
        }),
    )
    date_hierarchy = 'date_order'
    list_filter = ('status', 'date_order')


admin.site.register(Product, ProductAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Order, OrderAdmin)
