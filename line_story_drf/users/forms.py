from django import forms

from users.models import Profile


class ProfileAdminForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput, max_length=255, required=False)

    class Meta:
        model = Profile
        fields = '__all__'
