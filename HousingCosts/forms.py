from django.forms import ModelForm
from .models import House
from django import forms


class HouseForm(ModelForm):
    class Meta:
        model = House
        # This indicates that we want all model fields in the form:
        fields = '__all__'


# Form for API search parameters:
class ApiSearchForm(forms.Form):
    city = forms.CharField(max_length=25)
    state = forms.CharField(max_length=2)
    beds = forms.IntegerField()
    baths = forms.IntegerField()
    price = forms.IntegerField()
