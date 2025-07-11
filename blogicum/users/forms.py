from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from blog.models import Comment, Post

User = get_user_model()


class CreatePostForm(forms.ModelForm):
    """Форма "Публикация"."""

    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MyCreationForm(UserCreationForm):
    """Форма "Юзер для регистрации на сайте"."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].help_text = 'Необязательное поле'
        self.fields['last_name'].help_text = 'Необязательное поле'


class MyChangeForm(UserChangeForm):
    """Форма "Юзер" для редактирования профиля на сайте."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].help_text = 'Необязательное поле'
        self.fields['last_name'].help_text = 'Необязательное поле'


class CommentForm(forms.ModelForm):
    """Форма "Комментарий"."""

    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].help_text = 'Оставьте комментарий'
