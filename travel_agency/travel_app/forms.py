from django import forms

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email Address")
    destination = forms.CharField(max_length=100, label="Destination")
    travel_date = forms.DateField(label="Travel Date", widget=forms.SelectDateWidget())

