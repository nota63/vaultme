from django.contrib import admin
from .models import Category, Item, Address, Cancel, Help, RequestItem, Account, SellProducts,Notice


class HelpAdmin(admin.ModelAdmin):
    list_filter = ('user', 'item',)
    list_display = ('item',)
    search_fields = ('item',)


class AddressAdmin(admin.ModelAdmin):
    list_filter = ('item', 'placed_on')
    list_display = ('item',)
    search_fields = ('item', 'placed_on',)


class RequestAdmin(admin.ModelAdmin):
    list_filter = ('user', 'item_name',)
    list_display = ('user', 'item_name',)
    search_fields = ('item_name',)


class AccountAdmin(admin.ModelAdmin):
    list_filter = ('user', 'city',)
    list_display = ('user', 'city',)
    search_fields = ('user', 'city',)


class SellProductsAdmin(admin.ModelAdmin):
    list_filter = ('user', 'product_name',)
    list_display = ('user', 'product_name',)
    search_fields = ('user', 'product_name',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Address, AddressAdmin)
admin.site.register(Cancel)
admin.site.register(Help, HelpAdmin)
admin.site.register(RequestItem, RequestAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(SellProducts, SellProductsAdmin)
admin.site.register(Notice)
