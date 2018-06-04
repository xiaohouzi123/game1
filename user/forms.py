from django import forms

from user.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'icon', 'sex', 'age']

    password2 = forms.CharField(max_length=128)

    def clean_password(self):
        cleaned_data = super().clean()

        if len(cleaned_data['password']) < 8:
            raise forms.ValidationError('密码长度过短')
        elif cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('两次密码不一致')
