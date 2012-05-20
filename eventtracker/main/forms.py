from django import forms

from django.forms.formsets import formset_factory

class ObjectForm(forms.Form):
	url = forms.CharField(label='Adres serwisu')
	pole1 = forms.CharField(label='Pole1')
	pole2 = forms.CharField(label='Pole2', required=False)
	pole3 = forms.CharField(label='Pole3', required=False)
	pole4 = forms.CharField(label='Pole4', required=False)
	pole5 = forms.CharField(label='Pole5', required=False)
	pole6 = forms.CharField(label='Pole6', required=False)

class TeachForm(forms.Form):
	url = forms.CharField(label='Adres serwisu')
	limit = forms.CharField(label='Limit')

class UrlForm(forms.Form):
	url = forms.CharField(label='Adres serwisu')

class PathsForm(forms.Form):
	path1 = forms.CharField(label='Sciezka do pola 1', required=False)
	path2 = forms.CharField(label='Sciezka do pola 2', required=False)
	path3 = forms.CharField(label='Sciezka do pola 3', required=False)
	path4 = forms.CharField(label='Sciezka do pola 4', required=False)
	path5 = forms.CharField(label='Sciezka do pola 5', required=False)
	path6 = forms.CharField(label='Sciezka do pola 6', required=False)

class ResultForm(forms.Form):
	pole1 = forms.CharField(label='Pole1')
	pole2 = forms.CharField(label='Pole2', required=False)
	pole3 = forms.CharField(label='Pole3', required=False)
	pole4 = forms.CharField(label='Pole4', required=False)
	pole5 = forms.CharField(label='Pole5', required=False)
	pole6 = forms.CharField(label='Pole6', required=False)

ResultFormset = formset_factory(ResultForm, extra=0)
