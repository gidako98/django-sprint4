from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from blog.models import Post


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.published().filter(author=user)
    is_owner = request.user == user
    return render(request, 'users/profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_owner': is_owner,
    })


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'users/edit_profile.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != kwargs['username']:
            return redirect('users:profile', username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)
