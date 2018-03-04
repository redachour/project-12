from django.conf.urls import url, include


from . import views


urlpatterns = [
    url(r'^applications/(?P<position>\d+)/(?P<applicant>\d+)/(?P<status>\w+)/$',
        views.ApplicationStatus.as_view(), name='status_update'),
    url(r'^applications/$', views.Applications.as_view(),
        name='my_applications'),
    url(r'^edit/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^notifications/$', views.Notifications.as_view(),
        name='my_notifications'),
    url(r'^(?P<pk>\d+)/$', views.ShowProfile.as_view(), name='show_profile'),
]
