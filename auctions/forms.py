from django import forms
from .models import Listing, User

class ListingForm(forms.Form):

    title = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class':'form-field title-field', 'placeholder':'Title'}))

    description = forms.CharField(
        max_length=1024, 
        widget=forms.TextInput(attrs={'class':'form-field dis-field', 'placeholder':'Description'}))

    starting_bid = forms.IntegerField(
        min_value=1, 
        widget=forms.NumberInput(attrs={'class':'form-field bid-field', 'placeholder':'Starting Bid'}))

    Image = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class':'form-field url-field', 'placeholder':'URL'}))

    category = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class':'form-field category-field', 'placeholder':'Category'}))


