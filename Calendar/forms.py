from datetime import datetime
from django import forms
from .models import *


class AddCalendarForms(forms.ModelForm):
    """Форма для создания события календаря"""
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя ученика или выберите из выпадающего списка','list':'datalistOptions'}))
    start = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))
    repeat = forms.BooleanField()
    price = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Цена за занятие'}))
    telegrambool = forms.BooleanField()
    
    class Meta:
        model = Calendar
        fields = ('title','start','end','repeat','price','telegrambool')
        
    def __init__(self, *args, **kwargs):
        super(AddCalendarForms,self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

class PaidEventForms(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ('paid',)
        widgets = {
            'paid' : forms.CheckboxInput(attrs={'class':"form-check-input",
                                                               'type':'checkbox',
                                                               'role':'switch',
                                                               'id':'flexSwitchCheckDefault',
                                                               'style':'transform: scale(1.5)',
                                                               })

        }

class ManualProceed(forms.Form):
    start = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

