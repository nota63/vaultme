from django import forms
from .models import Address, Item, Cancel, Help, RequestItem, Account, SellProducts


# create address form

class AddressForm(forms.ModelForm):
    class Meta():
        model = Address
        fields = ['full_name', 'email', 'contact', 'quantity', 'address', 'state', 'country']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 50})
        }


# create cancel form

class CancelForm(forms.ModelForm):
    class Meta():
        model = Cancel
        fields = ['why_cancel', 'suggestion']
        widgets = {

            'suggestion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40})}


# form for help requests

class HelpForm(forms.ModelForm):
    class Meta():
        model = Help
        fields = ['type', 'message', 'attach_image', 'email', 'contact']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 40})
        }


# form for request an item

class RequestItemForm(forms.ModelForm):
    class Meta():
        model = RequestItem
        fields = ['item_name', 'description', 'image', 'contact']


# create accountform

class AccountForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ['profile_pic', 'bank_account', 'bank_name', 'ifsc_code', 'email', 'city', 'pin_code']


# sell products form
class SellProductsForm(forms.ModelForm):
    class Meta():
        model = SellProducts
        fields = ['product_name', 'description', 'product_pdf', 'price']
