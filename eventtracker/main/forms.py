from django import forms

class FirstForm( forms.Form ):
    url = forms.CharField(label='Adres serwisu')
    pole1 = forms.CharField(label='Pole1')
    pole2 = forms.CharField(label='Pole2', required=False)
    pole3 = forms.CharField(label='Pole3', required=False)
    pole4 = forms.CharField(label='Pole4', required=False)
    pole5 = forms.CharField(label='Pole5', required=False)
    pole6 = forms.CharField(label='Pole6', required=False)
