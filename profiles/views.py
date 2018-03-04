from django.views import generic
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect
from braces.views import LoginRequiredMixin
from notifications.signals import notify
from django.contrib.auth.models import User

from . import forms
from . import models
from projects.models import Position


class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    model = models.Profile
    template_name = 'profiles/profile.html'

    def get(self, request, **kwargs):
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_pk)
        profile = get_object_or_404(models.Profile, user=user)
        kwargs['profile'] = profile
        kwargs['skills'] = models.ProfileSkill.objects.filter(profile=profile)
        return super().get(request, **kwargs)


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    form_class = forms.UserProfileForm
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['formset'] = forms.SkillInlineFormSet(
            queryset=models.ProfileSkill.objects.filter(profile=profile))
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = forms.UserProfileForm(self.request.POST, request.FILES,
                                     instance=profile)
        formset = forms.SkillInlineFormSet(
            self.request.POST,
            queryset=models.ProfileSkill.objects.filter(profile=profile))

        if form.is_valid():
            profile = form.save()
            if formset.is_valid():
                skills = formset.save(commit=False)
                for skill in skills:
                    skill.profile = profile
                    skill.save()

        return HttpResponseRedirect(reverse('profiles:show_profile',
                                    kwargs={'pk': profile.user.id}))


STATUS_CHOICES = {
    'undecided': None,
    'accepted': True,
    'rejected': False
}


class Applications(LoginRequiredMixin, generic.ListView):
    model = models.Application
    context_object_name = 'application_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        status_term = self.request.GET.get('status')

        if status_term in STATUS_CHOICES.keys():
            queryset = queryset.filter(is_accepted=STATUS_CHOICES[status_term])

        return queryset.filter(project__creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status') or 'all'
        return context


class ApplicationStatus(LoginRequiredMixin, generic.TemplateView):

    def get(self, request, *args, **kwargs):
        position = get_object_or_404(Position, pk=self.kwargs.get('position'))
        applicant = get_object_or_404(User, pk=self.kwargs.get('applicant'))
        status = self.kwargs.get('status')
        accept = True if status == 'approve' else False
        application = models.Application.objects.filter(
            position=position, applicant=applicant).update(is_accepted=accept)

        notify.send(applicant,
                    recipient=applicant,
                    verb='Your application for {} as {} was {}'.format(
                        position.project.title, position.name, status))
        return HttpResponseRedirect(reverse('profiles:my_applications'))


class Notifications(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profiles/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unreads'] = self.request.user.notifications.unread()
        return context
