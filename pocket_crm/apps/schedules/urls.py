from django.urls import path
from .views import UpcomingTouchpointListView, TouchpointDetailView

app_name = 'schedules'

urlpatterns = [
    path('upcoming/', UpcomingTouchpointListView.as_view(), name='upcoming-touchpoints'),
    path('<int:pk>/', TouchpointDetailView.as_view(), name='touchpoint-detail'),
]
