from django import forms
from portal.models import ProductsOfthisWeb


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user
        super(ProductForm, self).__init__(*args, **kwargs)

        # Optional image fields
        self.fields['image1'].required = False
        self.fields['image2'].required = False
        self.fields['image3'].required = False

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:
            product.added_by = self.user  # Set the user correctly
        if commit:
            product.save()
        return product

    class Meta:
        model = ProductsOfthisWeb
        fields = [
            'product_name', 'Description', 'Description_of_product', 'price', 'reviews',
            'unit_of_measurement', 'discount', 'availablity', 'category', 'subcategory',
            'image', 'image1', 'image2', 'image3', 'max_product'
        ]
