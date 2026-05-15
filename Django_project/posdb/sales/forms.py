# sales/forms.py

from django import forms
from .models import OrderItem


class OrderItemForm(forms.ModelForm):
    """One line item to add to an order."""
    class Meta:
        model  = OrderItem
        fields = ['product', 'quantity']

    def clean_quantity(self):
        """Validation: quantity must be at least 1."""
        qty = self.cleaned_data['quantity']
        if qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return qty
    def clean_product(self):
        """Validation: ពិនិត្យមើលថាតើទំនិញមានក្នុងស្តុកឬអត់ (ភារកិច្ច ២)"""
        product = self.cleaned_data.get('product')
        
        # ប្រសិនបើរកឃើញផលិតផល ហើយស្តុកស្មើនឹង ០ ត្រូវបង្ហាញ Error
        if product and product.stock == 0:
            raise forms.ValidationError("ទំនិញនេះអស់ពីស្តុកហើយ (Out of stock)!")
            
        return product