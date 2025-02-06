from django.urls import include, path
from rest_framework import routers

from qatrack.api.service_log import views

router = routers.DefaultRouter()
router.register(r'serviceareas', views.ServiceAreaViewSet)
router.register(r'unitserviceareas', views.UnitServiceAreaViewSet)
router.register(r'servicetypes', views.ServiceTypeViewSet)
router.register(r'serviceeventstatus', views.ServiceEventStatusViewSet)
router.register(r'serviceevents', views.ServiceEventViewSet)
router.register(r"serviceeventschedule", views.ServiceEventScheduleViewSet)
router.register(r"serviceeventtemplate", views.ServiceEventTemplateViewSet)
router.register(r'thirdparty', views.ThirdPartyViewSet)
router.register(r'hours', views.HoursViewSet)
router.register(r'returntoserviceqa', views.ReturnToServiceQAViewSet)
router.register(r'grouplinker', views.GroupLinkerViewSet)
router.register(r'grouplinkerinstance', views.GroupLinkerInstanceViewSet)

urlpatterns = [
    path("searcher/service_event/", views.service_event_searcher, name='service_event_searcher'),
    path('', include(router.urls)),
]
