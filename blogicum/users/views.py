from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MyCreationForm


class MyCreateView(CreateView):
    """CBV регистрации нового пользователя."""

    form_class = MyCreationForm
    success_url = reverse_lazy('blog:index')
    template_name = 'registration/registration_form.html'
