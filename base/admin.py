from django.contrib import admin
from .models import Product, Review,Cart



class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'name','pid', 'price_new', 'price_old', 'category', 'author')
    search_fields = ['name', 'product_code', 'category','author']
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('discount_percentage', None)
        form.base_fields.pop('reviews', None)
        form.base_fields.pop('pid', None)
        return form
class ReviewAdmin(admin.ModelAdmin):
    list_display = ( 'name','product','email')
    search_fields = ['name','product__name','comment','email']


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cart)
