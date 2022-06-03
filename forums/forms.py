from django import forms


class PostCreateForm(forms.Form):
    post_text = forms.CharField()