from django.forms import ModelForm
from books.models import *

class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder']= 'Enter '+ field.label
