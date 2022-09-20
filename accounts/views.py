from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import CustomUser, Profile
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    # pk = None

    # def get_success_url(self):
    #     return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})

    # def form_valid(self, form):
    #     profile = Profile.objects.create(user=get_user_model())
    #     return super(SignUpView, self).form_valid(form)


class UserView(LoginRequiredMixin, generic.DetailView):
    """Profile"""

    model = User
    context_object_name = "user"
    template_name = "registration/user.html"

    # def get_queryset(self):
    #     profile = Profile.objects.get(user=self.request.user)
    #     # profile = Profile.objects.get(user=self.request.user)
    #     return profile

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # user = CustomUser.objects.filter(pk=self.request.user.pk)
    #     try:
    #         profile = Profile.objects.get(user=self.request.user)
    #         # context["myuser"] = user

    #     except:
    #         profile = Profile.objects.create(user=self.request.user)
    #         # context["profile"] = profile
    #     context["profile"] = profile
    #     return context


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    """UpdateView"""

    model = User
    form_class = UserUpdateForm
    context_object_name = "form"
    template_name = "registration/user_form.html"
    pk = None
    # success_url = reverse_lazy('accounts:user')

    def get_success_url(self):
        return reverse("accounts:user", kwargs={"pk": self.request.user.pk})

    # def form_valid(self, form):
    #     """FormValid"""
    #     profile = User.objects.update(
    #         # user=self.request.user,
    #         first_name=form.cleaned_data["first_name"],
    #         last_name=form.cleaned_data["last_name"],
    #         id_number=form.cleaned_data["id_number"],
    #         contact=form.cleaned_data["contact"],
    #         address=form.cleaned_data["address"],
    #     )
    #     return super(ProfileUpdateView, self).form_valid(form)


def my_profile(request):
    return render(request, "payments/my_profile.html")
