from django.forms import ModelForm
from .models import Member

class MemberCreationForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder']= 'Enter '+ field.label