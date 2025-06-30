from django.core.validators import MinValueValidator
import uuid
from django.db import models
from django.contrib.auth.models import User
class Catagoriesofitems(models.Model):
    Catagory_name=models.CharField(max_length=500)
    class Meta:
        db_table='Catagories_on_this_web'
    def __str__(self):
        return self.Catagory_name

class SubCatagoriesofitems(models.Model):
    category = models.ForeignKey(Catagoriesofitems, on_delete=models.SET_NULL, null=True, blank=True,related_name='SubCatagoriesofitems')
    subCatagory_name=models.CharField(max_length=500)
    class Meta:
        db_table='subCatagories_on_this_web'
    def __str__(self):
        return self.subCatagory_name



class DynamicModel(models.Model):
    pagetitle=models.CharField(max_length=500)
    class Meta:
        db_table='DynamicPages'
    def __str__(self):
        return self.pagetitle

class CardDetails(models.Model):
    AVAILABLITY_CHOICES=[
        ('yes','Yes'),
        ('no','No'),
        ('limited','Limited'),
    ]
    WEIGHT_UNITS = [
        ('kg', 'Kilogram (kg)'),
        ('g', 'Gram (g)'),
        ('qt', 'Quintal (qt)'),
        ('ton', 'Metric Ton (ton)'),
        ('lbs', 'Pounds (lbs)'),
        ('none', 'None'),
        ('oz', 'Ounce (oz)'),
    ]
    
    VOLUME_UNITS = [
        ('l', 'Liter (L)'),
        ('ml', 'Milliliter (ml)'),
        ('gal', 'Gallon (gal)'),
        ('pt', 'Pint (pt)'),
        ('fl_oz', 'Fluid Ounce (fl oz)'),
    ]
    
    AREA_UNITS = [
        ('m2', 'Square Meter (m²)'),
        ('ha', 'Hectare (ha)'),
        ('ac', 'Acre (ac)'),
        ('km2', 'Square Kilometer (km²)'),
    ]
    
    
    image=models.ImageField(upload_to="product")
    image1=models.ImageField(upload_to="product", blank=True, null=True)
    image2=models.ImageField(upload_to="product", blank=True, null=True)
    image3=models.ImageField(upload_to="product", blank=True, null=True)
    cardtitle=models.CharField(max_length=500)
    Description = models.TextField()
    Description_of_product=models.TextField()
    unit_of_measurement = models.CharField(
        max_length=20, 
        choices=WEIGHT_UNITS + VOLUME_UNITS + AREA_UNITS,
        default='kg',
    )
    rating = models.PositiveSmallIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,validators=[MinValueValidator(0.01)])
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    availablity = models.CharField(max_length=10, choices=AVAILABLITY_CHOICES, default='yes')
    
    category = models.ForeignKey(Catagoriesofitems, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCatagoriesofitems, on_delete=models.SET_NULL, null=True, blank=True)
    max_product = models.PositiveIntegerField(default=0)
    delivery_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='Cards'
    def save(self, *args, **kwargs):
    # Set availablity based on max_product
        if self.max_product == 0:
            self.availablity = 'no'
        elif self.max_product <= 20:
            self.availablity = 'limited'
        else:
            self.availablity = 'yes'

        # Calculate and set the final_price
        try:
            discount_amount = (self.price * self.discount) / 100
            discounted = self.price - discount_amount
            self.final_price = round(discounted + self.delivery_charges, 2)
        except:
            self.final_price = self.price

        super().save(*args, **kwargs)
    
    @property
    def discounted_price(self):
        try:
            discount_amount = (self.price * self.discount) / 100
            discounted = self.price - discount_amount
            return round(discounted + self.delivery_charges, 2)
        except:
            return self.price

    def __str__(self):
        return self.cardtitle

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    companyBrandName=models.CharField(max_length=500,blank=True,null=True)
    Address=models.CharField(max_length=500,blank=True,null=True)
    City=models.CharField(max_length=500,blank=True,null=True)
    State=models.CharField(max_length=500,blank=True,null=True)
    Zip = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table="UserProfiles"
    def __str__(self):
        return str(self.phone)
    
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    brand = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    
    CATEGORY_CHOICES = [
        ('manufacturer', 'Manufacturer'),
        ('distributer', 'Distributer'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    additional_info = models.TextField(blank=True)
    class Meta:
        db_table = 'SellerProfile'

    def __str__(self):
        return f"{self.name} - {self.brand}"




class ProductsOfthisWeb(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    AVAILABLITY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('limited', 'Limited'),
    ]
    WEIGHT_UNITS = [
        ('kg', 'Kilogram (kg)'),
        ('g', 'Gram (g)'),
        ('qt', 'Quintal (qt)'),
        ('ton', 'Metric Ton (ton)'),
        ('lbs', 'Pounds (lbs)'),
        ('oz', 'Ounce (oz)'),
        ('none', 'None'),
    ]
    
    VOLUME_UNITS = [
        ('l', 'Liter (L)'),
        ('ml', 'Milliliter (ml)'),
        ('gal', 'Gallon (gal)'),
        ('pt', 'Pint (pt)'),
        ('fl_oz', 'Fluid Ounce (fl oz)'),
    ]
    
    AREA_UNITS = [
        ('m2', 'Square Meter (m²)'),
        ('ha', 'Hectare (ha)'),
        ('ac', 'Acre (ac)'),
        ('km2', 'Square Kilometer (km²)'),
    ]
    
    image = models.ImageField(upload_to="product")
    image1 = models.ImageField(upload_to="product", blank=True, null=True)
    image2 = models.ImageField(upload_to="product", blank=True, null=True)
    image3 = models.ImageField(upload_to="product", blank=True, null=True)
    product_name = models.CharField(max_length=500)
    Description = models.TextField()
    Description_of_product = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reviews = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit_of_measurement = models.CharField(
        max_length=20, 
        choices=WEIGHT_UNITS + VOLUME_UNITS + AREA_UNITS,
        default='kg',
    )
    discount = models.CharField(max_length=500)
    availablity = models.CharField(max_length=10, choices=AVAILABLITY_CHOICES, default='yes')
    category = models.ForeignKey(Catagoriesofitems, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCatagoriesofitems, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rating = models.FloatField(default=0.0)
    max_product = models.PositiveIntegerField(default=0)
    
    # Foreign key to the User model to track who added the product
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'products'

    def save(self, *args, **kwargs):
        if self.max_product == 0:
            self.availablity = 'no'
        elif self.max_product <= 20:
            self.availablity = 'limited'
        else:
            self.availablity = 'yes'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


# mantainance tables and models should be maintained by admin

class Slidermaintain(models.Model):
    image1=models.ImageField(upload_to="SliderImage")
    idetity_urls=models.CharField(max_length=500)
    
    class Meta:
        db_table='sliders'
    def __str__(self):
        return str(self.image1.name)
    
class Recomendations(models.Model):
    
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='Recommendations_by_Admin'
    def __str__(self):
        return str(self.productname)
    
class OffersSection(models.Model):
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='offers_by_Admin'
    def __str__(self):
        return str(self.productname)
    
class GrowthSection(models.Model):
    
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='Growth_by_Admin'
    def __str__(self):
        return str(self.productname)
    
class SmartfarmingSection(models.Model):
    
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='smartfarming_by_Admin'
    def __str__(self):
        return str(self.productname)
    
class SpraySection(models.Model):
    
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='Spray_by_Admin'
    def __str__(self):
        return str(self.productname)
    
class SeedsSection(models.Model):
    
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='Seeds_by_Admin'
    def __str__(self):
        return str(self.productname)
    
    
class SeasonalSection(models.Model):
    
    productname=models.ForeignKey(CardDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table='Seasonal_by_Admin'
    def __str__(self):
        return str(self.productname)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CardDetails, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Cascade delete on Order deletion
    product = models.ForeignKey(CardDetails, on_delete=models.CASCADE)  # Cascade delete on CardDetails deletion
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'orderItem'
    
    def __str__(self):
        return f"{self.quantity} of {self.product.cardtitle}"


class orderplacedfinal(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user_username = models.CharField(max_length=255)
    user_other_details = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        db_table = 'order_placed_final'

    def __str__(self):
        return self.user_username if self.user_username else "No user"

