from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductsOfthisWeb, CardDetails

@receiver(post_save, sender=ProductsOfthisWeb)
def create_card_on_accept(sender, instance, created, **kwargs):
    if instance.status == 'accepted':
        if not CardDetails.objects.filter(cardtitle=instance.product_name).exists():
            try:
                price = instance.price
                discount = float(instance.discount)
                delivery_charges = 0.0  # or custom logic if needed

                discount_amount = (price * discount) / 100
                discounted = price - discount_amount
                final_price = round(discounted + delivery_charges, 2)
            except:
                final_price = instance.price
                delivery_charges = 0.0

            CardDetails.objects.create(
                image=instance.image,
                image1=instance.image1,
                image2=instance.image2,
                image3=instance.image3,
                cardtitle=instance.product_name,
                Description=instance.Description,
                Description_of_product=instance.Description_of_product,
                unit_of_measurement=instance.unit_of_measurement,
                rating=int(instance.reviews),
                price=price,
                discount=discount,
                availablity=instance.availablity,
                category=instance.category,
                subcategory=instance.subcategory,
                max_product=instance.max_product,
                delivery_charges=delivery_charges,
                final_price=final_price,
                added_by=instance.added_by
            )
    elif instance.status == 'rejected':
        instance.delete()
