from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^project/(?P<pk>\d+)/apply/(?P<position>\d+)/$',
        views.PositionApplyView.as_view(), name='position_apply'),
    url(r'^project/(?P<pk>\d+)/delete/$', views.ProjectDeleteView.as_view(),
        name='project_delete'),
    url(r'^project/(?P<pk>\d+)/edit/$', views.ProjectEditView.as_view(),
        name='project_edit'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(),
        name='project_detail'),
    url(r'^project/add/$', views.ProjectCreateView.as_view(),
        name='add_project'),
    url(r'^$', views.ProjectListView.as_view(), name='project_list'),
]
