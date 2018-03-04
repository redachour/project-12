from django import forms

from . import models


class UserProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=models.Skill.objects.all())

    class Meta:
        model = models.Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar', 'skills')


SkillInlineFormSet = forms.modelformset_factory(
    models.ProfileSkill,
    fields=('name',),
    extra=0,
    min_num=1,
)
