from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from notifications.signals import notify
from braces.views import LoginRequiredMixin

from . import forms
from . import models
from profiles.models import Application


class ProjectListView(generic.ListView):
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        array = []
        positions = models.Position.objects.exclude(
            applications__is_accepted=True)
        for position in positions:
            if position.name not in array:
                array.append(position.name)
        context['position_names'] = array
        context['filter'] = self.request.GET.get('filter')
        context['skill'] = self.request.GET.get('skill')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        filter_term = self.request.GET.get('filter')
        if filter_term:
            queryset = queryset.filter(Q(positions__name=filter_term))
        skill_term = self.request.GET.get('skill')
        if skill_term:
            my_skills = self.request.user.profile.skills.all()
            queryset = queryset.filter(
                positions__skills__in=my_skills).distinct()

        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = models.Position.objects.filter(
            project=context['project']).exclude(applications__is_accepted=True)
        context['applied_for'] = models.Position.objects.filter(
            project=context['project'],
            applications__applicant=self.request.user)
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    fields = ('title', 'description', 'requirements', 'timeline')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = forms.PositionInlineFormSet(
            queryset=models.Position.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(self.request.POST)
        formset = forms.PositionInlineFormSet(
            self.request.POST,
            queryset=models.Position.objects.none())

        if form.is_valid():
            project = form.save(commit=False)
            project.creator = self.request.user
            project.save()
            if formset.is_valid():
                positions = formset.save(commit=False)
                for position in positions:
                    position.project = project
                    position.save()
                formset.save_m2m()
        return HttpResponseRedirect(reverse('projects:project_list'))


class ProjectEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.Project
    fields = ('title', 'description', 'requirements', 'timeline')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = forms.PositionInlineFormSet(
            queryset=models.Position.objects.filter(project=self.get_object()))
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        form_class = self.get_form_class()
        form = form_class(self.request.POST, instance=project)
        formset = forms.PositionInlineFormSet(
            self.request.POST,
            queryset=models.Position.objects.filter(project=project))

        if form.is_valid():
            project = form.save(commit=False)
            project.creator = self.request.user
            project.save()
            if formset.is_valid():
                models.Position.objects.filter(project=project).delete()
                positions = formset.save(commit=False)
                for position in positions:
                    position.project = project
                    position.save()
                formset.save_m2m()
        return HttpResponseRedirect(reverse('projects:project_detail',
                                    kwargs={"pk": project.id}))


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Project
    success_url = reverse_lazy('projects:project_list')


class PositionApplyView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(models.Project, pk=self.kwargs.get('pk'))
        position = get_object_or_404(models.Position,
                                     pk=self.kwargs.get('position'))
        Application.objects.create(
            applicant=self.request.user,
            project=project,
            position=position)

        notify.send(
            project.creator,
            recipient=project.creator,
            verb='{} submitted an application for {} as {}'.format(
                self.request.user, project.title, position.name),
            description=''
        )
        return HttpResponseRedirect(reverse('projects:project_list'))
