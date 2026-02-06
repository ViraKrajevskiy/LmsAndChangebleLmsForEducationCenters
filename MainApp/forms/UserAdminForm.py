from django import forms
from MainApp.models.roles.models_roles import User

class UserAdminForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
       
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        