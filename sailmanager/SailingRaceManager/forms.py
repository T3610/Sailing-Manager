from django import forms
from crispy_forms.helper import FormHelper
from django.forms.widgets import DateInput

from .models import Boat, Racer, Race, Official

class BoatForm(forms.ModelForm):

    class Meta:
        model = Boat
        fields = ('BoatName', 'PyNumber',)

class RacerForm(forms.ModelForm):

    class Meta:
        model = Racer
        fields = ('Boat', 'HelmName', 'CrewName', 'SailNumber',)

    

class RaceForm(forms.ModelForm):

    class Meta:
        model = Race
        fields = ('RaceNumber', 'Date', 'StartTime', 'RaceLength', 'RaceType',)
        widgets = {
            'Date': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class OfficialForm(forms.ModelForm):

    class Meta:
        model = Official
        fields = ('Role', 'Name')


