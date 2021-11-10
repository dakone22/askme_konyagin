from django import forms
from django.contrib.auth.models import User

from .models import Profile, Question


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)
    biography = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=False)

    class Meta:
        model = Profile
        fields = ('nickname', 'avatar', 'biography',)


class AskForm(forms.ModelForm):
    # tags = tags_input_fields.TagsInputField(  # TODO: nice tags
    #     Tag.objects.all(),
    #     # create_missing=True,
    #     required=True,
    # )

    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')
