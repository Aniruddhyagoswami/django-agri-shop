from django.contrib import admin, messages
from django.apps import apps
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .models import *

# --------- Custom ProductAdmin with Summernote ----------
class ProductAdmin(SummernoteModelAdmin):
    list_display = ['product_name', 'price']
    summernote_fields = ('Description_of_product', 'Description')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            self.message_user(
                request,
                "✅ New product submitted!",
                level=messages.SUCCESS
            )
            self.message_user(
                request,
                mark_safe(f"""
                    <div style='border:1px solid #ccc; padding:10px; border-radius:8px; background:#f0f0f5; margin-top:10px;'>
                        <h4><strong>{obj.product_name}</strong></h4>
                        <p>💰 Price: ₹{obj.price}</p>
                        <a href='/admin/portal/productsofthisweb/{obj.id}/' style='color:#007bff;'>View Product</a>
                    </div>
                """),
                level=messages.INFO,
                extra_tags='safe'
            )

# --------- Custom CardDetailsAdmin ----------
class CardDetailsAdmin(SummernoteModelAdmin):
    list_display = ['cardtitle', 'price']
    summernote_fields = ('Description_of_product', 'Description')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            self.message_user(
                request,
                "✅ New card details submitted!",
                level=messages.SUCCESS
            )
            self.message_user(
                request,
                mark_safe(f"""
                    <div style='border:1px solid #ccc; padding:10px; border-radius:8px; background:#f9f9f9; margin-top:10px;'>
                        <h4><strong>{obj.cardtitle}</strong></h4>
                        <p>💰 Price: ₹{obj.price}</p>
                        <a href='/admin/portal/carddetails/{obj.id}/' style='color:#007bff;'>View Card</a>
                    </div>
                """),
                level=messages.INFO,
                extra_tags='safe'
            )

# --------- Reusable Actions ----------
def delete_records_of_date(modeladmin, request, queryset):
    specific_date = request.POST.get('specific_date')
    if specific_date:
        queryset.filter(created_at__date=specific_date).delete()
        modeladmin.message_user(request, f"Records from {specific_date} have been deleted.")
    else:
        modeladmin.message_user(request, "No date provided.", level='error')

def delete_all_data(modeladmin, request, queryset):
    queryset.delete()
    modeladmin.message_user(request, "All selected records have been deleted.")

# --------- Manual Registration for Custom Admins ----------
if not admin.site.is_registered(ProductsOfthisWeb):
    admin.site.register(ProductsOfthisWeb, ProductAdmin)

if not admin.site.is_registered(CardDetails):
    admin.site.register(CardDetails, CardDetailsAdmin)

# --------- Auto Register Remaining Models ----------
app = apps.get_app_config('portal')

for model in app.get_models():
    if admin.site.is_registered(model) or model in [ProductsOfthisWeb, CardDetails]:
        continue

    if hasattr(model, 'Description_of_product') or hasattr(model, 'Description'):
        class CustomAdmin(SummernoteModelAdmin):
            summernote_fields = ('Description_of_product', 'Description')
            actions = [delete_records_of_date, delete_all_data]
        admin.site.register(model, CustomAdmin)
    else:
        class DefaultAdmin(admin.ModelAdmin):
            actions = [delete_records_of_date, delete_all_data]
        admin.site.register(model, DefaultAdmin)
