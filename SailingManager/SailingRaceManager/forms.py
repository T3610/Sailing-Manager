from django import forms
from crispy_forms.helper import FormHelper

from .models import Boat, Racer, Race

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
        fields = ('RaceNumber', 'StartTime', 'RaceLength', 'RaceType',)


