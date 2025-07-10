from django.views.generic.edit import CreateView
from django.urls import path, reverse_lazy

from .forms import RegistrationForm

urlpatterns = [
    path('registration/',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=RegistrationForm,
             success_url=reverse_lazy('blog:index'),
         ),
         name='registration'),
]
