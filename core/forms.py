from django import forms
from core.models import User

CreateReviewGroups = [
    ('Movies', 'Movies'),
    ('Games', 'Games'),
    ('Books', 'Books'),
    ('Music', 'Music'),
    ('Art', 'Art')
]


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput
    )
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class CreateReviewForm(forms.Form):
    title = forms.CharField()
    group = forms.CharField(
        widget=forms.Select(choices=CreateReviewGroups)
    )
    text = forms.CharField(
        widget=forms.Textarea
    )
    rating = forms.CharField(
        widget=forms.Select(choices=list(zip(range(1, 11), range(1, 11))))
    )
    tags = forms.CharField()
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
            'accept': 'image/*'
        })
    )

