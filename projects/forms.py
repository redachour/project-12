from django import forms

from profiles.models import Skill
from . import models


class PositionCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Position Title'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Position description'}))
    length = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'length of involvement'}))
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Skill.objects.all())

    class Meta:
        model = models.Position
        fields = ('name', 'description', 'skills', 'length')


PositionInlineFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionCreateForm,
    fields=('name', 'description', 'skills', 'length'),
    extra=0,
    min_num=1,
)
