class FollowForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['follows']
