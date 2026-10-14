from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet
from apps.memories.views import MemoryListCreateView, MemoryDetailView
from apps.interactions.views import InteractionListCreateView, InteractionDetailView
from apps.schedules.views import ScheduleListCreateView, ScheduleDetailView

app_name = 'contacts'

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
    path('contacts/<int:contact_id>/memories/', MemoryListCreateView.as_view(), name='contact-memories-list'),
    path('contacts/<int:contact_id>/memories/<int:pk>/', MemoryDetailView.as_view(), name='contact-memories-detail'),
    path('contacts/<int:contact_id>/interactions/', InteractionListCreateView.as_view(), name='contact-interactions-list'),
    path('contacts/<int:contact_id>/interactions/<int:pk>/', InteractionDetailView.as_view(), name='contact-interactions-detail'),
    path('contacts/<int:contact_id>/schedules/', ScheduleListCreateView.as_view(), name='contact-schedules-list'),
    path('contacts/<int:contact_id>/schedules/<int:pk>/', ScheduleDetailView.as_view(), name='contact-schedules-detail'),
]
