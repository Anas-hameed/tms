"""main url of tms project"""

from django.urls import include, path

urlpatterns = [
    path(r'user/', include('core.api.user.urls')),
    path(r'trainingplan/', include('core.api.traningplan.urls')),
    path(r'', include('core.api.enrolment.urls')),
    path(r'', include('core.api.module.urls')),
    path(r'', include('core.api.task.urls')),
    path(r'', include('core.api.feedback.urls')),
]
