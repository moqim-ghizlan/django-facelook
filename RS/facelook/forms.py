from django import forms
from .models import Post, Topic, Like
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
User = get_user_model()


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        labels = {
            'first_name': _('Prénom'),
            'last_name': _('Nom'),
            }
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'title',
                    'id' : 'title',
                    'required' : True,
                    'label' : 'Titre'
                    }),
            'text':  forms.TextInput(
                attrs={
                    'class': 'text',
                    'id' : 'text',
                    'required' : True,
                    'row' : 5,
                    'label' : 'Description'
                    })
                }
        labels = {
            'title': _('Titre'),
            'text': _('Description'),
            }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('topic', 'text')
        widgets = {

           # forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))


            'text':  forms.Textarea(
                attrs={
                    'class': 'text',
                    'id' : 'text',
                    'required' : True,
                    'row' : 5,
                    'label' : 'Corps du post'
                    }),
            'topic': forms.Select(
                attrs={
                    'class': 'topic',
                    'id' : 'topic',
                    'required' : True,
                    'label' : 'Sujet'

                    })
                }
        labels = {
            'topic': _('Sujet'),
            'text': _('Corps du post'),
            }
