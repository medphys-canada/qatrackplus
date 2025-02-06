from django.urls import include, path
from rest_framework import routers

from qatrack.api.qa import views

router = routers.DefaultRouter()

router.register(r'frequencies', views.FrequencyViewSet)
router.register(r'testinstancestatus', views.TestInstanceStatusViewSet)
router.register(r'autoreviewrules', views.AutoReviewRuleViewSet)
router.register(r'autoreviewrulesets', views.AutoReviewRuleSetViewSet)
router.register(r'references', views.ReferenceViewSet)
router.register(r'tolerances', views.ToleranceViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tests', views.TestViewSet)
router.register(r'unittestinfos', views.UnitTestInfoViewSet)
router.register(r'testlists', views.TestListViewSet)
router.register(r'testlistmemberships', views.TestListMembershipViewSet)
router.register(r'sublists', views.SublistViewSet)
router.register(r'unittestcollections', views.UnitTestCollectionViewSet)
router.register(r'testinstances', views.TestInstanceViewSet)
router.register(r'testlistinstances', views.TestListInstanceViewSet)
router.register(r'testlistcycles', views.TestListCycleViewSet)
router.register(r'testlistcyclememberships', views.TestListCycleMembershipViewSet)

urlpatterns = [
    # view for composite calculations via api
    path("composite/", views.CompositeCalculation.as_view(), name="api.composite"),

    # view for uploads via api
    path("upload/", views.Upload.as_view(), name="api.upload"),

    # search urls
    path("searcher/test/", views.test_searcher, name='test_searcher'),
    path("searcher/test_list/", views.test_list_searcher, name='test_list_searcher'),
    path("searcher/test_list_cycle/", views.test_list_cycle_searcher, name='test_list_cycle_searcher'),
    path("searcher/test_instance/", views.test_instance_searcher, name='test_instance_searcher'),
    path("searcher/test_list_instance/", views.test_list_instance_searcher, name='test_list_instance_searcher'),
    path('', include(router.urls)),
]
