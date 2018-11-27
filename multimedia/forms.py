from django import forms
from bootcamp.multimedia.models import Multimedia, CategorieMedia



class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['title', 'multimedia_link']

class CategorieMediaForm(forms.ModelForm):
	class Meta:
		model = CategorieMedia
		fields = ['title', 'description']